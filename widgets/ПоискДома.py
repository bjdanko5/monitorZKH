import streamlit as st
from dataclasses import dataclass
@dataclass
class TaggedParams:
    tag: str
    params: dict
try:
    import utils.Поиск_Дома_db as hierarchy_db
except ImportError as e:
    print("Pressed Reload in Browser...")
#conn = utils.conn_and_auth_check()
def ПоискДома(selected_hierarchy_container,params):
  

    hierarchy_df = hierarchy_db.get_hierarchy(params["level"],params["parentobjid"])
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
        selected_hierarchy_tag = str(selected_level)+"_"+str(selected_parentobjid)           
        tagged_params_dict[selected_hierarchy_tag] = {"params":params}       
        st.session_state.tagged_params_dict = tagged_params_dict   

    selected_hierarchy_tag = str(params["level"])+"_"+str(params["parentobjid"])
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
            del tagged_params_dict[selected_hierarchy_tag]
            st.rerun()
