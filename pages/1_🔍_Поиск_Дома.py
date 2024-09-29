import streamlit as st
import pandas as pd
import pyodbc
import utils.utils as utils
import time
utils.auth_check()
with st.status("Устанавливается подключение к базе данных...", state="running", expanded=True) as status:
    st.write("Ожидайте...")
    st.session_state["conn"] = utils.init_connection()
    if st.session_state.get("conn") is None:
        del st.session_state["password_correct"]
        status.update(label="Не удалось подключиться к базе данных.",state="error", expanded=True)
        st.write("Выполнен Выход пользователя из Монитора ЖКХ.")   
        if st.button("Войти ещё раз"):
            st.switch_page("Монитор_ЖКХ.py") 
        st.stop()   
    else:        
        conn = st.session_state["conn"]
        status.update(label="Подключение к базе данных выполнено.",state="complete", expanded=True)   
        st.write("Можно работать...")
time.sleep (5)       
status.update(label="БД подключена",state="complete", expanded=False)           

        


def get_regions_dataset() -> pd.DataFrame:  
  rows = utils.run_query("""
      SELECT 
          namespace.NAME, 
          namespace.TYPENAME, 
          ADMHIERARCHY.REGIONCODE
      FROM 
          ADMHIERARCHY
      JOIN 
          namespace
      ON 
          ADMHIERARCHY.OBJECTID = namespace.OBJECTID
      WHERE 
          ADMHIERARCHY.Level = 0
      ORDER BY 
          ADMHIERARCHY.REGIONCODE
  """)
  return rows
def get_city_raion_dataset(region_code) -> pd.DataFrame:  
  params = (utils.alltrim(region_code),)
  rows = utils.run_query("""
      SELECT
          namespace.NAME,
          namespace.TYPENAME,
          IIF(ADMHIERARCHY.AREACODE > ADMHIERARCHY.CITYCODE, ADMHIERARCHY.AREACODE, ADMHIERARCHY.CITYCODE),
          ADMHIERARCHY.REGIONCODE,
          IIF(ADMHIERARCHY.CITYCODE = 0, 0, 1)
      FROM
          ADMHIERARCHY
      JOIN
          namespace
      ON
          ADMHIERARCHY.OBJECTID = namespace.OBJECTID
      WHERE
          ADMHIERARCHY.Level = 1
          AND ADMHIERARCHY.REGIONCODE = ?
      ORDER BY
          ADMHIERARCHY.REGIONCODE
  """, params)
  return rows
def get_city_dataset(region_code,city_raion_code) -> pd.DataFrame:  
  params = (utils.alltrim(region_code),utils.alltrim(city_raion_code),)
  rows = utils.run_query("""
      SELECT
          namespace.NAME,
          namespace.TYPENAME,
          IIF(ADMHIERARCHY.CITYCODE > ADMHIERARCHY.PLACECODE, ADMHIERARCHY.CITYCODE, ADMHIERARCHY.PLACECODE),
          IIF(ADMHIERARCHY.AREACODE > ADMHIERARCHY.CITYCODE, ADMHIERARCHY.AREACODE, ADMHIERARCHY.CITYCODE),
          ADMHIERARCHY.REGIONCODE
      FROM
          ADMHIERARCHY
      JOIN
          namespace
      ON
          ADMHIERARCHY.OBJECTID = namespace.OBJECTID
      WHERE
          ADMHIERARCHY.Level = 2
          AND ADMHIERARCHY.REGIONCODE = ?
          AND IIF(ADMHIERARCHY.AREACODE > ADMHIERARCHY.CITYCODE, ADMHIERARCHY.AREACODE, ADMHIERARCHY.CITYCODE) = ?
      ORDER BY
          ADMHIERARCHY.REGIONCODE
  """, params)
  return rows

def get_region_df() -> pd.DataFrame:  

  regions_dataset = get_regions_dataset()
  if regions_dataset is None:
      df = pd.DataFrame(columns=['region_name', 'region_type', 'region_code'])
      st.markdown ("Не удалось подключиться к базе данных.")
  else:
      df = pd.DataFrame(dict(zip(['region_name', 'region_type', 'region_code'], zip(*regions_dataset))))
  column_configuration = {
     "region_name": st.column_config.TextColumn(
         "Регион", help="Наименование региона", max_chars=150, width="large"
     ),
     "region_type": st.column_config.TextColumn(
         "Тип Региона",
         help="Тип Региона",
         width="medium"
     ),
     "region_code": st.column_config.TextColumn(
         "Код Региона",
         help="Код Региона",
         width="small"
     ), 
  }
  return df, column_configuration
