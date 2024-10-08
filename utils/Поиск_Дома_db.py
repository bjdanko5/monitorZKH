import streamlit as st
import pandas as pd
import utils.utils as utils
from sqlalchemy import text 
def get_hierarchy(level,parentobjid):
    conn = st.session_state["conn"]
    query = """
            select top 10 
                    a.OBJECTID    as objectid,
                    ns.NAME       as name,
                    ns.TYPENAME   as typename,
                    a.Level       as level,
                    a.parentOBJID as parentobjid,
                    h.OBJECTID    as house_objectid,
                    h.HOUSENUM    as housenum,
                    h.ADDNUM1     as addnum1,
                    h.ADDNUM2     as addnum2    
            from ADMHIERARCHY a
            join namespace as ns
            on a.OBJECTID = ns.OBJECTID
            left join HOUSES h
            on a.OBJECTID = h.OBJECTID  
            where  a.parentobjid = :parentobjid
            and a.isactive = 1
            order by
            ns.name
            """
    params = {"parentobjid": parentobjid}
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=["objectid", "name", "typename", "level", "parentobjid", "house_objectid", "housenum", "addnum1", "addnum2"])
    return df

def get_houses(level,parentobjid):
    conn = st.session_state["conn"]
    query = """
            select top 10 
                    a.OBJECTID    as objectid,
                    ns.NAME       as name,
                    ns.TYPENAME   as typename,
                    a.Level       as level,
                    a.parentOBJID as parentobjid,
                    h.OBJECTID    as house_objectid,
                    h.HOUSENUM    as housenum,
                    h.ADDNUM1     as addnum1,
                    h.ADDNUM2     as addnum2    
            from ADMHIERARCHY a
            join namespace as ns
            on a.OBJECTID = ns.OBJECTID
            left join HOUSES h
            on a.OBJECTID = h.OBJECTID  
            where  a.parentobjid = :parentobjid
            and a.isactive = 1
            order by
            ns.name
            """
    params = {"parentobjid": parentobjid}
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=["objectid", "name", "typename", "level", "parentobjid", "house_objectid", "housenum", "addnum1", "addnum2"])
    return df
