import streamlit as st

import utils.utils as utils
import widgets.ПоискДома as sh

conn = utils.conn_and_auth_check()
header_container = st.empty()
header_container.header("Поиск Дома")

if st.session_state.get("tagged_params_dict") is None:
            st.session_state.tagged_params_dict={}
tagged_params_dict = st.session_state.tagged_params_dict       
num_levels = len(tagged_params_dict)+1 
for level in range(num_levels):
    if level == 0: 
        parentobjid = 0
    else:
        parentobjid = tagged_params_dict[str(level-1)]["params"]["objectid"]    
    params={"level":level,"parentobjid":parentobjid}
    sh_container = st.container()
    sh.ПоискДома(sh_container,params)

