import streamlit as st
import pandas as pd
from sqlalchemy import text 
def get_user_by_name(name):
    conn = st.session_state["conn"]
    query = """
    SELECT 
    u.id,
    u.name,
    u.fullname,
    u.password,
    r.id AS role_id,
    r.name AS role_name,
    o.id AS org_id,
    o.name AS org_name
    FROM 
    mzkh_users u
    LEFT JOIN mzkh_roles r
        ON u.id_role = r.id
    LEFT JOIN mzkh_orgs o
        ON u.id_org = o.id
    WHERE 
    r.target = 'Пользователь'
    AND u.name = :name
    ORDER BY 
    u.name
    """
    params = {"name": name}
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=['id', 'name','fullname', 'password', 'role_id', 'role_name', 'org_id', 'org_name'])
    return df
def get_users_by_org_id(org_id):
    conn = st.session_state["conn"]
    query = """
    SELECT 
        u.id,
    u.name,
    u.fullname,
    u.password,

    r.id AS role_id,
    r.name AS role_name,
    o.id AS org_id,
    o.name AS org_name
    FROM 
    mzkh_users u
    LEFT JOIN mzkh_roles r
        ON u.id_role = r.id
    LEFT JOIN mzkh_orgs o
        ON u.id_org = o.id
    WHERE 
    r.target = 'Пользователь'
    AND o.id = :org_id
    ORDER BY 
    u.name
    """
    params = {"org_id": int(org_id)}
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=['id', 'name','fullname', 'password', 'role_id', 'role_name', 'org_id', 'org_name'])
    return df

def get_user_by_id(id):
    conn = st.session_state["conn"]
    query = """
    SELECT 
        u.id,
    u.name,
    u.fullname,
    u.password,

    r.id AS role_id,
    r.name AS role_name,
    o.id AS org_id,
    o.name AS org_name
    FROM 
    mzkh_users u
    LEFT JOIN mzkh_roles r
        ON u.id_role = r.id
    LEFT JOIN mzkh_orgs o
        ON u.id_org = o.id
    WHERE 
    r.target = 'Пользователь'
    AND u.id = :id
    ORDER BY 
    u.name
    """
    params = {"id": id}
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=['id', 'name','fullname', 'password', 'role_id', 'role_name', 'org_id', 'org_name'])
    return df

def get_users(role_name = None):
    conn = st.session_state["conn"]
    if  role_name:
        query = """
        SELECT 
            u.id,
    u.name,
    u.fullname,
    u.password,

        r.id AS role_id,
        r.name AS role_name,
        o.id AS org_id,
        o.name AS org_name
        FROM 
        mzkh_users u
        LEFT JOIN mzkh_roles r
            ON u.id_role = r.id
        LEFT JOIN mzkh_orgs o
            ON u.id_org = o.id
        WHERE 
        r.target = 'Пользователь'
        AND r.name = :role_name
        ORDER BY 
        u.name
        """
        params = {"role_name": role_name}
    else:
        query = """
        SELECT 
            u.id,
    u.name,
    u.fullname,
    u.password,

        r.id AS role_id,
        r.name AS role_name,
        o.id AS org_id,
        o.name AS org_name
        FROM 
        mzkh_users u
        LEFT JOIN mzkh_roles r
            ON u.id_role = r.id
        LEFT JOIN mzkh_orgs o
            ON u.id_org = o.id
        WHERE 
        r.target = 'Пользователь'
        ORDER BY 
        u.name
        """
        params = {}  
    result = conn.execute(text(query), params)
    rows = result.fetchall()
    if rows: 
        df = pd.DataFrame(rows)
    else:  
        df = pd.DataFrame(columns=['id', 'name','fullname', 'password', 'role_id', 'role_name', 'org_id', 'org_name'])
    return df

def add_user(name,fullname, password, id_role,id_org):
    conn = st.session_state["conn"]
    query = "INSERT INTO mzkh_users (name,fullname,password,id_role,id_org) VALUES (:name, :fullname, :password, :id_role, :id_org)"
    conn.execute(text(query), {"name":name,"fullname": fullname,"password": password, "id_role": id_role, "id_org": id_org})
    conn.commit()
def update_user(id, name,fullname, password, id_role,id_org):
    conn = st.session_state["conn"]
    query = "UPDATE mzkh_users SET name = :name, fullname = :fullname, password = :password, id_role = :id_role, id_org = :id_org WHERE id = :id"
    conn.execute(text(query), {"id": id,"name": name,"fullname": fullname,"password": password, "id_role": id_role, "id_org": id_org})    
    conn.commit()
def delete_user(id):
    conn = st.session_state["conn"]
    query = "DELETE FROM mzkh_users WHERE id = :id"
    conn.execute(text(query), {"id": id})
    conn.commit()
   
