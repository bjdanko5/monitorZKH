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
#conn = utils.conn_and_auth_check()
def СправочникиПоказателей(selected_datums_container):
    
    def on_select_datums_df():
        selection_rows = st.session_state["event_spr_datums_df"].selection.rows
        if len(selection_rows) > 0:        
            selected_row_id = selection_rows[0] 
            selected_item = datums_df.iloc[selected_row_id].to_dict()
            if "справочник" in selected_item["datum_type_name"].lower():
                st.session_state.selected_spr_datum = selected_item
            else: st.session_state.spr_datum_deny = True   
    #------------------------------------------------ 

    #------------------------- тело функции-------------------------------  
    subsystem_id = st.session_state.datumsParentStack.get_id_subsystem()
    if not subsystem_id:
        st.write("Редактирование Справочников Показателей невозможно, т.к. не выбрана подсистема.")
        return 
    selected_datums_container.subheader("Редактирование Справочника Показателя")
    selected_spr_datum = st.session_state.get("selected_spr_datum",None)
    with selected_datums_container:
        if selected_spr_datum:   
            selected_datums_button = st.button(
                label=str(selected_spr_datum["code"]+" "+selected_spr_datum["name"]),
                type='primary',
                key="selected_spr_datum_button" 
            )
            if selected_datums_button:
                del st.session_state.selected_spr_datum_button
                del st.session_state.selected_spr_datum
                st.rerun()
    if selected_spr_datum is None:
        datum_parent_id = st.session_state.datumsParentStack.peek_id()
        
        datum_types_df = datum_types_db.get_datum_types(datum_parent_id = datum_parent_id)
            
        datums_df = datums_db.get_datums(subsystem_id = subsystem_id,datum_parent_id=datum_parent_id)
        
        column_configuration = {
        
        "id": st.column_config.NumberColumn(
            "ИД", 
            help="ИД", 
            width="small"
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

        with selected_datums_container:       
            event_spr_datums_df= st.dataframe(
                datums_df,
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                on_select=on_select_datums_df,
                selection_mode="single-row",
                key="event_spr_datums_df"
                )
        if st.session_state.get("spr_datum_deny", False):     
            st.info("Выберите показатель с типом '... из Справочника'",icon=":material/error:") 
            del st.session_state.spr_datum_deny 

