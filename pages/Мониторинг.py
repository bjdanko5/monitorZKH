import streamlit as st
try:
    import utils.utils as utils
    import utils.Поиск_Дома_db as hierarchy_db
    import utils.datum_values_db as datum_values_db
    import utils.datums_db as datums_db
    import utils.options_db as options_db
    import utils.subsystems_db as subsystems_db
    import widgets.ЗаголовокПодсистемы as ЗаголовокПодсистемы
    import widgets.ВыборИзСправочника as ВыборИзСправочника
    import extra_streamlit_components as stx 
    import widgets.ФайлыПоказателя as ФайлыПоказателя
    import widgets.Изображения as Изображения
    import widgets.Документы as Документы
except ImportError as e:
    print("Pressed Reload in Browser...")
def get_value_for_datum_type(row,datum_type_code = None):
    datum_type_code = row['datum_type_code'] if datum_type_code == None else datum_type_code
    if datum_type_code in("int","option_int"):
        datum_value = row['int_value'] 
    elif datum_type_code in ("string","option_string"):
        datum_value = row['nvarchar_value'] 
    elif datum_type_code  in ("float","option_float"):
       datum_value = row['float_value'] 
    elif datum_type_code in ("date","option_date"):   
        datum_value = row['date_value'] 
    elif datum_type_code in ("bool","option_bool"):   
        datum_value = row['int_value']  
    return datum_value    

def datum_values_callback(**datum_values_row):
    #print(datum_values_row)
    datum_value = st.session_state.get("datum_value_"+str(datum_values_row['id']),None)
    if datum_values_row['datum_type_code'] in("int","option_int"):
       datum_values_row['int_value'] = datum_value
    elif datum_values_row['datum_type_code'] in ("string","option_string"):
       datum_values_row['nvarchar_value'] = datum_value    
    elif datum_values_row['datum_type_code'] in ("float","option_float"):
       datum_values_row['float_value'] = datum_value 
    elif datum_values_row['datum_type_code'] in ("date","option_date"):   
        datum_values_row['date_value'] = datum_value 
    elif datum_values_row['datum_type_code'] in ("bool","option_bool"):   
        datum_values_row['int_value'] = datum_value 
    datum_values_row['id_houses_objectid']=st.session_state.get("selected_house_objectid")  
    datum_values_db.merge_datum_values_values(conn,datum_values_row)
    pass
def get_formatted_edizm(row):
    if row['edizm_name']:
        if row['edizm_name'].strip() == "" or str(row['edizm_name']).strip() =="Тип не указан":
            return ""
        else:
            return "<br> :green["+row['edizm_name']+"]"
def custom_sort(item, saved_Вкладка):
    if item.id == saved_Вкладка:
        return 0  # Первый элемент, если id совпадает
    else:
        return 1  # Остальные элементы

conn = utils.conn_and_auth_check()

