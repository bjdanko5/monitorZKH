import streamlit as st
try:
    import pandas as pd
    from sqlalchemy import text
    import utils.utils as utils
    import numpy as np
    import utils.datums_db as datums_db
    import utils.datum_types_db as datum_types_db
    import utils.edizms_db as edizms_db
    import utils.Stack as Stack
    import utils.subsystems_db as subsystems_db
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
def get_infs_tab_items(selected_tab_name):
    # выбираем показатели выбранной вкладки из infs
    conn = st.session_state["conn"]    
    query = """
        SELECT id,code, datum_name, datum_name_rus, tab_name, tab_name_rus, length, is_nullable, type_name
        FROM infs
        WHERE  tab_name=:tab_name
    """
    params={"tab_name":selected_tab_name}
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows:
        df = pd.DataFrame(rows)
    else:
        columns = ['id','code', 'datum_name', 'datum_name_rus', 'tab_name', 'tab_name_rus', 'length', 'is_nullable', 'type_name']
        df = pd.DataFrame(columns=columns)   
    return df

def get_infs_tabs():  
    conn = st.session_state["conn"]    
    query = """
        SELECT id,code,tab_name,tab_name_rus,type_name
        FROM infs_tabs 
    """
    params={}
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows:
        df = pd.DataFrame(rows)
    else:
        columns = ['id','code','tab_name','tab_name_rus','type_name']
        df = pd.DataFrame(columns=columns)   
    return df
def get_id_datum_type_by_datum_type_code(datum_type_code,selected_datum_parent_id = None):
    datum_types_df = datum_types_db.get_datum_types(datum_type_code = datum_type_code,datum_parent_id=selected_datum_parent_id)
    return int(datum_types_df.loc[datum_types_df['code'] == datum_type_code, 'id'].iloc[0])
def get_id_edizm_by_edizm_code(edizm_code):
    edizms_df =edizms_db.get_edizms(edizm_code = edizm_code)
    return int(edizms_df.loc[edizms_df['code'] == edizm_code, 'id'].iloc[0])
if st.button("Загрузить показатели"):
    st.session_state.datumsParentStack = Stack.DatumsParentStack()

    datumsParentStack = st.session_state.datumsParentStack;    

    subsystem_id = 1
    subsystems_df = subsystems_db.get_subsystems(subsystem_id = subsystem_id)
    
    datumsParentStack.set_id_subsystem(int(subsystems_df.iloc[0]["id"]))
    datumsParentStack.set_subsystem_name(subsystems_df.iloc[0]["name"])    
   
    infs_tabs_df = get_infs_tabs()
    id_datum_type_tab = get_id_datum_type_by_datum_type_code('tab')
    id_edizm_tab = get_id_edizm_by_edizm_code('empty')
    
    tabs_df = datums_db.get_datums(subsystem_id = subsystem_id)
    for index, row in infs_tabs_df.iterrows():
        tab_df = tabs_df.loc[tabs_df['name']==row['tab_name']]
        if tab_df.empty:
            params={}
            params["id_subsystem"] = subsystem_id
            params["name"] = row["tab_name"]
            params["fullname"] = row["tab_name_rus"]
            params["code"] = row["code"]
            params["id_datum_type"] = id_datum_type_tab
            params["parent_id"] = None 
            params["id_edizm"]  = id_edizm_tab           
            datums_db.add_datum_dict(params = params)
        else:
            params={}
            params["id_subsystem"] = subsystem_id
            params["name"] = row["tab_name"]
            params["fullname"] = row["tab_name_rus"]
            params["code"] = row["code"]
            params["id_datum_type"] = id_datum_type_tab
            params["parent_id"] = None
            params["id_edizm"]  = id_edizm_tab
            datums_db.update_datum_dict(params = params, original_row = tab_df.iloc[0].to_dict())

        selected_parent_datum_df = datums_db.get_datums(subsystem_id = subsystem_id,datum_name = row["tab_name"])
        selected_parent_datum = selected_parent_datum_df.iloc[0].to_dict()
        st.session_state.datumsParentStack.push(selected_parent_datum) 

        selected_subsystem_id        = datumsParentStack.get_id_subsystem()
        selected_datum_parent_id     = datumsParentStack.peek_id()
        selected_datum_parent_id_str = datumsParentStack.peek_id_str()

        infs_tab_items_df = get_infs_tab_items(row['tab_name'])

        
        datums_df = datums_db.get_datums(subsystem_id = selected_subsystem_id,datum_parent_id = selected_datum_parent_id)
        
        for tab_item_index, tab_item_row in infs_tab_items_df.iterrows():
            datum_df = datums_df.loc[datums_df['name']==tab_item_row['tab_name']]
            if datum_df.empty:
                params={}
                params["id_subsystem"] = selected_subsystem_id
                params["name"] = tab_item_row["datum_name"]
                params["fullname"] = tab_item_row["datum_name_rus"]
                params["code"] = tab_item_row["code"]
                if tab_item_row["type_name"] == 'nvarchar':
                   tab_item_row["type_name"] = 'string' 
                id_datum_type = get_id_datum_type_by_datum_type_code(tab_item_row["type_name"],selected_datum_parent_id)
                params["id_datum_type"] = id_datum_type
                params["parent_id"] = selected_datum_parent_id 
                params["id_edizm"]  = id_edizm_tab
                           
                datums_db.add_datum_dict(params = params)
            else:
                params={}
                params["id_subsystem"] = selected_subsystem_id
                params["name"] = tab_item_row["datum_name"]
                params["fullname"] = tab_item_row["datum_name_rus"]
                params["code"] = tab_item_row["code"]
                if tab_item_row["type_name"] == 'nvarchar':
                   tab_item_row["type_name"] = 'string' 
                id_datum_type = get_id_datum_type_by_datum_type_code(tab_item_row["type_name"],selected_datum_parent_id)
                params["id_datum_type"] = id_datum_type
                params["parent_id"] = selected_datum_parent_id 
                params["id_edizm"]  = id_edizm_tab

                datums_db.update_datum_dict(params = params, original_row = datum_df.iloc[0].to_dict())
                
        #####
        #####
        st.session_state.datumsParentStack.pop()  
        #break    

    