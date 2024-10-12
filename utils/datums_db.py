import streamlit as st
import pandas as pd
from sqlalchemy import text
def prepare_int(i):
    return i if i is None else int(i)

def get_datums(subsystem_name=None, subsystem_id=None, subsystem_code=None, datum_parent_id=None):
    conn = st.session_state["conn"]
    
    query = """
        SELECT d.*, s.name AS subsystem_name, dt.name AS datum_type_name
        FROM mzkh_datums d
        LEFT JOIN mzkh_subsystems s ON d.id_subsystem = s.id
        LEFT JOIN mzkh_datum_types dt ON d.id_datum_type = dt.id
        WHERE (:subsystem_name IS NULL OR s.name = :subsystem_name)
        AND (:subsystem_id IS NULL OR s.id = :subsystem_id)
        AND (:subsystem_code IS NULL OR s.code = :subsystem_code)
        AND (:datum_parent_id IS NULL OR parent_id = :datum_parent_id)
        ORDER BY d.name
    """
    
    params = {
        "subsystem_name": subsystem_name,
        "subsystem_id": prepare_int(subsystem_id),
        "subsystem_code": subsystem_code,
        "datum_parent_id": prepare_int(datum_parent_id)
    }
    
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    
    if rows:
        df = pd.DataFrame(rows)
    else:
        columns = ['id', 'name', 'id_subsystem', 'subsystem_name', 'id_datum_type', 'datum_type_name', "code", "fullname", "parent_id", "page", "id_edizm"]
        df = pd.DataFrame(columns=columns)
    
    return df
def add_datum(name, code, fullname, id_subsystem, id_datum_type, parent_id,id_edizm):
    page = "pages/" + code + ".py"
    conn = st.session_state["conn"]
    query = """
        INSERT INTO mzkh_datums (name, code, fullname, id_subsystem, id_datum_type, parent_id, page, id_edizm)
        VALUES (:name, :code, :fullname, :id_subsystem, :id_datum_type, :parent_id, :page, :id_edizm)
    """
    params = {
        "name": name,
        "code": code,
        "fullname": fullname,
        "id_subsystem": prepare_int(id_subsystem),
        "id_datum_type":prepare_int(id_datum_type),
        "parent_id": prepare_int(parent_id),
        "page": page,
        "id_edizm": prepare_int(id_edizm)
    }
    conn.execute(text(query), params)
    conn.commit()
def update_datum(datum_id, name, code, fullname, id_subsystem, id_datum_type, parent_id, id_edizm):
    page = "pages/" + code + ".py"
    conn = st.session_state["conn"]
    query = """
        UPDATE mzkh_datums
        SET name = :name, code = :code, fullname = :fullname, id_subsystem = :id_subsystem,
            id_datum_type = :id_datum_type, parent_id = :parent_id, page = :page, id_edizm = :id_edizm
        WHERE id = :datum_id
    """
    params = {
        "name": name,
        "code": code,
        "fullname": fullname,
        "id_subsystem": prepare_int(id_subsystem),
        "id_datum_type": prepare_int(id_datum_type),
        "parent_id": prepare_int(parent_id),
        "page": "pages/" + code + ".py",
        "id_edizm": prepare_int(id_edizm),
        "datum_id": prepare_int(datum_id)
    }
    conn.execute(text(query), params)
    conn.commit()
def delete_datum(datum_id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_datums WHERE id = :datum_id"
    conn.execute(text(query), {"datum_id": datum_id})
    conn.commit()
   
