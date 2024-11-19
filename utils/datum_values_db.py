import streamlit as st
import pandas as pd
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy import text
import numpy as np
import math
from datetime import datetime
def prepare_int(i):
    return i if i is None else int(i)
def get_datum_values(id_houses_objectid,subsystem_name=None, subsystem_id=None, subsystem_code=None, datum_parent_id=None,datum_lvl=None,datum_id_lvl=None,mode = None,selected_datum_id = None):
    engine = st.session_state["engine"]
    conn = engine.connect()
    query = """
       SELECT d.*, 
       s.name AS subsystem_name,
       dt.name AS datum_type_name,
       dt.code AS datum_type_code
      ,e.name  AS edizm_name
      ,v.id AS id_datum_values
      ,COALESCE(v.int_value,0) AS int_value
      ,COALESCE(v.float_value,0) AS float_value
      ,v.date_value AS date_value
      ,COALESCE(v.nvarchar_value,'') AS nvarchar_value
      ,v.id_table_value AS id_table_value
      ,COALESCE(v.id_houses_objectid,v.id_unlinked_houses_id) AS id_houses_objectid
        FROM mzkh_datums d
        LEFT JOIN mzkh_datum_values v ON  d.id = v.id_datum
        AND :id_houses_objectid = v.id_houses_objectid
        LEFT JOIN mzkh_subsystems s ON d.id_subsystem = s.id
        LEFT JOIN mzkh_datum_types dt ON d.id_datum_type = dt.id
        LEFT JOIN mzkh_edizms e ON d.id_edizm = e.id
        WHERE (:subsystem_name IS NULL OR s.name = :subsystem_name)
        AND (:subsystem_id IS NULL OR s.id = :subsystem_id)
        AND (:subsystem_code IS NULL OR s.code = :subsystem_code)
        AND (:mode='all' OR :mode IS NULL AND (:datum_parent_id IS NULL AND d.parent_id IS NULL OR d.parent_id = :datum_parent_id))
        AND (:id_lvl0 IS NULL OR d.id_lvl0 = :id_lvl0)
        AND (:id_lvl1 IS NULL OR d.id_lvl1 = :id_lvl1)
        AND (:id_lvl2 IS NULL OR d.id_lvl2 = :id_lvl2)
        AND (:id_lvl3 IS NULL OR d.id_lvl3 = :id_lvl3)
        AND (:mode='all' OR :mode='one' AND (:selected_datum_id = v.id_datum))       
        ORDER BY 
        CASE 
            WHEN d.code ~ '^[0-9]+(\.[0-9]+)*$' THEN string_to_array(d.code, '.')::int[]
            ELSE string_to_array('0', '.')::int[] 
        END    

    """
    #AND (:datum_parent_id IS NULL OR parent_id = :datum_parent_id)
    params = {
        "subsystem_name"    : subsystem_name,
        "subsystem_id"      : prepare_int(subsystem_id),
        "subsystem_code"    : subsystem_code,
        "datum_parent_id"   : prepare_int(datum_parent_id),
        "mode"              : mode,
        "selected_datum_id" : prepare_int(selected_datum_id),
        "id_houses_objectid": prepare_int(id_houses_objectid)
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
        columns = ['id', 'name', 'id_subsystem', 'subsystem_name', 'id_datum_type', 'datum_type_name','datum_type_code', 'code', 'fullname', 'parent_id', 'page', 'id_edizm','lvl','id_lvl0','id_lvl1','id_lvl2','id_lvl3','id_datum_values','int_value','float_value','date_value','nvarchar_value','id_table_value','id_houses_objectid']
        df = pd.DataFrame(columns=columns)
    conn.commit()
    conn.close()
    return df
def get_datum_value(id_houses_objectid,selected_datum_id):
    engine = st.session_state["engine"]
    conn = engine.connect()
    query = """
       SELECT d.*, 
       s.name AS subsystem_name,
       dt.name AS datum_type_name,
       dt.code AS datum_type_code
      ,e.name  AS edizm_name
      ,v.id AS id_datum_values
      ,COALESCE(v.int_value,0) AS int_value
      ,COALESCE(v.float_value,0) AS float_value
      ,v.date_value AS date_value
      ,COALESCE(v.nvarchar_value,'') AS nvarchar_value
      ,v.id_table_value AS id_table_value
      ,COALESCE(v.id_houses_objectid,v.id_unlinked_houses_id) AS id_houses_objectid
        FROM mzkh_datums d
        LEFT JOIN mzkh_datum_values v ON  d.id = v.id_datum
        AND :id_houses_objectid = v.id_houses_objectid
        LEFT JOIN mzkh_subsystems s ON d.id_subsystem = s.id
        LEFT JOIN mzkh_datum_types dt ON d.id_datum_type = dt.id
        LEFT JOIN mzkh_edizms e ON d.id_edizm = e.id
        WHERE :selected_datum_id = v.id_datum
        ORDER BY 
         CASE 
            WHEN d.code ~ '^[0-9]+(\.[0-9]+)*$' THEN string_to_array(d.code, '.')::int[]
            ELSE string_to_array('0', '.')::int[] 
        END    

    """
    #AND (:datum_parent_id IS NULL OR parent_id = :datum_parent_id)
    params = {
        "selected_datum_id" : prepare_int(selected_datum_id),
        "id_houses_objectid": prepare_int(id_houses_objectid)
    }
    
    
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    
    if rows:
        df = pd.DataFrame(rows)
    else:
        columns = ['id', 'name', 'id_subsystem', 'subsystem_name', 'id_datum_type', 'datum_type_name','datum_type_code', 'code', 'fullname', 'parent_id', 'page', 'id_edizm','lvl','id_lvl0','id_lvl1','id_lvl2','id_lvl3','id_datum_values','int_value','float_value','date_value','nvarchar_value','id_table_value','id_houses_objectid']
        df = pd.DataFrame(columns=columns)
    conn.commit()
    conn.close()
    return df

def merge_datum_values_values(conn,params):
    #if params["date_value"] == None:
    #    params["date_value"] = datetime.now() 
    #if params["id_table_value"] == None:
    #    params["id_table_value"] = 0 
      
    #keys_params = ['id', 'name', 'id_subsystem', 'subsystem_name', 'id_datum_type', 'datum_type_name','datum_type_code', 'code', 'fullname', 'parent_id', 'page', 'id_edizm','lvl','id_lvl0','id_lvl1','id_lvl2','id_lvl3','id_datum_values','int_value','float_value','date_value','nvarchar_value','id_table_value','id_houses_objectid']
    engine = st.session_state["engine"]
    conn = engine.connect()
    keys_needed_params=['id_datum_values', 'id_datum', 'int_value', 'float_value','date_value','nvarchar_value','id_table_value','id_houses_objectid','id_unlinked_houses_id']
    
    params['id_datum'] = params['id']
    
    params = {
        key: int(value) if isinstance(value, np.int64) else "Не задано" if value in [None, ""] and isinstance(value, str) else value
        for key, value in params.items() if key in keys_needed_params
    }
    if params['int_value'] == True:
       params['int_value'] = 1
    else:    
       params['int_value'] = 0
    params['id'] = params.pop('id_datum_values') if 'id_datum_values' in params else params.get('id_datum_values')
    #params['id'] = params.pop('id_datum_values', params.get('id_datum_values'))
    params['id_unlinked_houses_id'] = None

    params = {key: None if isinstance(value, float) and math.isnan(value) else value for key, value in params.items()}
    print("Parameters being passed to the query:")
    for key, value in params.items():
        print(f"{key}: {value} (type: {type(value)})")
    merge_query =   """   
                    MERGE INTO mzkh_datum_values AS target
                    USING (SELECT :id AS id, :id_datum AS id_datum, :int_value AS int_value, 
                           :float_value AS float_value, :date_value AS date_value, 
                           :nvarchar_value AS nvarchar_value, :id_table_value AS id_table_value, 
                           :id_houses_objectid AS id_houses_objectid, 
                           :id_unlinked_houses_id AS id_unlinked_houses_id) 
                    AS source 
                    (id, id_datum, int_value, float_value, date_value, nvarchar_value, id_table_value, id_houses_objectid, id_unlinked_houses_id)
                    ON target.id_datum = source.id_datum
                    and target.id_houses_objectid = source.id_houses_objectid
                    WHEN MATCHED THEN
                        UPDATE SET
                            id_datum = source.id_datum,
                            int_value = source.int_value,
                            float_value = source.float_value,
                            date_value = cast(source.date_value as date),
                            nvarchar_value = source.nvarchar_value,
                            id_table_value = cast(source.id_table_value as bigint),
                            id_houses_objectid = source.id_houses_objectid,
                            id_unlinked_houses_id = cast(source.id_unlinked_houses_id as bigint)
                    WHEN NOT MATCHED THEN
                        INSERT (id_datum, int_value, float_value, date_value, nvarchar_value, id_table_value, id_houses_objectid, id_unlinked_houses_id)
                        --OUTPUT Inserted.ID
                        VALUES (source.id_datum, source.int_value, source.float_value, cast(source.date_value as date), source.nvarchar_value, cast(source.id_table_value as bigint), source.id_houses_objectid, cast(source.id_unlinked_houses_id as bigint));
                    """

    try:
        result = conn.execute(text(merge_query), params)
    except :
        conn.rollback()  # Полный откат транзакции
        result = conn.execute(text(merge_query), params)
    #row = result.fetchone()
    #new_record_id = row[0]
    #updated_record_id = row[1] if len(row) > 1 else None
    conn.commit()
    conn.close()
    #return new_record_id,updated_record_id

def update_datum_level(params,new_record_id):
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
    conn.comit()
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

    conn = st.session_state["conn"]
    insert_query = """
        INSERT INTO mzkh_datums (name, code, fullname, id_subsystem, id_datum_type, parent_id, page, id_edizm)
        OUTPUT Inserted.ID
        VALUES (:name, :code, :fullname, :id_subsystem, :id_datum_type, :parent_id, :page, :id_edizm)
    """
    result = conn.execute(text(insert_query), params)
    new_record_id = result.fetchone()[0]
    conn.commit()
    conn.close()
    update_datum_level(params,new_record_id)

def update_datum_dict(params,original_row):    
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

    conn = st.session_state["conn"]
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
    conn.commit()
    conn.close()
    update_datum_level(params,params["id"])
    
def delete_datum(datum_id):
    engine = st.session_state["engine"]
    conn = engine.connect()
    query = "DELETE FROM mzkh_datums WHERE id = :datum_id"
    conn.execute(text(query), {"datum_id": datum_id})
    conn.commit()
    conn.close()