def get_city_raion_df(df_region,selected_regions ) -> pd.DataFrame:
  region_name = ""
  region_type = ""   
  for region in selected_regions:
     filtered_df = df_region.iloc[region]

     region_code = filtered_df["region_code"]
     region_name = filtered_df["region_name"]
     region_type = filtered_df["region_type"] 
     city_raion_dataset = get_city_raion_dataset(region_code)
  
     if city_raion_dataset is None: 
      df_city_raion = pd.DataFrame(columns=['city_raion_name', 'city_raion_type', 'city_raion_code', 'region_code','is_city']) 
     else:  
      df_city_raion = pd.DataFrame(dict(zip(['city_raion_name', 'city_raion_type', 'city_raion_code', 'region_code','is_city'], zip(*city_raion_dataset))))
     
  column_configuration = {
     "city_raion_name": st.column_config.TextColumn(
         "Район / Город", help="Наименование Район / Город", max_chars=150, width="large"
     ),
     "city_raion_type": st.column_config.TextColumn(
         "Тип Район / Город",
         help="Тип Район / Город",
         width="medium"
         
     ),
     "city_raion_code": st.column_config.TextColumn(
         "Код Район / Город",
         help="Район / Город",
         width="small"       
     ), 
     "region_code": st.column_config.TextColumn(
         "Код Региона",
         help="Код Региона",
         width="small"
     ), 
     "is_city": st.column_config.NumberColumn(
         "Это Город",
         help="Это Город",
         width="small"
     ), 

    }
  return df_city_raion, column_configuration,region_name,region_type
def get_city_df(df_city_raion,selected_city_raion ) -> pd.DataFrame:
  city_raion_name = ""
  city_raion_type = ""
  for city_raion in selected_city_raion:
     filtered_df = df_city_raion.iloc[city_raion]

     city_raion_code = filtered_df["city_raion_code"]
     city_raion_name = filtered_df["city_raion_name"]
     city_raion_type = filtered_df["city_raion_type"]   
     is_city         = filtered_df["is_city"]   
     region_code     = filtered_df["region_code"]   
     if is_city == 0: 
      city_dataset = get_city_dataset(region_code,city_raion_code)
      df_city = pd.DataFrame(dict(zip(['city_name', 'city_type', 'city_code','city_raion_code','region_code'], zip(*city_dataset))))
     else:
      df_city = pd.DataFrame(columns=['city_name', 'city_type', 'city_code', 'city_raion_code', 'region_code'])
      
        
  column_configuration = {
      "city_name": st.column_config.TextColumn(
         "Населенный пункт", help="Населенный пункт", max_chars=150, width="large"
     ),
     "city_type": st.column_config.TextColumn(
         "Тип НП",
         help="Тип НП",
         width="medium"
         
     ),
     "city_code": st.column_config.TextColumn(
         "Код НП",
         help="Код НП",
         width="small"
         
     ), 
     "city_raion_code": st.column_config.TextColumn(
         "Код Район / Город",
         help="Район / Город",
         width="small"       
     ), 
     "region_code": st.column_config.TextColumn(
         "Код Региона",
         help="Код Региона",
         width="small"
     ), 

    }
  return df_city,column_configuration,city_raion_name,city_raion_type
def is_city( selected_city_raion) -> bool:
  for city_raion in selected_city_raion:
     filtered_df = df_city_raion.iloc[city_raion]
     is_city         = filtered_df["is_city"]   
     return (is_city==1)

#conn = utils.init_connection()
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

  if len(selected_city_raion) > 0 and not is_city(selected_city_raion): 
    df_city,column_configuration,city_raion_name,city_raion_type = get_city_df(df_city_raion,selected_city_raion )
    st.header("Населенные пункты района " +  " " + city_raion_name + " " + city_raion_type)
    event_df_city = st.dataframe(
      df_city,
      column_config=column_configuration,
      use_container_width=True,
      hide_index=True,
      on_select="rerun",
      selection_mode="single-row",
    )
    selected_city = event_df_city.selection.rows
    if len(selected_city) > 0:
      st.markdown("Населенный пункт в районе выбран.") 
    else:  
      st.markdown("Населенный пункт в районе не выбран.")

