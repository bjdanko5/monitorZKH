import streamlit as st
try:
    import utils.utils as utils
except ImportError as e:
    print("Pressed Reload in Browser...")
import pandas as pd
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
def get_house(objectid):
    conn = st.session_state["conn"]
    query = """
  select
			hp.value            as post_index,
			hier5_ns.NAME       as hier5_name,
            hier5_ns.TYPENAME   as hier5_typename,
            hier4_ns.NAME       as hier4_name,
            hier4_ns.TYPENAME   as hier4_typename,
            hier3_ns.NAME       as hier3_name,
            hier3_ns.TYPENAME   as hier3_typename,
            hier2_ns.NAME       as hier2_name,
            hier2_ns.TYPENAME   as hier2_typename,
            hier1_ns.NAME       as hier1_name,
            hier1_ns.TYPENAME   as hier1_typename,

            street_ns.NAME       as street_name,
            street_ns.TYPENAME   as street_typename,
            h.HOUSENUM    as housenum,
            h.ADDNUM1     as addnum1,
            h.ADDNUM2     as addnum2,    
            h.OBJECTID    as house_objectid,
            hier_street.OBJECTID    as street_objectid,
			hier1.OBJECTID  as hier1_objectid,
			hier2.OBJECTID  as hier2_objectid,
			hier3.OBJECTID  as hier3_objectid,
			hier4.OBJECTID  as hier4_objectid

            from HOUSES h
			
			join ADMHIERARCHY hier_house
            on hier_house.OBJECTID = h.OBJECTID  
			
			join ADMHIERARCHY hier_street 
			on hier_street.OBJECTID = hier_house.PARENTOBJID
			
			join ADMHIERARCHY hier1
			on hier1.OBJECTID = hier_street.PARENTOBJID

			join namespace as hier1_ns
            on hier1.OBJECTID = hier1_ns.OBJECTID

			join ADMHIERARCHY hier2
			on hier2.OBJECTID = hier1.PARENTOBJID

			join namespace as hier2_ns
            on hier2.OBJECTID = hier2_ns.OBJECTID


			left join ADMHIERARCHY hier3
			on hier3.OBJECTID = hier2.PARENTOBJID

			left join namespace as hier3_ns
            on hier3.OBJECTID = hier3_ns.OBJECTID


			left join ADMHIERARCHY hier4
			on hier4.OBJECTID = hier3.PARENTOBJID

			left join namespace as hier4_ns
            on hier4.OBJECTID = hier4_ns.OBJECTID

			left join ADMHIERARCHY hier5
			on hier5.OBJECTID = hier4.PARENTOBJID

			left join namespace as hier5_ns
            on hier5.OBJECTID = hier5_ns.OBJECTID
			
			join namespace as street_ns
            on hier_street.OBJECTID = street_ns.OBJECTID

            left join HOUSESPARAMS hp
			on hp.OBJECTID = h.OBJECTID 
               and hp.TYPEID = 5
			   and hp.ENDDATE >now()

            where  h.OBJECTID = :objectid
            and hier_street.isactive = 1
			and hier_house.isactive = 1
			and h.isactive = 1
            order by
            street_ns.name,h.housenum


            """
    params = {"objectid": objectid}
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=["post_index", "hier5_name", "hier5_typename","hier4_name", "hier4_typename", 
                                   "hier3_name", "hier3_typename", "hier2_name", "hier2_typename", 
                                   "hier1_name", "hier1_typename", "street_name", "street_typename", 
                                   "housenum", "addnum1", "addnum2","house_objectid", "street_objectid", 
                                   "hier1_objectid", "hier2_objectid","hier3_objectid", "hier4_objectid"])
    return df

def format_address(df):
    address = ""
    if not df.empty:
        # Skip empty post_index
        if not pd.isnull(df["post_index"].iloc[0]):
            address += df["post_index"].iloc[0] + ", "
        
        # Add hierarchy levels, skipping empty ones
        for level, level_type in zip(["hier5_name", "hier4_name", "hier3_name", "hier2_name", "hier1_name"],
                                     ["hier5_typename", "hier4_typename", "hier3_typename", "hier2_typename", "hier1_typename"]):
            if not pd.isnull(df[level].iloc[0]):
                address += df[level_type].iloc[0] + " " + df[level].iloc[0] + ", "
        
        # Add street and house number
        address += df["street_typename"].iloc[0] + " " + df["street_name"].iloc[0] + ", "
        address += df["housenum"].iloc[0] + " "
        
        # Add additional address details
        if not pd.isnull(df["addnum1"].iloc[0]) and df["addnum1"].iloc[0].strip() != "":
            address += "к. " + df["addnum1"].iloc[0].strip() + " "
        if not pd.isnull(df["addnum2"].iloc[0]) and df["addnum2"].iloc[0].strip() != "":
            address += "ст. " + df["addnum2"].iloc[0].strip() + " "
    
    return address.strip()