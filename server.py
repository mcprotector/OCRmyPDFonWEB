import os
import tempfile
import streamlit as st
import ocrmypdf

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

STATE_FIXED_PDF_PATH="fixed_pdf_path"
STATE_UPLOADED_FILE="uploaded_file"
STATE_UPLOADED_FILE_NAME="uploaded_file_name"

ocrmypdf_ocr=True
ocrmypdf_deskew=False
ocrmypdf_optimize=1
ocrmypdf_languages=[]

st.set_page_config(page_title='OCRmyPDFonWEB')

def uploader_callback():
    if st.session_state[STATE_UPLOADED_FILE] is not None:
        fd, path = tempfile.mkstemp()

        with st.spinner('For large files, the duration of the process can be very long. Therefore, it is recommended to be patient and wait as long as no error message is displayed.'):
            try:
                with os.fdopen(fd, 'wb') as tmp:
                    uploaded_file=st.session_state[STATE_UPLOADED_FILE]

                    tmp.write(uploaded_file.getvalue())
                    tmp.close()

                    fixed_path=path + '_fixed.pdf'

                    # Формируем строку языков для OCRmyPDF (например: 'deu+eng+rus')
                    lang_string = '+'.join(st.session_state['selected_languages']) if st.session_state['selected_languages'] else 'eng'

                    ocrmypdf.ocr(path, fixed_path, 
                        language=lang_string,
                        optimize=ocrmypdf_optimize,
                        deskew=ocrmypdf_deskew,
                        tesseract_timeout=400 if ocrmypdf_ocr else 0,
                        force_ocr=True,
			rotate_pages=True,
                        rotate_pages_threshold=5.0,
                        max_image_mpixels=901167396
                    )

                    st.session_state[STATE_FIXED_PDF_PATH] = fixed_path
                    st.session_state[STATE_UPLOADED_FILE_NAME] = uploaded_file.name + '_ompow.pdf'                    
            finally:
                os.remove(path)

def download_callback():
    for key in st.session_state.keys():
        del st.session_state[key]

c1 = st.container()
c1.title("OCRmyPDFonWEB")

if STATE_FIXED_PDF_PATH not in st.session_state:
    c1.write("Выберите параметры и загрузите PDF-файл. После успешного завершения этого процесса отредактированный PDF-файл будет доступен для скачивания.")
    ocrmypdf_ocr = c1.checkbox('Распознать текст', value=True)
    ocrmypdf_deskew = c1.checkbox('Выровнять перекосы', value=True)

    # ВЫБОР ЯЗЫКОВ
    c1.write("Язык документа(-ов):")
    languages = {
        'German (Deutsch)': 'deu',
        'English': 'eng',
        'French (Français)': 'fra',
        'Spanish (Español)': 'spa',
        'Italian (Italiano)': 'ita',
        'Russian (Русский)': 'rus',
        'Polish (Polski)': 'pol',
        'Dutch (Nederlands)': 'nld'
    }
    
    selected_langs = []
    col1, col2 = c1.columns(2)
    
    with col1:
        if st.checkbox('German (Deutsch)', value=True, key='lang_deu'):
            selected_langs.append('deu')
        if st.checkbox('English', value=True, key='lang_eng'):
            selected_langs.append('eng')
        if st.checkbox('French (Français)', key='lang_fra'):
            selected_langs.append('fra')
        if st.checkbox('Spanish (Español)', key='lang_spa'):
            selected_langs.append('spa')
    
    with col2:
        if st.checkbox('Italian (Italiano)', key='lang_ita'):
            selected_langs.append('ita')
        if st.checkbox('Russian (Русский)', key='lang_rus'):
            selected_langs.append('rus')
        if st.checkbox('Polish (Polski)', key='lang_pol'):
            selected_langs.append('pol')
        if st.checkbox('Dutch (Nederlands)', key='lang_nld'):
            selected_langs.append('nld')
    
    st.session_state['selected_languages'] = selected_langs

    ocrmypdf_optimize = c1.slider(
        label = "Optimize file size (0 off, 1 without quality loss, 3 smallest but maybe with slight quality loss)",
        min_value = 0,
        max_value = 3,
        value = 0
    )
    c1.file_uploader(label="Upload PDF", on_change=uploader_callback, key=STATE_UPLOADED_FILE)
else:
    c1.write("Редактирование PDF-файла успешно завершено. Теперь оптимизированная версия готова к загрузке.")
    try:
        with open(st.session_state[STATE_FIXED_PDF_PATH], 'rb') as f:
            st.download_button(label = 'Download PDF', data = f, file_name=st.session_state[STATE_UPLOADED_FILE_NAME], on_click = download_callback)
    finally:
        os.remove(st.session_state[STATE_FIXED_PDF_PATH])
        

