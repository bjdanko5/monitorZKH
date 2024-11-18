import streamlit as st
import hmac
#try:
import utils.utils as utils   
import utils.users_db as users_db
from logtail import LogtailHandler
import logging

handler = LogtailHandler(source_token="HuXAzztxnhkthASvbRxaZv2a")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(handler)
#except ImportError as e:
#       print("Pressed Reload in Browser...")

#

st.title("Мониторинг ЖКХ")
def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
 
        with st.form("Credentials"):
            st.text_input("Пользователь", key="username")
            st.text_input("Пароль", type="password", key="password")
            st.form_submit_button("Войти", on_click=password_entered, type="primary", use_container_width=True)

    def password_entered():
        """Checks whether a password entered by the user is correct."""     
        conn = utils.get_conn_status()
        user_df = users_db.get_user_by_name(st.session_state["username"])
        if not user_df.empty and st.session_state["password"] == str(user_df["password"][0]):
          
        #if not user_df.empty and hmac.compare_digest(
        #    st.session_state["password"],
        #    str(user_df["password"][0]),
        #):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            #del st.session_state["username"]
            st.session_state["username"] =  st.session_state["username"]
    
    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False) and "username" in st.session_state:
        logger.info("Вход разрешен: " + st.session_state["username"]) 
        return True

    # Show inputs for username + password.
    login_form()
  
if not check_password():
    logger.info("Не авторизован: " + st.session_state["username"]) 
    #st.rerun()  
else:
    logger.info("Авторизован: " + st.session_state["username"]) 
    
# Main Streamlit app starts here
st.info("Выберите необходимое действие на навигационной панели...",icon=":material/help:")
#utils.auth_check()
