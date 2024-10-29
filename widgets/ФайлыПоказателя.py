import streamlit as st
try:
    import utils.utils as utils
    #import utils.files_db as files_db
    import utils.datum_types_db as datum_types_db
    import utils.subsystems_db as subsystems_db
    import pprint
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
@st.dialog("Файлы Показателя")    
def ФайлыПоказателя(datum_id,datum_type_id,datum_type_code,datum_code,datum_name):
    languages = {
    "RU": {
        "button": "Отправить",
        "instructions": "Перетащите файлы сюда",
        "limits": "Лимит 2MB на Файл",
    },
    }
    #lang = st.radio("", options=["RU", "ES"], horizontal=True)
    lang ="RU"

    hide_label = (
    """
    <style>
        div[data-testid="stFileUploader"]>section[data-testid="stFileUploaderDropzone"]>button[data-testid="stBaseButton-secondary"] {
        color:white;
       
        }
        div[data-testid="stFileUploader"]>section[data-testid="stFileUploaderDropzone"]>button[data-testid="stBaseButton-secondary"]::after {
            content: "BUTTON_TEXT";
            color:black;
            display: block;
            position: absolute;
        }
        div[data-testid="stFileUploaderDropzoneInstructions"]>div>span {
        visibility:hidden;
        }
        div[data-testid="stFileUploaderDropzoneInstructions"]>div>span::after {
        content:"INSTRUCTIONS_TEXT";
        visibility:visible;
        display:block;
        }
        div[data-testid="stFileUploaderDropzoneInstructions"]>div>small {
        visibility:hidden;
        }
        div[data-testid="stFileUploaderDropzoneInstructions"]>div>small::before {
        content:"FILE_LIMITS";
        visibility:visible;
        display:block;
        }
    </style>
    """.replace(
            "BUTTON_TEXT", languages.get(lang).get("button")
        )
        .replace("INSTRUCTIONS_TEXT", languages.get(lang).get("instructions"))
        .replace("FILE_LIMITS", languages.get(lang).get("limits"))
    )

    st.markdown(hide_label, unsafe_allow_html=True)

    file_uploader = st.file_uploader(label="Отправьте файлы")

  
    #------------------------------- тело функции-------------------------------  
#Основная программа
conn = utils.conn_and_auth_check() 
options_container = st.container()
#ФайлыПоказателя(options_container)
 
