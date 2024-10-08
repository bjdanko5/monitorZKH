import streamlit as st
try:
    import utils.Поиск_Дома_db as hierarchy_db
except ImportError as e:
    print("Pressed Reload in Browser...")
#conn = utils.conn_and_auth_check()
def ПоискДома(selected_hierarchy_container,params):
  

    hierarchy_df = hierarchy_db.get_hierarchy(params["level"],params["parentobjid"])
    if hierarchy_df.empty:
        ВыборДома(params["parentobjid"])
        return
    
    column_configuration = {
        "objectid": st.column_config.NumberColumn(
            "objectid",
            help="objectid",
            width="small"
        ),
        "name": st.column_config.TextColumn(
            "Наименование",
            help="Наименование",
            width="medium"
        ),
        "typename": st.column_config.TextColumn(
            "Тип",
            help="Тип",
            width="medium"
        ),
        "level": st.column_config.NumberColumn(
            "Уровень",
            help="Уровень",
            width="small"
        ),
        "parentobjid": st.column_config.NumberColumn(
            "parentobjid",
            help="parentobjid",
            width="small"
        ),
        "house_objecitid": st.column_config.NumberColumn(
            "house_objecitid",
            help="house_objecitid",
            width="small"
        ),
        "housenum": st.column_config.TextColumn(
            "housenum",
            help="housenum",
            width="medium"
        ),
        "addnum1": st.column_config.TextColumn(
            "addnum1",
            help="addnum1",
            width="medium"
        ),
        "addnum2": st.column_config.TextColumn(
            "addnum2",
            help="addnum2",
            width="medium"
        )
        
    }

    def on_select_hierarchy_df():
        if len(st.session_state.event_hierarchy_df.selection.rows) > 0:
            selected_row_id = st.session_state.event_hierarchy_df.selection.rows[0]  
        if st.session_state.get("tagged_params_dict") is None:
            st.session_state.tagged_params_dict={}
         
        tagged_params_dict = st.session_state.tagged_params_dict   
        selected_level   = hierarchy_df.iloc[selected_row_id]["level"]   
        selected_parentobjid = hierarchy_df.iloc[selected_row_id]["parentobjid"]
        selected_name= hierarchy_df.iloc[selected_row_id]["name"]
        selected_typename= hierarchy_df.iloc[selected_row_id]["typename"]
        selected_objectid = hierarchy_df.iloc[selected_row_id]["objectid"]
        params = {"level":selected_level,"parentobjid":selected_parentobjid,"objectid":selected_objectid,"name":selected_name,"typename":selected_typename}
        tagged_params_dict = st.session_state.tagged_params_dict   
        selected_hierarchy_tag = str(selected_level)          
        tagged_params_dict[selected_hierarchy_tag] = {"params":params}       
        st.session_state.tagged_params_dict = tagged_params_dict   

    selected_hierarchy_tag = str(params["level"])
    #
    if st.session_state.get("tagged_params_dict") is None:
            st.session_state.tagged_params_dict={}
    tagged_params_dict = st.session_state.tagged_params_dict        
    if not selected_hierarchy_tag in tagged_params_dict:
        event_hierarchy_df = st.dataframe(
        hierarchy_df, 
        column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
        on_select=on_select_hierarchy_df,
        selection_mode="single-row",
        key="event_hierarchy_df")
    else:    
        with selected_hierarchy_container:
            if "selected_org_button"+selected_hierarchy_tag in st.session_state:
                st.empty()
        selected_hierarchy_button = st.button(
            label = str(st.session_state.tagged_params_dict[selected_hierarchy_tag]["params"]["typename"]+" "+
                        st.session_state.tagged_params_dict[selected_hierarchy_tag]["params"]["name"]
                        )
            ,
            type  ='primary',
            key   = "selected_org_button" +selected_hierarchy_tag
        )   
        if selected_hierarchy_button:
            st.session_state.tagged_params_dict = {k: v for k, v in st.session_state.tagged_params_dict.items() if int(k) <= int(selected_hierarchy_tag)-1}
            #del tagged_params_dict[selected_hierarchy_tag]
            st.rerun()
def ВыборДома(street_objectid):
    houses_df = hierarchy_db.get_houses(street_objectid)
    if houses_df.empty:
        st.write("Домов нет")
        return
    column_configuration = {
        "street_name": st.column_config.TextColumn(
            "Улица",
            help="Улица",
            width="medium"
        ),
        "street_typename": st.column_config.TextColumn(
            "Тип улицы",
            help="Тип улицы",
            width="medium"
        ),
        "housenum": st.column_config.TextColumn(
            "Номер дома",
            help="Номер дома",
            width="medium"
        ),
        "addnum1": st.column_config.TextColumn(
            "Корпус",
            help="Корпус",
            width="medium"
        ),
        "addnum2": st.column_config.TextColumn(
            "Строение",
            help="Строение",
            width="medium"
        ),
        "house_objectid": st.column_config.NumberColumn(
            "objectid",
            help="objectid",
            width="small"
        ),
        "street_objectid": st.column_config.NumberColumn(
            "street_objectid",
            help="street_objectid",
            width="small"
        ),
        "street_parentobjid": st.column_config.NumberColumn(
            "street_parentobjid",
            help="street_parentobjid",
            width="small"
        )
    }

    def on_select_houses_df():
         
         if len(st.session_state.event_houses_df.selection.rows) > 0:
            selected_row_id = st.session_state.event_houses_df.selection.rows[0]  
            st.session_state["selected_house_objectid"] = houses_df.iloc[selected_row_id]["house_objectid"]       
            
         else:   
           if "selected_house_objectid" in st.session_state:
            del st.session_state["selected_house_objectid"]
            st.rerun()
    event_houses_df = st.dataframe(
    houses_df, 
    column_config=column_configuration,
    use_container_width=True,
    hide_index=True,
    on_select=on_select_houses_df,
    selection_mode="single-row",
    key="event_houses_df")
    if "selected_house_objectid" in st.session_state:
        st.switch_page("pages/Дом.py")