ЗаголовокПодсистемы.ЗаголовокПодсистемы()
Вкладки_container = st.container()
with Вкладки_container:
    if st.session_state.get("selected_Подсистема",None):
        st.session_state.selected_subsystem_id = st.session_state.selected_Подсистема
    else:    
        if st.session_state.get("saved_Подсистема",None):
            st.session_state.selected_subsystem_id = st.session_state.saved_Подсистема

    
    #subsystem_code = "Паспорт_МКД"
    #st.session_state.selected_subsystem_id = int(subsystems_db.get_subsystem_by_code(subsystem_code=subsystem_code)["id"][0])
    #st.session_state.selected_subsystem_name = subsystems_db.get_subsystem_by_code(subsystem_code=subsystem_code)["name"][0]
    subsystem_id = st.session_state.get("selected_subsystem_id",None)

        
    df_Вкладки = datums_db.get_datums_Вкладки(subsystem_id = subsystem_id)
    if df_Вкладки.empty:          
        if st.session_state.get("saved_Вкладка",None):
            del st.session_state.saved_Вкладка 
        if st.session_state.get("selected_Вкладка",None):
            del st.session_state.selected_Вкладка
    else:    
        data = [
        stx.TabBarItemData(id=int(row['id']), title=row['fullname'], description='Раздел')
        for index, row in df_Вкладки.iterrows()
        ]
        
        saved_Вкладка = st.session_state.saved_Вкладка if 'saved_Вкладка' in st.session_state else None
        data = sorted(data, key=lambda x: custom_sort(x, saved_Вкладка))
        
        col1, col2, col3 = st.columns([0.05,0.9,0.05])
        with col1:
          st.markdown('# <<')  
        with col3:
          st.markdown('# >>')    
        with col2:
            selected_Вкладка =int(stx.tab_bar(data=data, default=data[0].id,key ="selected_Вкладка"))
        st.session_state.saved_Вкладка = selected_Вкладка
        selected_house_objectid = st.session_state["selected_house_objectid"]
        #st.info(f"{st.session_state.id_Вкладка=}")
        datums_df = datum_values_db.get_datum_values(id_houses_objectid = selected_house_objectid,
                                                subsystem_id = st.session_state.selected_subsystem_id,
                                                datum_lvl=0,datum_id_lvl=selected_Вкладка,mode='all')
    #  if not datums_df.empty:
    #          datums_df 
        
        for index, row in datums_df.iterrows():
            if 'option' in row['datum_type_code']:
                value_for_datum_type = get_value_for_datum_type(row,row['datum_type_code'])
                index_opts,opts = options_db.get_typed_options(value_for_datum_type,row['id'],row['datum_type_code'])

            spaces = '&nbsp;&nbsp;' * int(row['lvl']*4)
            
            if row['lvl'] == 1:
                c = st.container()
                col1, col2, col3 = st.columns([0.01,0.8,0.1])
            else: 
                c = st.container()
                col1, col2, col3 = st.columns([0.01,0.8,0.1])   
            with c:
                with col1: 
                    pass
                    #st.page_link(f"pages/Показатели.py?selected_house_objectid={selected_house_objectid}&datum_code={row['code']}", label=f"Изменить", icon=":material/assignment_ind:")                    
                with col2: 
                    st.markdown(f"  ### {spaces} {row['code']} {row['name']}", unsafe_allow_html=True)    
                
                    #st.checkbox("", value=False, key=row['code'])
                    sub_c = st.container()
                    if row['datum_type_code'] in("int","option_int","float","option_float"):
                        sub_col1, sub_col2, sub_col3 = st.columns([0.1,0.20,0.70])
                        if row['datum_type_code'] in ("int","option_int"):
                            format_str ='%i'
                            numvalue = row['int_value']
                        elif row['datum_type_code'] in ("float","option_float"):
                            format_str ='%0.6f'
                            numvalue = row['float_value']
                        
                        with sub_col2:
                            if row['datum_type_code'] in ("int","float"):
                                st.number_input(label = "Значение(Число)",
                                                value = numvalue,
                                                on_change = datum_values_callback,
                                                kwargs    = row.to_dict(),
                                                key= ("datum_value_"+str(row['id'])),
                                                format = format_str
                                                ) 
                            elif row['datum_type_code'] in ("option_int","option_float"):                             
                                st.selectbox(label = "Значение из Справочника(Число)",   
                                                index = index_opts,
                                                options = opts,
                                                on_change = datum_values_callback,
                                                kwargs    = row.to_dict(),
                                                key= ("datum_value_"+str(row['id'])),

                                            )    
                        with sub_col3:
                            st.markdown(get_formatted_edizm(row),unsafe_allow_html = True)        
                    elif row['datum_type_code'] in("string","option_string"):
                        sub_col1, sub_col2, sub_col3 = st.columns([0.1,0.8,0.1])
                        with sub_col2:
                            if row['datum_type_code'] in ("string"):
                                st.text_input(label = "Значение(Строка)",
                                                value = row['nvarchar_value'],
                                                on_change = datum_values_callback,
                                                kwargs    = row.to_dict(),
                                                key= ("datum_value_"+str(row['id']))
                                                ) 
                            elif row['datum_type_code'] in ("option_string"):                             
                                st.selectbox(label = "Значение из Справочника(Строка)",   
                                                index = index_opts,
                                                options = opts,
                                                on_change = datum_values_callback,
                                                kwargs    = row.to_dict(),
                                                key= ("datum_value_"+str(row['id'])),

                                            )
                        with sub_col3:
                            st.markdown(get_formatted_edizm(row),unsafe_allow_html = True)        
                    elif row['datum_type_code'] in("date","option_date"):
                        sub_col1, sub_col2, sub_col3 = st.columns([0.1,0.12,0.78])
                        with sub_col2:
                            if row['datum_type_code'] in ("date"):
                                st.date_input(label = "Значение(Дата)",
                                                format ="DD.MM.YYYY",
                                                value = row['date_value'],
                                                on_change = datum_values_callback,
                                                kwargs    = row.to_dict(),
                                                key= ("datum_value_"+str(row['id']))
                                                ) 
                            elif row['datum_type_code'] in ("option_date"):                             
                                st.selectbox(label = "Значение из Справочника(Дата)",   
                                                index = index_opts,
                                                options = opts,
                                                on_change = datum_values_callback,
                                                kwargs    = row.to_dict(),
                                                key= ("datum_value_"+str(row['id'])),
                                            )
                        with sub_col3:
                            st.markdown(get_formatted_edizm(row),unsafe_allow_html = True)        
                                
                    elif row['datum_type_code'] in("bool","option_bool"):
                        sub_col1, sub_col2, sub_col3 = st.columns([0.1,0.2,0.7])
                        with sub_col2:
                            if row['datum_type_code'] in ("bool"):
                                st.checkbox(label = "Значение(Да / Нет)",
                                                value = (row["int_value"] == 1),
                                                on_change = datum_values_callback,
                                                kwargs    = row.to_dict(),
                                                key= ("datum_value_"+str(row['id']))
                                                ) 
                            elif row['datum_type_code'] in ("option_bool"):                             
                                st.selectbox(label = "Значение из Справочника(Да / Нет)",   
                                                index = index_opts,
                                                options = opts,
                                                on_change = datum_values_callback,
                                                kwargs    = row.to_dict(),
                                                key= ("datum_value_"+str(row['id'])),
                                            )
                        with sub_col3:
                            st.markdown(get_formatted_edizm(row),unsafe_allow_html = True)        
                with col3:
                    if st.button(
                            label = 'Файлы',
                            key  = ("files_datum_value_btn"+str(row['id'])),
                            kwargs = row.to_dict()
                            ):
                            keys_to_delete = [key for key in st.session_state.keys() if 'uploader' in key]
                            for key in keys_to_delete:
                                del st.session_state[key]
                            ФайлыПоказателя.ФайлыПоказателя(row['id'],row['id_datum_type'],row['datum_type_code'],row['code'],row['name'])
                    if st.button(
                            label = 'Изображения',
                            key  = ("img_datum_value_btn"+str(row['id'])),
                            kwargs = row.to_dict()
                            ):        
                            Изображения.Изображения(row['id'],row['id_datum_type'],row['datum_type_code'],row['code'],row['name'])
                    if st.button(
                            label = 'Документы',
                            key  = ("doc_datum_value_btn"+str(row['id'])),
                            kwargs = row.to_dict()
                            ):        
                            Документы.Документы(row['id'],row['id_datum_type'],row['datum_type_code'],row['code'],row['name'])
         
 
                    if 'option' in row['datum_type_code']:
                        if st.button(
                            label = 'Выбрать из Справочника',
                            key  = ("pick_datum_value_btn"+str(row['id'])),
                            kwargs = row.to_dict()
                            ):
                            ВыборИзСправочника.BыборИзCправочникаПоказателей(row['id'],row['id_datum_type'],row['datum_type_code'],row['code'],row['name'])

                            
            st.divider()            
