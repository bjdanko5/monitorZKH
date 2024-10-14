import streamlit as st
try:
    import utils.utils as utils
    import utils.Поиск_Дома_db as hierarchy_db
    import utils.datums_db as datums_db
    import utils.subsystems_db as subsystems_db
    import widgets.ЗаголовокПодсистемы as ЗаголовокПодсистемы
except ImportError as e:
    print("Pressed Reload in Browser...")

conn = utils.conn_and_auth_check()

ЗаголовокПодсистемы.ЗаголовокПодсистемы("Паспорт МКД")
Вкладки_container = st.container()
with Вкладки_container:
    subsystem_code = "Паспорт_МКД"
    st.session_state.selected_subsystem_id = int(subsystems_db.get_subsystem_by_code(subsystem_code=subsystem_code)["id"][0])
    df_Вкладки = datums_db.get_datums_Вкладки(subsystem_id = st.session_state.selected_subsystem_id)

    #Create the tabs
    tabs = st.tabs(df_Вкладки['name'].tolist())

    # Iterate over the tabs and display the content for each tab
    for tab, row in zip(tabs, df_Вкладки.itertuples()):
        with tab:
            st.subheader(row.fullname)
