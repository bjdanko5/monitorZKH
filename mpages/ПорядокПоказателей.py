import streamlit as st
import networkx as nx
import pandas as pd
import utils.datums_db as datums_db
import utils.utils as utils
conn = utils.conn_and_auth_check()   
class DataFrameCodeHierarchy:
    def __init__(self, dataframe):
        self.graph = nx.DiGraph()
        self.dataframe = dataframe
        self.build_hierarchy()

    def build_hierarchy(self):
        for index, row in self.dataframe.iterrows():
            code = row['code']
            self.graph.add_node(code, original_code=code)
            # Добавляем узел с исходным кодом

    def move_code(self, source_code, target_code):
        source_index = self.dataframe.index[self.dataframe['code'] == source_code].tolist()
        target_index = self.dataframe.index[self.dataframe['code'] == target_code].tolist()
        
        # Проверка на перемещение последнего элемента в рамках родительского элемента
        parent_source_code = '.'.join(source_code.split('.')[:-1])
        parent_target_code = '.'.join(target_code.split('.')[:-1])
        
        max_code_in_parent = max([int(code.split('.')[-1]) for code in self.dataframe['code'] if code.startswith(parent_source_code)])
        
        if parent_source_code == parent_target_code and int(source_code.split('.')[-1]) == max_code_in_parent:
            utils.queue_op_statuses("Невозможно сдвинуть последний элемент вниз")
            return
        
        # Проверка на непрерывность нумерации
        codes = sorted([source_code, target_code])
        start_code_num = int(codes[0].replace('.', ''))
        end_code_num = int(codes[1].replace('.', ''))
        
        if end_code_num - start_code_num > 1:
            for i in range(start_code_num + 1, end_code_num):
                code_to_check = '.'.join(list(str(i)))
                if code_to_check not in self.dataframe['code'].values:
                    utils.queue_op_statuses(f"Предупреждение: Потенциальная 'дыра' в нумерации  на {code_to_check}","error")
                    return
        
        # Перемещение кодов
        if len(source_index) == 1 and (len(target_index) == 1 or len(target_index) == 0):
            # Обновить поле code для обоих кодов
            if len(target_index) == 1:
                self.dataframe.loc[target_index[0], 'code'] = source_code
            self.dataframe.loc[source_index[0], 'code'] = target_code
            utils.queue_op_statuses(f"Показатели с Кодами {source_code} и {target_code} обменяны местами")
        else:
            utils.queue_op_statuses(f"Ошибка: Код {source_code} не найден или  несколько найдено показателей с одинаковым кодом","error")

    def move_up(self, code):
        code_list = code.split('.')
        if len(code_list) > 1:
            parent_code = '.'.join(code_list[:-1])
            min_subpoint = min([int(subcode.split('.')[-1]) for subcode in self.dataframe['code'].values if subcode.startswith(parent_code)])
            if int(code_list[-1]) > min_subpoint:
                new_code = parent_code + '.' + str(int(code_list[-1]) - 1)
                self.move_code(code, new_code)
            else:
                utils.queue_op_statuses("Невозможно сдвинуть вверх первый показатель")
        else:
            utils.queue_op_statuses("Недопустимый формат Кода ","error")

    def move_down(self, code):
        parent_code = '.'.join(code.split('.')[:-1])
        current_subpoint = int(code.split('.')[-1])
        next_subpoint = current_subpoint + 1
        min_subpoint = 1
        max_subpoint = max([int(subcode.split('.')[-1]) for subcode in self.dataframe['code'].values if subcode.startswith(parent_code)], default=0)
        
        # Проверка на возможность перемещения вниз
        if next_subpoint <= max_subpoint:
            new_code = f"{parent_code}.{next_subpoint}"
            self.move_code(code, new_code)    
        else:
            utils.queue_op_statuses("Невозможно сдвинуть последний элемент вниз")

    def levelUp(self, code):
        code_list = code.split('.')
        if len(code_list) > 1:
            new_code = '.'.join(code_list[:-1])
            self.move_code(code, new_code)

    def levelDown(self, code):
        self.move_down(code)

