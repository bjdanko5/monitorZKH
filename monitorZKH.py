import streamlit as st
import pandas as pd
import pyodbc

def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )
@st.cache_data(ttl=600)
def run_query(query, params=None):
    with conn.cursor() as cur:
        if params:
          cur.execute(query, params)
        else:
          cur.execute(query)
        return cur.fetchall()
def get_regions_dataset() -> pd.DataFrame:  
  rows = run_query("select namespace.NAME, namespace.TYPENAME,ADMHIERARCHY.REGIONCODE FROM ADMHIERARCHY join namespace on ADMHIERARCHY.OBJECTID = namespace.OBJECTID where ADMHIERARCHY.Level = 0 order by ADMHIERARCHY.REGIONCODE")
  return rows
def get_city_raion_dataset(region_code) -> pd.DataFrame:  
  params = (region_code,)
  rows = run_query("select namespace.NAME, namespace.TYPENAME,ADMHIERARCHY.REGIONCODE FROM ADMHIERARCHY join namespace on ADMHIERARCHY.OBJECTID = namespace.OBJECTID where ADMHIERARCHY.Level = 1 and ADMHIERARCHY.REGIONCODE= ? order by ADMHIERARCHY.REGIONCODE", params)
  return rows

conn = init_connection()

def get_region_df() -> pd.DataFrame:  
  regions_dataset = get_regions_dataset()
  st.header("Регионы")
  df = pd.DataFrame(dict(zip(['region_name', 'region_type', 'region_code'], zip(*regions_dataset))))
  column_configuration = {
      "region_name": st.column_config.TextColumn(
         "Регион", help="Наименование региона", max_chars=150, width="large"
     ),
     "region_type": st.column_config.TextColumn(
         "Тип Региона",
         help="Тип Региона",
         width="small",
     ),
     "region_code": st.column_config.TextColumn(
         "Код Региона",
         help="Код Региона",
         width="medium",
     ), 
  }
  event = st.dataframe(
    df,
    column_config=column_configuration,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
  )

  selected_regions = event.selection.rows
  if len(selected_regions) > 0:
   for region in selected_regions:
     filtered_df = df.iloc[region]
     st.header("Районы "+" "+filtered_df["region_name"]+filtered_df["region_type"])
     region_code = filtered_df["region_code"]
     city_raion_dataset = get_city_raion_dataset(region_code)
     df_city_raion = pd.DataFrame(dict(zip(['region_name', 'region_type', 'region_code'], zip(*city_raion_dataset))))
     event = st.dataframe(
     df_city_raion,
     column_config=column_configuration,
     use_container_width=True,
     hide_index=True,
     on_select="rerun",
     selection_mode="single-row",
  )
  else:
     st.markdown("Регион не выбран.")

get_region_df()