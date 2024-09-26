import streamlit as st
import pandas as pd
import pyodbc

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
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
# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
conn = init_connection()
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("select namespace.NAME, namespace.TYPENAME,ADMHIERARCHY.REGIONCODE FROM ADMHIERARCHY join namespace on ADMHIERARCHY.OBJECTID = namespace.OBJECTID where ADMHIERARCHY.Level = 0 order by ADMHIERARCHY.REGIONCODE")

# Print results.
#for row in rows:
#    st.write(f"{row[0]} has a :{row[1]}:")
#
#st.write("Hello world")
#df = pd.DataFrame(rows, columns=['NAME', 'TYPENAME', 'REGIONCODE'])
df = pd.DataFrame(rows)

# print(len(rows))
# print(rows[0])
#df.columns = ['NAME', 'TYPENAME', 'REGIONCODE']

# df = pd.DataFrame({
#     'NAME': [row[0] for row in rows],
#     'TYPENAME': [row[1] for row in rows],
#     'REGIONCODE': [row[2] for row in rows]
#})

#df = pd.DataFrame(dict(zip(['NAME', 'TYPENAME', 'REGIONCODE'], zip(*rows))))
st.header("Регионы")
df = pd.DataFrame(dict(zip(['Регион', 'Тип Региона', 'Код Региона'], zip(*rows))))
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
st.header("Выбранный Регион")
selected_regions = event.selection.rows
if len(selected_regions) > 0:
  for region in selected_regions:
    filtered_df = df.iloc[region]
    st.dataframe( filtered_df,
        column_config=column_configuration,
        use_container_width=True,)
else:
    st.markdown("Регион не выбран.")