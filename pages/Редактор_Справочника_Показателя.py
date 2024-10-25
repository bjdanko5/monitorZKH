import streamlit as st
try:
    import utils.utils as utils
    import utils.options_db as options_db
    import utils.subsystems_db as subsystems_db
    import pprint
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
def РедакторСправочника(options_container):
    def options_df_callback():
        def get_id_option_type_by_option_type_name(option_type_name):
            return int(option_types_df.loc[option_types_df['name'] == option_type_name, 'id'].iloc[0])
        def update_options(edited_rows, original_options_df):
            id_subsystem = st.session_state.optionsParentStack.get_id_subsystem()
            parent_id = st.session_state.optionsParentStack.peek_id()
  
            for row_id, row in edited_rows.items():
                
                original_row = original_options_df.iloc[int(row_id)]
                
                option_type_name = row.get("option_type_name", original_row["option_type_name"])
                id_option_type = get_id_option_type_by_option_type_name(option_type_name)
                
                row["id_subsystem"]  = id_subsystem
                row["parent_id"]     = parent_id
                row["id_option_type"] = id_option_type
                row["id_edizm"]      = None
              
                options_db.update_option_dict(row,original_row)

        def add_options(added_rows):
            id_subsystem = st.session_state.optionsParentStack.get_id_subsystem()
            parent_id = st.session_state.optionsParentStack.peek_id()
            for row in added_rows:
                if parent_id is None:
                    option_type_name ="Вкладка"
                else:    
                    option_type_name = row.get("option_type_name", "Тип Показателя")

                id_option_type = get_id_option_type_by_option_type_name(option_type_name)
                
                row["id_subsystem"]  = id_subsystem
                row["parent_id"]     = parent_id
                row["id_option_type"] = id_option_type
                row["id_edizm"]      = None

                options_db.add_option_dict(row)

        def delete_options(deleted_rows):
            for row_id in deleted_rows:
                original_row = original_options_df.iloc[int(row_id)]
                option_id = int(original_row["id"])
                options_db.delete_option(option_id)
 

        ss = st.session_state["event_options_df_editor"]
       
        update_options(ss["edited_rows"], original_options_df)
        add_options(ss["added_rows"])
        delete_options(ss["deleted_rows"])

    #fill_options_container тело функции-------------------------------  
    subsystem_id = st.session_state.optionsParentStack.get_id_subsystem()

    if not subsystem_id:
        st.write("Редактирование Справочника невозможно, т.к. не выбрана подсистема.")
        return 
    
    option_parent_id = st.session_state.optionsParentStack.peek_id()
    
    subsystems_df  = subsystems_db.get_subsystems()
    option_types_df = option_types_db.get_option_types(option_parent_id = option_parent_id)
        
    options_df = options_db.get_options(subsystem_id = subsystem_id,option_parent_id=option_parent_id)

    original_options_df = options_df.copy()
    
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
    "option_type_name": st.column_config.SelectboxColumn(
        "Тип Показателя 🔽",
        options=option_types_df["name"].tolist(),    
        help="Роль",
        width="medium",
        required = True
    ),
    "page":None,
    "subsystem_name": None,
    "id_option_type": None,
    "id_subsystem": None,
    "parent_id": None,
    "id_edizm" : None,

    }

    with options_container:       

        event_options_df= st.data_editor(
            options_df,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            disabled=["id"],
            num_rows="dynamic",
            on_change=options_df_callback,
            key="event_options_df_editor"
            )

    return 
