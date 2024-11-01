import streamlit as st
try:
    import utils.utils as utils
    #import utils.files_db as files_db
    import utils.datum_types_db as datum_types_db
    import utils.subsystems_db as subsystems_db
    import utils.files_db as files_db
    import pprint
    import requests
    import datetime
    import os
except ImportError as e:
    print("Pressed Reload in Browser...")
conn = utils.conn_and_auth_check()
@st.fragment
def ПоказатьЗагруженныеФайлы(datum_id,datum_code,datum_name,files_empty,upl=None):
    def files_df_callback():
        selection_rows =st.session_state.get("event_files_df"+str(datum_id)+"_"+str(st.session_state.uploader_key)).selection.rows
        if len(selection_rows) > 0:        
            selected_row_id = selection_rows[0] 
            selected_item =  files_df.iloc[selected_row_id].to_dict()
            st.session_state.selected_file = selected_item
   
    #------------------------------- тело функции-------------------------------  
    
    files_df = files_db.get_files(datum_id=datum_id)
   
    column_configuration = {
    
    "id": st.column_config.NumberColumn(
        "ИД", 
        help="ИД", 
        width="small",
        disabled=True
    ),
    "name": st.column_config.TextColumn(
        "Имя файла",
        help="Имя файла",
        width="medium",
        required=True       
    ),
    "file_size": st.column_config.NumberColumn(
            "Размер", 
            help="Размер файла",
            width="small",
       ),
    "file_type": st.column_config.TextColumn(
        "Тип",
        help="Тип файла",
        width="small",
        required=True       
    ),
    "user_name": st.column_config.TextColumn(
        "Пользователь",
        help="Пользователь",
        width="medium",
        required=True       
    ),
    "category": st.column_config.TextColumn(
        "Категория",
        help="Категория файла",
        width="medium",
        required=True       
    ),
    "dt": st.column_config.DateColumn(
        "Дата",
        help="Дата загрузки файла",
        width="medium",
        format ='DD.MM.YYYY HH:mm',
        required=True       
    ),
    "id_datum":None
    }      
    event_files_df= st.dataframe(
            files_df,
            column_config=column_configuration,
            use_container_width=True,
            hide_index=True,
            on_select = files_df_callback,
            selection_mode="single-row",
            key="event_files_df"+str(datum_id)+"_"+str(st.session_state.uploader_key)
            )
    if st.session_state.get("selected_file",None):
       # if not st.session_state.get("del_button"+str(st.session_state.get("selected_file"))):
           if st.button(label="Удалить",key="del_button"+str(st.session_state.get("selected_file")['id'])):
                files_db.delete_file(st.session_state.get("selected_file")['id'])        
                del st.session_state.selected_file
                st.session_state.uploader_key += 1 
                with files_empty:
                    ПоказатьЗагруженныеФайлы(datum_id,datum_code,datum_name,files_empty)
                    st.session_state.uploader_key += 1
                    if upl:
                        upl.empty()
                        with upl:    
                            st.info("Для загрузки файлов зайдите  в режим Файлы заново.",icon=":material/help:")
                        
                     
                                            

    
@st.dialog("Файлы Показателя", width="large")    
def ФайлыПоказателя(datum_id,datum_type_id,datum_type_code,datum_code,datum_name):
    #------------------------------- тело функции-------------------------------  
    conn = utils.conn_and_auth_check() 
    if "uploader_key" not in st.session_state:
      st.session_state.uploader_key = 0
    files_container = st.container()
    files_empty = st.empty()
    with files_empty:
        ПоказатьЗагруженныеФайлы(datum_id,datum_code,datum_name,files_empty)
    with files_container:       
        st.header(f"{datum_code} {datum_name}")
           
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
        font-size:0;
        }
        div[data-testid="stFileUploader"]>section[data-testid="stFileUploaderDropzone"]>button[data-testid="stBaseButton-secondary"]::after {
        content: "BUTTON_TEXT"; 
        font-size: initial !important; /* либо нужный вам размер шрифта */
        visibility:visible;
        display: block;
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
    лЗагружалисьФайлы = False
    upl=st.empty()
    with upl:
        uploaded_files = st.file_uploader(label="Отправьте файлы", accept_multiple_files=True, key=f"uploader_{st.session_state.uploader_key}")
   
    for uploaded_file in uploaded_files:
        file_data  = uploaded_file.getvalue()
       
        url = 'http://192.168.10.130:8080/upload'

        # Отправка POST запроса с файлом
        files = {'uploads': (uploaded_file.name, file_data, 'application/octet-stream')}
        data = {'folder': str(datum_id)}
        response = requests.post(url, files=files, data = data)
        
        # Проверка статуса ответа
        if response.status_code == 200:
            
            file_df = files_db.get_file(uploaded_file.name,datum_id)
            
            file_id = file_df["id"][0] if not file_df.empty else None

            file_extension = os.path.splitext(uploaded_file.name)[1]
            params={"id":file_id, 
                    "id_datum":datum_id, 
                    "name":uploaded_file.name, 
                    "file_type":file_extension,
                    "file_size":len(file_data), 
                    "user_name":st.session_state.get("username"), 
                    "category":"Изображение" if file_extension in(".jpeg",".jpg") else "Документ",
                    "dt":datetime.datetime.now()
            }
            files_db.merge_files(conn,params)
            #st.session_state.uploader_key += 1  
            лЗагружалисьФайлы = True          
        else:
            st.write(f"Файл: {uploaded_file.name} был загружен, произошла ошибка записи в хранилище не прошла.({response.status_code})")
    
    if лЗагружалисьФайлы:
        with files_empty:
            st.session_state.uploader_key += 1 
            with upl:
                uploaded_files = st.file_uploader(label="Отправьте файлы", accept_multiple_files=True, key=f"uploader_{st.session_state.uploader_key}")
            ПоказатьЗагруженныеФайлы(datum_id,datum_code,datum_name,files_empty,upl) 
           


 
