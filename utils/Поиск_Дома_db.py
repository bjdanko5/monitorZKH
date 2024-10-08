import streamlit as st
import pandas as pd
import utils.utils as utils
from sqlalchemy import text 
def get_hierarchy(level,parentobjid):
    conn = st.session_state["conn"]
    query = """
            select 
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

def get_houses(parentobjid):
    conn = st.session_state["conn"]
    query = """
            select
            street_ns.NAME       as street_name,
            street_ns.TYPENAME   as street_typename,
            h.HOUSENUM    as housenum,
            h.ADDNUM1     as addnum1,
            h.ADDNUM2     as addnum2,    
            h.OBJECTID    as house_objectid,
            hier_street.OBJECTID    as street_objectid,
            hier_street.parentOBJID as street_parentobjid
            from ADMHIERARCHY hier_street
			
			join namespace as street_ns
            on hier_street.OBJECTID = street_ns.OBJECTID

			join ADMHIERARCHY hier_house
			on hier_street.OBJECTID = hier_house.PARENTOBJID
            
			join HOUSES h
            on hier_house.OBJECTID = h.OBJECTID  

            where  hier_street.OBJECTID = :parentobjid
            and hier_street.isactive = 1
			and hier_house.isactive = 1
			and h.isactive = 1
            order by
            street_ns.name,h.housenum
            """
    params = {"parentobjid": parentobjid}
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=["street_name", "street_typename", "housenum", "addnum1", "addnum2", "house_objectid", "street_objectid", "street_parentobjid"])
    return df
