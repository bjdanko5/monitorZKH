import streamlit as st
try:
    import utils.utils as utils
    import utils.Поиск_Дома_db as hierarchy_db
    import utils.datums_db as datums_db
    import utils.subsystems_db as subsystems_db
    import widgets.ЗаголовокПодсистемы as ЗаголовокПодсистемы
    import extra_streamlit_components as stx  
except ImportError as e:
    print("Pressed Reload in Browser...")

conn = utils.conn_and_auth_check()

ЗаголовокПодсистемы.ЗаголовокПодсистемы("Паспорт МКД")
Вкладки_container = st.container()
with Вкладки_container:
    subsystem_code = "Паспорт_МКД"
    st.session_state.selected_subsystem_id = int(subsystems_db.get_subsystem_by_code(subsystem_code=subsystem_code)["id"][0])
    st.session_state.selected_subsystem_name = subsystems_db.get_subsystem_by_code(subsystem_code=subsystem_code)["name"][0]
    df_Вкладки = datums_db.get_datums_Вкладки(subsystem_id = st.session_state.selected_subsystem_id)
    data = [
    stx.TabBarItemData(id=int(row['id']), title=row['name'], description=row['fullname'])
    for index, row in df_Вкладки.iterrows()
    ]
    st.session_state.id_Вкладка =int(stx.tab_bar(data=data, default=int(df_Вкладки["id"][0])))

    #st.info(f"{st.session_state.id_Вкладка=}")
    datums_df = datums_db.get_datums(subsystem_id = st.session_state.selected_subsystem_id,
                                     datum_lvl=0,datum_id_lvl=st.session_state.id_Вкладка,mode='all')
    if not datums_df.empty:
            datums_df 
    columns_to_print = ['id', 'name', 'code']

   
    
        
   

    for index, row in datums_df.iterrows():
        #for column in columns_to_print:
        spaces = '&nbsp;&nbsp;' * int(row['lvl']*4)
        if row['lvl'] == 1:
            c = st.container()
            col1, col2, col3 = st.columns([0.01,0.6,0.3])
            with c:
                with col1: 
                    #st.checkbox("", value=False, key=row['code'])
                    pass
                with col2: 
                    st.markdown(f"  ### {spaces} {row['code']} {row['name']}", unsafe_allow_html=True)    
                with col3:
                    st.page_link("pages/Показатели.py", label=f"Изменить", icon=":material/assignment_ind:")
        else:
            c = st.container()
            col1, col2, col3 = st.columns([0.01,0.6,0.3])
            
            with c:
                with col1: 
                    pass
                    #st.checkbox("", value=False, key=row['code'])
                with col2: 
                    st.markdown(f"  ### {spaces} {row['code']} {row['name']}", unsafe_allow_html=True)    
                with col3:
                    st.page_link("pages/Показатели.py", label=f"Изменить", icon=":material/assignment_ind:")
  
 
               #st.button("Изменить", 
                #key=row['code'],
                #help=None, 
                #on_click=None, 
                #args=None,
                #kwargs=None, 
                #type="secondary", 
                #disabled=False, 
                #use_container_width=False)
 
                #st.markdown(f"{spaces}{row['code']} {row['name']}", unsafe_allow_html=True)    
            
