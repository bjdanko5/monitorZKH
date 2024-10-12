import streamlit as st
try:
    import utils.datums_db as datums_db
    import utils.datum_types_db as datum_types_db
except ImportError as e:
    print("Pressed Reload in Browser...")
#conn = utils.conn_and_auth_check()

def ВыборПоказателя(selected_datums_container,datum_parent_id):
    def on_select_datums_df():
        if len(st.session_state.event_datums_df.selection.rows) > 0:
            selected_row_id = st.session_state.event_datums_df.selection.rows[0]  
            st.session_state.pred_selected_datum_parent_id = st.session_state.selected_datum_parent_id
            st.session_state.selected_datum_parent_id = datums_df.iloc[selected_row_id]["parent_id"]
            st.session_state.selected_datum_code = datums_df.iloc[selected_row_id]["code"]
            st.session_state.selected_datum_name = datums_df.iloc[selected_row_id]["name"]
            st.session_state.selected_datum_fullname= datums_df.iloc[selected_row_id]["fullname"]
            st.session_state.selected_datumtype_name = datums_df.iloc[selected_row_id]["datum_type_name"]
            st.session_state.selected_datum_id = datums_df.iloc[selected_row_id]["id"]
            ВыборПоказателя(selected_datums_container,datum_parent_id) 
        else:    
            with selected_datums_container:
                if "selected_org_button"+ st.session_state.selected_datum_parent_id in st.session_state:
                    st.empty()
            selected_datums_button = st.button(
                label = str(st.session_state.selected_datum_code+" "+
                            st.session_state.selected_datum_name
                            )
                ,
                type  ='primary',
                key   = "selected_org_button" +st.session_state.selected_datum_parent_id
            )   
            if selected_datums_button:
                #st.session_state.tagged_params_dict = {k: v for k, v in st.session_state.tagged_params_dict.items() if int(k) <= int(selected_datums_tag)-1}
                st.session_state.selected_datum_parent_id = st.session_state.pred_selected_datum_parent_id
                st.session_state.pred_selected_datum_parent_id = None
                ВыборПоказателя(selected_datums_container,datum_parent_id) 
                st.rerun()

    datum_types_df = datum_types_db.get_datum_types()
    datums_df = datums_db.get_datums(datum_parent_id)
    if datums_df.empty:
        st.session_state.selected_datum_parent_id = None
        return

    column_configuration = {
    "id": st.column_config.NumberColumn(
        "ИД", help="ИД", width="small",disabled=True
    ),
    "parent_id": st.column_config.NumberColumn(
        "ИД datum_parent_id", help="ИД", width="small",disabled=True
    ),
    "name": st.column_config.TextColumn(
        "Наименование",
        help="Наименование",
        width="medium",
        required=True       
    ),
       "code": st.column_config.TextColumn(
        "Код",
        help="Код",
        width="small",
        required=True       
    ),
    "fullname": st.column_config.TextColumn(
        "Полное Наименование",
        help="Полное Наименование",
        width="medium",
        required=True       
    ),
    "datum_type_name": st.column_config.TextColumn(
        "Тип Показателя",
        help="Тип Показателя",
        width="small",
        required = True
    ),
    "subsystem_name": st.column_config.TextColumn(
        "Подсистема 🔽",
        help="Подсистема",
        width="small",
        required = True
    ),

    }
    event_datums_df = st.dataframe(
        datums_df, 
        column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
        on_select=on_select_datums_df,
        selection_mode="single-row",
        key="event_datums_df")

   