import streamlit as st
try:
    import utils.utils as utils
    import utils.files_db as files_db
    import pprint
    import requests
    import datetime
    import os
except ImportError as e:
    print("Pressed Reload in Browser...")
@st.dialog("Документы Показателя", width="large")    
def Документы(datum_id,datum_type_id,datum_type_code,datum_code,datum_name):
    #------------------------------- тело функции-------------------------------  
    files_df = files_db.get_files_by_category(category="Документ")
    if files_df.empty:
        st.info("Документы Показателя можно загрузить по кнопке Файлы",icon=":material/help:")
        if st.button("Назад"):
            
            st.rerun()
    else:   
        base_url = 'http://192.168.10.130:/mzkh_files'
        for index, row in files_df.iterrows():
            url = base_url+"/"+str(row['id_datum'])+"/"+row['name']        
            Описание = row['name']+" - "+str(row['file_size'] % 1024)+"  KB - "+row['dt'].strftime('%d.%m.%Y %H:%M') 
            st.markdown("### "+"["+Описание+"]("+url+")",unsafe_allow_html=True)
