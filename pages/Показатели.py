import streamlit as st
try:
    import utils.utils as utils 
    import widgets.ВыборПодсистемы as so
    import widgets.ВыборПоказателя as sd
    import widgets.РедакторПоказателей as rd
    import utils.Stack as Stack
    import widgets.СправочникиПоказателей as spd
    
    import pprint
except ImportError as e:
    print("Pressed Reload in Browser...")
#Основная программа страницы
st.header("Показатели")

if not st.session_state.get("datumsParentStack"):
    st.session_state.datumsParentStack = Stack.DatumsParentStack()

so_container = st.container()
so.ВыборПодсистемы(so_container)

sd_container = st.container()
sd.ВыборПоказателя(sd_container,None)

datums_container = st.container()
rd.РедакторПоказателей(datums_container)

datums_container = st.container()
spd.СправочникиПоказателей(datums_container)


op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Обновить"):
       st.rerun() 
utils.setup_op_status(op_status_container,"Редактируйте Показатели и нажмите Обновить")
