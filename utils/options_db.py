import streamlit as st
import pandas as pd
from sqlalchemy import text
import numpy as np
def prepare_int(i):
    return i if i is None else int(i)
def get_options(datum_id=None):
    conn = st.session_state["conn"]    
    query = """
            SELECT id
                ,id_datum
                ,name
                ,int_value
                ,float_value
                ,date_value
                ,nvarchar_value
            FROM mzkh_options
            WHERE id_datum = :datum_id
        """
    params = {
        "datum_id": datum_id,
    }
    result = conn.execute(text(query), params)
    rows = result.fetchall() 
    if rows:
        df = pd.DataFrame(rows)
    else:
        columns = ["id",
                   "id_datum",
                   "name",
                   "int_value",
                   "float_value",
                   "date_value",
                   "nvarchar_value"]
        df = pd.DataFrame(columns=columns)
    return df
def add_option_dict(params):
    defaults = {
        "int_value": None,
        "float_value": None,
        "date_value": None,
        "nvarchar_value": None,
    }

    params.update({key: value for key, value in defaults.items() if key not in params})
    params = {
    key: int(value) if isinstance(value, np.int64) 
    else "Не задано" if value in [None, ""] and isinstance(value, str) 
    else value 
    for key, value in params.items()
    }


    conn = st.session_state["conn"]
    insert_query = """
        INSERT INTO mzkh_options (
                   id_datum,
                   name,
                   int_value,
                   float_value,
                   date_value,
                   nvarchar_value)
        OUTPUT Inserted.ID
        VALUES (
                   :id_datum,
                   :name,
                   :int_value,
                   :float_value,
                   :date_value,
                   :nvarchar_value)
    """
    result = conn.execute(text(insert_query), params)
    new_record_id = result.fetchone()[0]
    #update_option_level(conn,params,new_record_id)
    conn.commit()

def update_option_dict(params,original_row):    
 
    params.update({key: value for key, value in original_row.items() if key not in params})
    #params.pop("subsystem_name", None)
    #params.pop("option_type_name", None)
 
    params = {
    key: int(value) if isinstance(value, np.int64) 
    else "Не задано" if value in [None, ""] and isinstance(value, str) 
    else value 
    for key, value in params.items()
    }
   
    conn = st.session_state["conn"]
    query = """
        UPDATE mzkh_options
        SET
            id_datum = :id_datum,
            name = :name,
            int_value = :int_value,
            float_value = :float_value,
            date_value = :date_value,
            nvarchar_value = :nvarchar_value
        WHERE id = :id
    """
    conn.execute(text(query), params)
    #update_option_level(conn,params,params["id"])
    conn.commit()
def delete_option(option_id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_options WHERE id = :option_id"
    conn.execute(text(query), {"option_id": option_id})
    conn.commit()
   
