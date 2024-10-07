import streamlit as st
from dataclasses import dataclass
@dataclass
class TaggedParams:
    tag: str
    params: dict
try:
    import utils.Поиск_Дома_db as hierarhy_db
except ImportError as e:
    print("Pressed Reload in Browser...")
#conn = utils.conn_and_auth_check()
def ВыборОрганизации(selected_hierarhy_container,params):
    params = {"level":0,"parentobjid":0}
    #selected_hierarhy = (0,0 )
    if st.session_state.get("tagged_params_dict") is None:
       st.session_state.tagged_params_dict=[]
    else:
        tagged_params_dict = st.session_state.tagged_params_dict   
    selected_hierarhy_tag = str(params.level)+"_"+str(params.parentobjid)
    
    tagged_params_dict[selected_hierarhy_tag] = {"params":params}

    hierarhy_df = hierarhy_db.hierarhy_df(selected_hierarhy.level,selected_hierarhy.parentobjid)
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

    def on_select_hierarhy_df():
        if len(st.session_state.event_hierarhy_df.selection.rows) > 0:
            selected_row_id = st.session_state.event_hierarhy_df.selection.rows[0]          
            selected_org_id   = hierarhy_df.iloc[selected_row_id]["id"]   
            selected_org_name = hierarhy_df.iloc[selected_row_id]["name"]
            st.session_state.selected_org_id = selected_org_id
            st.session_state.selected_org_name = selected_org_name

    if not "selected_org_id" in st.session_state:
        event_hierarhy_df = st.dataframe(
        hierarhy_df, 
        column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
        on_select=on_select_hierarhy_df,
        selection_mode="single-row",
        key="event_hierarhy_df")
    else:    
        with selected_hierarhy_container:
            if "selected_org_button" in st.session_state:
                st.empty()
    
        selected_org_button = st.button(
            label = st.session_state.selected_org_name,
            type  ='primary',
            key   = "selected_org_button" +selected_hierarhy_tag
        )   
        if selected_org_button:
            del st.session_state.selected_org_id 
            del st.session_state.selected_org_name 
            st.rerun()
