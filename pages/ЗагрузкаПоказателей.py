import streamlit as st
try:
    import pandas as pd
    from sqlalchemy import text
    import utils.utils as utils
    import numpy as np
    import utils.datums_db as datums_db
    import utils.datum_types_db as datum_types_db
    import utils.Stack as Stack
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
def get_infs_tabs():  

    conn = st.session_state["conn"]    
    query = """
        SELECT code,tab_name,tab_name_rus,type_name
        FROM infs_tabs 
    """
    params=[]
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows:
        df = pd.DataFrame(rows)
    else:
        columns = ['code','tab_name','tab_name_rus','type_name']
        df = pd.DataFrame(columns=columns)   
    return df
def get_id_datum_type_by_datum_type_code(datum_type_code):
    datum_types_df = datum_types_db.get_datum_types(datum_type_code = datum_type_code)
    return int(datum_types_df.loc[datum_types_df['code'] == datum_type_code, 'id'].iloc[0])
if st.button("Загрузить показатели"):
    subsystem_id = 1
    infs_tabs_df = get_infs_tabs()
    id_datum_type_tab = get_id_datum_type_by_datum_type_code('tab')
    if not st.session_state.get("datumsParentStack"):
        st.session_state.datumsParentStack = Stack.DatumsParentStack()
    for index, row in infs_tabs_df.iterrows():
        tabs_df = datums_db.get_datums_Вкладки(subsystem_id = subsystem_id)
        tabs_df = tabs_df[tabs_df['name']==row['tab_name']]
        if tabs_df.empty:
            params={}
            params["id_subsystem"] = subsystem_id
            params["name"] = row["tab_name"]
            params["fullname"] = row["tab_name_rus"]
            params["code"] = row["code"]
            params["id_datum_type"] = id_datum_type_tab
            params["parent_id"] = None 
            params["id_edizm"]  = None           
            datums_db.add_datum_dict(params = params)
        else:
            params={}
            params["id_subsystem"] = subsystem_id
            params["name"] = row["tab_name"]
            params["name"] = row["tab_name"]
            params["fullname"] = row["tab_name_rus"]
            params["code"] = row["code"]
            params["id_datum_type"] = id_datum_type_tab
            params["parent_id"] = None
            params["id_edizm"]  = None
            datums_db.update_datum_dict(params = params, original_row = tabs_df.to_dict())
        break    

    