def show_datums_reorder():
    #------------------------------------------------    
    def on_select_datums_reorder_df():
        selection_rows = st.session_state["event_datums_reorder_df"].selection.rows
        st.session_state.datums_reorder_selection = selection_rows                   
        if len(selection_rows) > 0:        
            selected_row_id = selection_rows[0] 
            selected_item = datums_reorder_df.iloc[selected_row_id].to_dict()
            st.session_state["selected_datum_reorder"] = selected_item
            #st.session_state["datum_reorder_rerun"] = True
            #datumsParentStack.push(selected_item)
    #------------------------------------------------    
    #data = {
    #    'code': [
    #        '13.3', '13.3.1', '13.3.2', '13.3.3', '13.3.4',
    #        '13.3.5', '13.3.6', '13.3.7', '13.4',
    #        '13.4.1', '13.4.2', '13.4.3', '13.4.4',
    #        '13.4.5', '13.4.6', '13.4.7'
    #    ]
    #}
    ##df = pd.DataFrame(data)
    #if not "selected_datum_reorder" in st.session_state:
    
    if not st.session_state.get("datumsParentStack",None) or not st.session_state.datumsParentStack.peek() :
        st.swith_page("mpages/Показатели.py")
    datum_parent_id = st.session_state.datumsParentStack.peek_id()
    subsystem_id = st.session_state.datumsParentStack.get_id_subsystem()
    datums_reorder_df = datums_db.get_datums(subsystem_id = 1, datum_parent_id = datum_parent_id)
     
    if not datums_reorder_df.empty:
        column_configuration = {
        "id": st.column_config.NumberColumn(
            "ИД", help="ИД", width="small",disabled=True
        ),
        "code": st.column_config.TextColumn(
            "Код",
            help="Код",
            width="medium",
            required=True,
            disabled=True       
        ), 
        "name": st.column_config.TextColumn(
            "Тег",
            help="Тег",
            width="large",
            required=True,
            disabled=True       
        ),

        "fullname": st.column_config.TextColumn(
            "Наименование",
            help="Наименование",
            width="large",
            required=True,
            disabled=True       
        ),

        "parent_id":None,
        "id_subsystem":None,       
        #"name":None,
        #"fullname": st.column_config.TextColumn(
        #    "Полное Наименование",
        #    help="Полное Наименование",
        #    width="medium",
        #    required=True       
        #),
        }
    event_datums_reorder_df = st.dataframe(
        datums_reorder_df, 
        column_config=column_configuration,
        use_container_width=False,
        hide_index=True,
        on_select=on_select_datums_reorder_df,
        selection_mode="single-row",
        key="event_datums_reorder_df")
    datums_reorder_df['original_code'] = datums_reorder_df['code']
   
    return datums_reorder_df   

#if not "selected_datum_reorder" in st.session_state: 
#del st.session_state["selected_datum_reorder"]
#reorder_container = st.empty()
#with reorder_container:
if not st.session_state.get("datumsParentStack",None) or not st.session_state.datumsParentStack.peek() :
        st.swith_page("mpages/Показатели.py")
st.header("Порядок показателей")
datums_reorder_df = show_datums_reorder()
df_code_hierarchy = DataFrameCodeHierarchy(datums_reorder_df)

if "selected_datum_reorder" in st.session_state:
    st.markdown(f"#### Выбран {st.session_state.selected_datum_reorder['code']} {st.session_state.selected_datum_reorder['fullname']}")
    if st.button("Вверх",icon=":material/arrow_upward:"):
        utils.queue_op_statuses(f"Сдвиг показателя {st.session_state.selected_datum_reorder['code']} вверх")
        df_code_hierarchy.move_up(st.session_state.selected_datum_reorder["code"])
        
        diff_df = datums_reorder_df.loc[datums_reorder_df['code'] != datums_reorder_df['original_code']]
        
        for diff_index,diff_row  in diff_df.iterrows():
            diff_row['original_code'] = diff_row['code']
            params = diff_row.to_dict()
            original_row = diff_row.to_dict()
            datums_db.update_datum_dict(params = params, original_row = original_row)
        del st.session_state["selected_datum_reorder"]         
        st.rerun()
    if st.button("Вниз",icon=":material/arrow_downward:"):       
        utils.queue_op_statuses(f"Сдвиг показателя {st.session_state.selected_datum_reorder['code']} вниз")
        df_code_hierarchy.move_down(st.session_state.selected_datum_reorder["code"])
        
        diff_df = datums_reorder_df.loc[datums_reorder_df['code'] != datums_reorder_df['original_code']]
        
        for diff_index,diff_row  in diff_df.iterrows():
            diff_row['original_code'] = diff_row['code']
            params = diff_row.to_dict()
            original_row = diff_row.to_dict()
            datums_db.update_datum_dict(params = params, original_row = original_row)
        del st.session_state["selected_datum_reorder"]     
        st.rerun()
op_status_container = st.empty()
utils.setup_op_status(op_status_container,"Выберите Показатель для перемещения")


# Тест levelUp
#st.info("\nMoving '13.3.1' level up in the DataFrame")
#df_code_hierarchy.levelUp('13.3.1')
# Тест levelDown
#st.info("\nMoving '13.3.1' level down in the DataFrame")
#df_code_hierarchy.levelDown('13.3.1')
