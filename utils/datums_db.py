import streamlit as st
import pandas as pd
from sqlalchemy import text
import numpy as np
def prepare_int(i):
    return i if i is None else int(i)
def get_datums_Вкладки(subsystem_name=None, subsystem_id=None, subsystem_code=None, datum_parent_id=None):
    df = get_datums(subsystem_name=subsystem_name, subsystem_id=subsystem_id, subsystem_code=subsystem_code, datum_parent_id = None)
    df = df[df['parent_id'].isnull()]
    df = df[['id',"name","fullname"]]
    return df
def get_datums_Выбор(subsystem_name=None, subsystem_id=None, subsystem_code=None, datum_parent_id=None):
    df = get_datums(subsystem_name=subsystem_name, subsystem_id=subsystem_id, subsystem_code=subsystem_code, datum_parent_id=datum_parent_id)
    df = df[['id',"code","name","fullname","parent_id","id_subsystem"]]
    return df
def get_datums(subsystem_name=None, subsystem_id=None, subsystem_code=None, datum_parent_id=None,datum_lvl=None,datum_id_lvl=None,mode = None,datum_id = None,datum_code = None,datum_name = None):    
    engine = st.session_state["engine"]
    conn = engine.connect()
  
    query = """
        SELECT d.*, s.name AS subsystem_name, dt.name AS datum_type_name,e.name AS edizm_name
        FROM mzkh_datums d
        LEFT JOIN mzkh_subsystems s ON d.id_subsystem = s.id
        LEFT JOIN mzkh_datum_types dt ON d.id_datum_type = dt.id
        LEFT JOIN mzkh_edizms e ON d.id_edizm = e.id
        WHERE (:subsystem_name IS NULL OR s.name = :subsystem_name)
        AND (:subsystem_id IS NULL OR s.id = :subsystem_id)
        AND (:subsystem_code IS NULL OR s.code = :subsystem_code)
        AND (:datum_id IS NULL OR d.id = :datum_id)
        AND (:datum_code IS NULL OR d.code = :datum_code)
        AND (:datum_name IS NULL OR d.name = :datum_name)
        AND (:mode='all' OR :mode IS NULL AND (:datum_parent_id IS NULL AND parent_id IS NULL OR parent_id = :datum_parent_id))
        AND (:id_lvl0 IS NULL OR id_lvl0 = :id_lvl0)
        AND (:id_lvl1 IS NULL OR id_lvl1 = :id_lvl1)
        AND (:id_lvl2 IS NULL OR id_lvl2 = :id_lvl2)
        AND (:id_lvl3 IS NULL OR id_lvl3 = :id_lvl3)
        ORDER BY 
         CASE 
            WHEN d.code ~ '^[0-9]+(\.[0-9]+)*$' THEN string_to_array(d.code, '.')::int[]
            ELSE string_to_array('0', '.')::int[] 
        END    

    """
    #AND (:datum_parent_id IS NULL OR parent_id = :datum_parent_id)
    params = {
        "datum_id"      : datum_id,
        "datum_code"    : datum_code,
        "datum_name"   : datum_name,
        "subsystem_name": subsystem_name,
        "subsystem_id": prepare_int(subsystem_id),
        "subsystem_code": subsystem_code,
        "datum_parent_id": prepare_int(datum_parent_id),
        "mode"           : mode
    }
    
    for lvl in range(4):
        if datum_lvl == lvl:
            params[f"id_lvl{lvl}"] = datum_id_lvl
        else:    
            params[f"id_lvl{lvl}"] = None

    result = conn.execute(text(query), params)
    rows = result.fetchall()
    
    if rows:
        df = pd.DataFrame(rows)
    else:
        columns = ['id', 'name', 'id_subsystem', 'subsystem_name', 'id_datum_type', 'datum_type_name', "code", "fullname", "parent_id", "page", "id_edizm","lvl","id_lvl0","id_lvl1","id_lvl2","id_lvl3","edizm_name"]
        df = pd.DataFrame(columns=columns)
    conn.commit()
    conn.close()
    return df
