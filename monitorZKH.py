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
def get_region_df() -> pd.DataFrame:  
  regions_dataset = get_regions_dataset()
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
  return df, column_configuration
def get_city_raion_df(df_region,selected_regions ) -> pd.DataFrame:
  for region in selected_regions:
     filtered_df = df_region.iloc[region]

     region_code = filtered_df["region_code"]
     region_name = filtered_df["region_name"]
     region_type = filtered_df["region_tyoe"]   

     city_raion_dataset = get_city_raion_dataset(region_code)
     
     df_city_raion = pd.DataFrame(dict(zip(['region_name', 'region_type', 'region_code'], zip(*city_raion_dataset))))
     
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
  return df_city_raion, column_configuration,region_name,region_type
conn = init_connection()

st.header("Регионы")
df_region,column_configuration = get_region_df()

event_df_region = st.dataframe(
    df_region,
    column_config=column_configuration,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
  )

selected_regions = event_df_region.selection.rows

if len(selected_regions) > 0:
  df_city_raion, column_configuration,region_name,region_type= get_city_raion_df(df_region,selected_regions )
  
  st.header("Районы или города регионального значения " +  " " + region_name + " " + region_type)
  
  event_df_city_raion = st.dataframe(
    df_city_raion,
    column_config=column_configuration,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
  )
  selected_city_raion = event_df_city_raion.selection.rows
  if len(selected_city_raion) > 0:
    st.markdown("Район " + " " + selected_city_raion[0]["region_name"] + " " + selected_city_raion[0]["region_type"])
  else:  
    st.markdown("Район или город не выбран.")

