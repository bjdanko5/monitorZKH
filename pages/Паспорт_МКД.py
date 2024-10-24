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
    st.session_state.id_Вкладка = stx.tab_bar(data=data, default=int(df_Вкладки["id"][0]))

    st.info(f"{st.session_state.id_Вкладка=}")
    if st.session_state.id_Вкладка==1: 
        datums_df = datums_db.get_datums(subsystem_id = st.session_state.selected_subsystem_id,
                                     datum_lvl=1,datum_id_lvl=st.session_state.id_Вкладка)
        datums_df 
    if st.session_state.id_Вкладка==5: 
        datums_df = datums_db.get_datums(subsystem_id = st.session_state.selected_subsystem_id,
                                     datum_lvl=1,datum_id_lvl=st.session_state.id_Вкладка) 
        datums_df
    #tabs = st.tabs(df_Вкладки['name'].tolist())

    # Iterate over the tabs and display the content for each tab
    #for tab, row in zip(tabs, df_Вкладки.itertuples()):
    #    with tab:
    #        st.subheader(row.fullname)