def get_datums_with_childs(subsystem_name=None, subsystem_id=None, subsystem_code=None, datum_parent_id=None,datum_lvl=None,datum_id_lvl=None,mode = None,datum_id = None,datum_code = None,datum_name = None):    
    engine = st.session_state["engine"]
    conn = engine.connect()
  
    query = """
        SELECT d.*, s.name AS subsystem_name, dt.name AS datum_type_name,e.name AS edizm_name
        FROM mzkh_datums d
        LEFT JOIN mzkh_subsystems s ON d.id_subsystem = s.id
        LEFT JOIN mzkh_datum_types dt ON d.id_datum_type = dt.id
        LEFT JOIN mzkh_edizms e ON d.id_edizm = e.id
        WHERE (:subsystem_name IS NULL OR s.name = :subsystem_name)
        AND (:subsystem_id IS NULL OR s.id = :subsystem_id)
        AND (:subsystem_code IS NULL OR s.code = :subsystem_code)
        AND (:datum_id IS NULL OR d.id = :datum_id)
        AND (:datum_code IS NULL OR d.code = :datum_code)
        AND (:datum_name IS NULL OR d.name = :datum_name)
        --AND (:mode='all' OR :mode IS NULL AND (:datum_parent_id IS NULL AND parent_id IS NULL OR parent_id = :datum_parent_id))
        --AND (:datum_parent_id IS NULL AND parent_id IS NULL OR parent_id = :datum_parent_id)
        AND (
        :datum_parent_id IS  NULL 
        or
        :datum_parent_id IS NOT NULL 
        and(
           (id_lvl0 = :datum_parent_id)
        or (id_lvl1 = :datum_parent_id)
        or (id_lvl2 = :datum_parent_id)
        or ( id_lvl3 = :datum_parent_id)
        )
        )
        ORDER BY 
         CASE 
            WHEN d.code ~ '^[0-9]+(\.[0-9]+)*$' THEN string_to_array(d.code, '.')::int[]
            ELSE string_to_array('0', '.')::int[] 
        END    

    """
    #AND (:datum_parent_id IS NULL OR parent_id = :datum_parent_id)
    params = {
        "datum_id"      : datum_id,
        "datum_code"    : datum_code,
        "datum_name"   : datum_name,
        "subsystem_name": subsystem_name,
        "subsystem_id": prepare_int(subsystem_id),
        "subsystem_code": subsystem_code,
        "datum_parent_id": prepare_int(datum_parent_id),
        "mode"           : mode
    }
    
    for lvl in range(4):
        if datum_lvl == lvl:
            params[f"id_lvl{lvl}"] = datum_id_lvl
        else:    
            params[f"id_lvl{lvl}"] = None

    result = conn.execute(text(query), params)
    rows = result.fetchall()
    
    if rows:
        df = pd.DataFrame(rows)
    else:
        columns = ['id', 'name', 'id_subsystem', 'subsystem_name', 'id_datum_type', 'datum_type_name', "code", "fullname", "parent_id", "page", "id_edizm","lvl","id_lvl0","id_lvl1","id_lvl2","id_lvl3","edizm_name"]
        df = pd.DataFrame(columns=columns)
    conn.commit()
    conn.close()
    return df

   

def update_datum_level(params,new_record_id,tr_conn=None):
    if tr_conn:
        conn = tr_conn
    else:    
        engine = st.session_state["engine"]
        conn = engine.connect()

    params["lvl"], params["id_lvl0"], params["id_lvl1"], params["id_lvl2"], params["id_lvl3"] = st.session_state.datumsParentStack.get_lvl(new_record_id)
    update_query = """
                   UPDATE mzkh_datums
                   SET
                       lvl = :lvl,
                       id_lvl0 = :id_lvl0,
                       id_lvl1 = :id_lvl1,
                       id_lvl2 = :id_lvl2,
                       id_lvl3 = :id_lvl3
                   WHERE id = :id
                """
    conn.execute(text(update_query), {"id": new_record_id, "lvl": params["lvl"], "id_lvl0": params["id_lvl0"], "id_lvl1": params["id_lvl1"], "id_lvl2": params["id_lvl2"], "id_lvl3": params["id_lvl3"]})
    if not tr_conn:
      conn.commit()
      conn.close()
