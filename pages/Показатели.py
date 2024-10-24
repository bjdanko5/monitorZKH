import streamlit as st
try:
    import utils.utils as utils
    
    import utils.datums_db as datums_db
    import utils.datum_types_db as datum_types_db
    import utils.subsystems_db as subsystems_db
    import widgets.ВыборПодсистемы as so
    import widgets.ВыборПоказателя as sd
    import utils.Stack as Stack
    import pprint
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
def fill_datums_container(datums_container):
    def datums_df_callback():
        def get_id_datum_type_by_datum_type_name(datum_type_name):
            return int(datum_types_df.loc[datum_types_df['name'] == datum_type_name, 'id'].iloc[0])
        def update_datums(edited_rows, original_datums_df):
            id_subsystem = st.session_state.datumsParentStack.get_id_subsystem()
            parent_id = st.session_state.datumsParentStack.peek_id()
  
            for row_id, row in edited_rows.items():
                
                original_row = original_datums_df.iloc[int(row_id)]
                
                datum_type_name = row.get("datum_type_name", original_row["datum_type_name"])
                id_datum_type = get_id_datum_type_by_datum_type_name(datum_type_name)
                
                row["id_subsystem"]  = id_subsystem
                row["parent_id"]     = parent_id
                row["id_datum_type"] = id_datum_type
                row["id_edizm"]      = None
              
                datums_db.update_datum_dict(row,original_row)

        def add_datums(added_rows):
            id_subsystem = st.session_state.datumsParentStack.get_id_subsystem()
            parent_id = st.session_state.datumsParentStack.peek_id()
            for row in added_rows:
                if parent_id is None:
                    datum_type_name ="Вкладка"
                else:    
                    datum_type_name = row.get("datum_type_name", "Тип Показателя")

                id_datum_type = get_id_datum_type_by_datum_type_name(datum_type_name)
                
                row["id_subsystem"]  = id_subsystem
                row["parent_id"]     = parent_id
                row["id_datum_type"] = id_datum_type
                row["id_edizm"]      = None

                datums_db.add_datum_dict(row)

        def delete_datums(deleted_rows):
            for row_id in deleted_rows:
                original_row = original_datums_df.iloc[int(row_id)]
                datum_id = int(original_row["id"])
                datums_db.delete_datum(datum_id)
 

        ss = st.session_state["event_datums_df_editor"]
       
        update_datums(ss["edited_rows"], original_datums_df)
        add_datums(ss["added_rows"])
        delete_datums(ss["deleted_rows"])

    #fill_datums_container тело функции-------------------------------  
    subsystem_id = st.session_state.datumsParentStack.get_id_subsystem()

    if not subsystem_id:
        st.write("Редактирование Показателей невозможно, т.к. не выбрана подсистема.")
        return 
    
    datum_parent_id = st.session_state.datumsParentStack.peek_id()
    
    subsystems_df  = subsystems_db.get_subsystems()
    datum_types_df = datum_types_db.get_datum_types(datum_parent_id = datum_parent_id)
        
    datums_df = datums_db.get_datums(subsystem_id = subsystem_id,datum_parent_id=datum_parent_id)

    original_datums_df = datums_df.copy()
    
    column_configuration = {
    
    "id": st.column_config.NumberColumn(
        "ИД", 
        help="ИД", 
        width="small",
        disabled=True
    ),

    "code": st.column_config.TextColumn(
        "Код",
        help="Код",
        width="medium",
        required=True       
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
    "datum_type_name": st.column_config.SelectboxColumn(
        "Тип Показателя 🔽",
        options=datum_types_df["name"].tolist(),    
        help="Роль",
        width="medium",
        required = True
    ),
    "page":None,
    "subsystem_name": None,
    "id_datum_type": None,
    "id_subsystem": None,
    "parent_id": None,
    "id_edizm" : None,

    }

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

    return 

#Основная программа страницы
st.header("Показатели")

if not st.session_state.get("datumsParentStack"):
    st.session_state.datumsParentStack = Stack.DatumsParentStack()

so_container = st.container()
so.ВыборПодсистемы(so_container)

sd_container = st.container()
sd.ВыборПоказателя(sd_container,None)

datums_container = st.container()
fill_datums_container(datums_container)

op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Обновить"):
       st.rerun() 
utils.setup_op_status(op_status_container,"Редактируйте Показатели и нажмите Обновить")
