import streamlit as st
import pandas as pd
from sqlalchemy import text
import numpy as np
def prepare_int(i):
    return i if i is None else int(i)

def get_value_field_name_for_datum_type(datum_type_code):
    if datum_type_code in("int","option_int"):
        value_field_name = 'int_value' 
    elif datum_type_code in ("string","option_string"):
        value_field_name ='nvarchar_value'
    elif datum_type_code  in ("float","option_float"):
       value_field_name ='float_value' 
    elif datum_type_code in ("date","option_date"):   
        value_field_name ='date_value' 
    elif datum_type_code in ("bool","option_bool"):   
        value_field_name = 'int_value'  
    return value_field_name 

def get_typed_options(value_for_datum_type,datum_id,datum_type_code):
    value_field_name = get_value_field_name_for_datum_type(datum_type_code)
    options_df = get_options(datum_id)
    typed_options = options_df[value_field_name]

    value_indexes = typed_options.index[typed_options == value_for_datum_type].tolist()

    value_index = value_indexes[0] if len(value_indexes)>0 else None

    return value_index,typed_options

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
            ORDER BY name
        """
    params = {
        "datum_id": prepare_int(datum_id),
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
    params.pop("bool_value", None)
    
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
        VALUES (
                   :id_datum,
                   :name,
                   :int_value,
                   :float_value,
                   :date_value,
                   :nvarchar_value)
        RETURNING id;           
    """
    result = conn.execute(text(insert_query), params)
    new_record_id = result.fetchone()[0]
    #update_option_level(conn,params,new_record_id)
    conn.commit()

def update_option_dict(params,original_row):    
    params.pop("bool_value", None)
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
   
