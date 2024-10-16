import streamlit as st
import pandas as pd
try:
    import utils.utils as utils
    
    import utils.datums_db as datums_db
    import utils.datum_types_db as datum_types_db
    import utils.subsystems_db as subsystems_db
    import widgets.ВыборПодсистемы as so
    import widgets.ВыборПоказателя as sd
   
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
def fill_datum_types_df():
    datum_types_df = datum_types_db.get_datum_types()
    return datum_types_df
def fill_subsystems_df():
    subsystems_df = subsystems_db.get_subsystems()
    return subsystems_df
def fill_datums_container():  
    subsystems_df = subsystems_db.get_subsystems()
    datum_types_df = fill_datum_types_df()

    subsystem_id = st.session_state.get("selected_subsystem_id")
    datum_parent_id = st.session_state.datumsStack.peek_id()

    datums_df = datums_db.get_datums(subsystem_id = subsystem_id,datum_parent_id=datum_parent_id)
    original_datums_df = datums_df.copy()
    
    column_configuration = {
    "id": st.column_config.NumberColumn(
        "ИД", help="ИД", width="small",disabled=True
    ),
    "name": st.column_config.TextColumn(
        "Наименование",
        help="Наименование",
        width="medium",
        required=True       
    ),
    "fullname": st.column_config.TextColumn(
        "Полное Наименование",
        help="Полное Наименование",
        width="medium",
        required=True       
    ),

    "datum_type_id": st.column_config.NumberColumn(
        "ИД Типа Показателя",
        help="ИД Типа Показателя",
        width="small",
        required = True,
        disabled=True   
    ),   
    "datum_type_name": st.column_config.SelectboxColumn(
        "Тип Показателя 🔽",
        options=datum_types_df["name"].tolist(),    
        help="Роль",
        width="small",
        required = True
    ),
    "subsystem_id": st.column_config.NumberColumn(
        "ИД Подсистемы",
        help="ИД Подсистемы",
        width="small",
        disabled=True   
    ),   
    "subsystem_name": st.column_config.SelectboxColumn(
        "Подсистема 🔽",
        options=subsystems_df["name"].tolist(),    
        help="Подсистема",
        width="small",
        required = True
    ),

    }
    def datums_df_callback():
        def get_id_datum_type_by_datum_type_name(datum_type_name):
            return int(datum_types_df.loc[datum_types_df['name'] == datum_type_name, 'id'].iloc[0])
        def get_id_subsystem_by_subsystem_name(subsystem_name):
            return int(subsystems_df.loc[subsystems_df['name'] == subsystem_name, 'id'].iloc[0])

        #это заглушка на будущее
        ss = st.session_state["event_datums_df_editor"]
        edited_rows = ss["edited_rows"]
        added_rows = ss["added_rows"]
        deleted_rows = ss["deleted_rows"]
        # Обновление существующих данных
        for row_id, row in edited_rows.items():
            datum_name = row.get("name", original_datums_df.iloc[int(row_id)]["name"])
            datum_code = row.get("code", original_datums_df.iloc[int(row_id)]["code"])
            datum_fullname = row.get("fullname", original_datums_df.iloc[int(row_id)]["fullname"])
            datum_type_name = row.get("datum_type_name", original_datums_df.iloc[int(row_id)]["datum_type_name"])
            subsystem_name = row.get("subsystem_name", original_datums_df.iloc[int(row_id)]["subsystem_name"])
            datum_parent_id = row.get("parent_id", original_datums_df.iloc[int(row_id)]["parent_id"])
            datum_id_edizm = row.get("id_edizm", original_datums_df.iloc[int(row_id)]["id_edizm"])
            id_datum_type = get_id_datum_type_by_datum_type_name(datum_type_name)
            
            if "selected_subsystem_id" in st.session_state:
                id_subsystem = st.session_state.selected_subsystem_id
            else:
                id_subsystem = get_id_subsystem_by_subsystem_name(subsystem_name)
            
            selected_datum_parent_id = sd.get_selected_datum_parent_id()        

            datum_id = int(original_datums_df.iloc[int(row_id)]["id"])
            
            datums_db.update_datum(datum_id, datum_name,datum_code,datum_fullname, id_subsystem, id_datum_type, selected_datum_parent_id, datum_id_edizm)
            
        # Add new datumanizations
        for row in added_rows:
            name = row.get("name", "Показатель")
            code = row.get("code", "Код")
            fullname = row.get("name", "Полное Имя")
            datum_type_name = row.get("datum_type_name", "Показатель")
            id_edizm  = row.get("id_edizm", None)
            id_datum_type = get_id_datum_type_by_datum_type_name(datum_type_name)
            subsystem_name = row.get("subsystem_name", "Подсистема")
            if "selected_subsystem_id" in st.session_state:
              id_subsystem = get_id_subsystem_by_subsystem_name(subsystem_name)
            else:  
              id_subsystem = None
              utils.queue_op_status("Обязательно Выберите Подсистему",status_type="error")
              return

            selected_datum_parent_id = sd.get_selected_datum_parent_id()
            datums_db.add_datum( name,code,fullname,id_subsystem,id_datum_type,selected_datum_parent_id,id_edizm)
        # Delete datumanizations
        for row_id in deleted_rows:
            datum_id = int(original_datums_df.iloc[int(row_id)]["id"])
            datums_db.delete_datum(datum_id)
 
    datums_container = st.container()
    with datums_container:       
        event_datums_df= st.data_editor(
            datums_df,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            disabled=["id"],
            num_rows="dynamic",
            on_change=datums_df_callback,
            key="event_datums_df_editor"
            )

    return datums_df,column_configuration 

#Основная программа страницы
st.header("Показатели")
so_container = st.container()
so_container.subheader("Выбор Подсистемы")
so.ВыборПодсистемы(so_container)

sd_container = st.container()
sd_container.subheader("Выбор Вкладки / Показателя для отбора Показателей")

sd.ВыборПоказателя(sd_container,None)

if st.session_state.datumsStack.is_empty():

    if "selected_subsystem_id" in st.session_state:
        st.subheader("Вкладки Подсистемы " + str(st.session_state.selected_subsystem_name))
    else:    
        st.subheader("Вкладки Подсистемы не выбраны")
        
else:
    if "selected_subsystem_id" in st.session_state:
        st.subheader("Показатели Подсистемы " + str(st.session_state.selected_subsystem_name)+" в " + str(st.session_state.datumsStack.peek()["datum_name"]))
    else:    
        st.subheader("Показатели Подсистема и Родительский Показатель не выбраны")
    

datums_df,column_configuration = fill_datums_container()


op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Обновить"):
       st.rerun() 
utils.setup_op_status(op_status_container,"Редактируйте Показатели и нажмите Обновить")
