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

#for tag, value in tagged_params_dict.items():
#sh_container = st.container()
#params={"level":0,"parentobjid":0}
#sh.ПоискДома(sh_container,params)
#selected_hierarchy_tag = str(params["level"])+"_"+str(params["parentobjid"])
#if "tagged_params_dict" in st.session_state:
#    if st.session_state["tagged_params_dict"].get(selected_hierarchy_tag) is not None:
#        if "params" in st.session_state["tagged_params_dict"][selected_hierarchy_tag]:
#            parentobjid = st.session_state.tagged_params_dict[selected_hierarchy_tag]["params"]["objectid"]
#            selected_hierarchy_tag = str(params["level"])+"_"+str(parentobjid)  
#            params={"level":params["level"]+1,"parentobjid":parentobjid}
#            sh_container1 = st.container()
#            sh.ПоискДома(sh_container1,params)
