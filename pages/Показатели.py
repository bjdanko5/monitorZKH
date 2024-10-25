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
conn = utils.conn_and_auth_check()    
#Основная программа страницы
st.header("Показатели")

if not st.session_state.get("datumsParentStack"):
    st.session_state.datumsParentStack = Stack.DatumsParentStack()

so_container = st.container()
so.ВыборПодсистемы(so_container)

sd_container = st.container()
sd.ВыборПоказателя(sd_container,None)

st.toggle("Редактор Справочник показателя", 
    value=st.session_state.get("mode_edit_spr_datum",False), 
    key="mode_edit_spr_datum", 
    help=None, 
    on_change=None, 
    args=None, 
    kwargs=None, 
    label_visibility="visible")
if st.session_state.mode_edit_spr_datum:
    datums_container = st.container()
    spd.СправочникиПоказателей(datums_container)
else:
    if st.session_state.get("selected_spr_datum_button"):
        del st.session_state.selected_spr_datum_button 
    if st.session_state.get("selected_spr_datum"):    
        del st.session_state.selected_spr_datum

    datums_container = st.container()
    rd.РедакторПоказателей(datums_container)



op_status_container = st.empty()
col1, col2, col3 = st.columns(3)
with col1: 
    if st.button("Обновить"):
       st.rerun() 
utils.setup_op_status(op_status_container,"Редактируйте Показатели и нажмите Обновить")