def add_datum_dict(params):
    engine = st.session_state["engine"]
    conn = engine.connect()
    params.pop("subsystem_name", None)
    params.pop("datum_type_name", None)
    
    params = {
    key: int(value) if isinstance(value, np.int64) 
    else "Не задано" if value in [None, ""] and isinstance(value, str) 
    else value 
    for key, value in params.items()
    }
    params["page"] = "mpages/" + params["code"] + ".py"

    insert_query = """
        INSERT INTO mzkh_datums (name, code, fullname, id_subsystem, id_datum_type, parent_id, page, id_edizm)
        VALUES (:name, :code, :fullname, :id_subsystem, :id_datum_type, :parent_id, :page, :id_edizm)
        RETURNING id;
    """
    result = conn.execute(text(insert_query), params)
    new_record_id = result.fetchone()[0]
    conn.commit()
    conn.close() 
    update_datum_level(params,new_record_id)
def StartTransaction():
    engine = st.session_state["engine"]
    conn = engine.connect()
    return conn 
def RolbackTransaction(conn):
    conn.rollback()
    conn.close()
def EndTransaction(conn):
    conn.commit()
    conn.close()
         
def update_datum_dict(params,original_row,tr_conn = None):
    if tr_conn:
       conn = tr_conn
    else:        
        engine = st.session_state["engine"]
        conn = engine.connect()
    params.update({key: value for key, value in original_row.items() if key not in params})
    params.pop("subsystem_name", None)
    params.pop("datum_type_name", None)
 
    params = {
        key: int(value) if isinstance(value, np.int64) 
            else "Не задано" if value in [None, ""] and isinstance(value, str) 
            else None if pd.isna(value) 
            else value 
        for key, value in params.items()
    }
    params["page"] = "mpages/" + params["code"] + ".py"

    query = """
        UPDATE mzkh_datums
        SET
            name = :name,
            code = :code,
            fullname = :fullname,
            id_subsystem = :id_subsystem,
            id_datum_type = :id_datum_type,
            parent_id = :parent_id,
            page = :page,
            id_edizm = :id_edizm
        WHERE id = :id
    """
    conn.execute(text(query), params)
   
    if not tr_conn:
        update_datum_level(params,params["id"],conn)
        conn.commit()
        conn.close()        
def update_datum_dict1(params,original_row,tr_conn = None):
    if tr_conn:
       conn = tr_conn
    else:        
        engine = st.session_state["engine"]
        conn = engine.connect()
    params.update({key: value for key, value in original_row.items() if key not in params})
    params.pop("subsystem_name", None)
    params.pop("datum_type_name", None)
 
    params = {
        key: int(value) if isinstance(value, np.int64) 
            else "Не задано" if value in [None, ""] and isinstance(value, str) 
            else None if pd.isna(value) 
            else value 
        for key, value in params.items()
    }
    params["page"] = "mpages/" + params["code"] + ".py"

    query = """
        UPDATE mzkh_datums
        SET
            name = :name,
            code = :code,
            fullname = :fullname,
            id_subsystem = :id_subsystem,
            id_datum_type = :id_datum_type,
            parent_id = :parent_id,
            page = :page,
            id_edizm = :id_edizm,
            lvl = :lvl,
            id_lvl0 =:id_lvl0,
            id_lvl1 =:id_lvl1,
            id_lvl2 =:id_lvl2,
            id_lvl3 =:id_lvl3
        WHERE id = :id
    """
    conn.execute(text(query), params)
   
    if not tr_conn:
        update_datum_level(params,params["id"],conn)
        conn.commit()
        conn.close()     

def delete_datum(datum_id):
    engine = st.session_state["engine"]
    conn = engine.connect()
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_datums WHERE id = :datum_id"
    conn.execute(text(query), {"datum_id": datum_id})
    conn.commit()
    conn.close()
   
