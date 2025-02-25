import cv2
import streamlit as st
from PIL import Image
import numpy as np

from ocr.ocr_metrics import OcrMetrics
from ocr.ocr_model import EasyOcrModel
from pre_process.cv_preprocess import ImgPreprocessing
from utils.image_utils import ImageKit
from utils.text_utils import TextReader


def main(ocr_model, ocr_metrics, img_process, txt_reader):
    st.title("Приложение для обработки изображений")
    uploaded_txt = None

    # Создание боковой панели
    with st.sidebar:
        st.header("Параметры обработки")

        # Загрузка изображения
        uploaded_img = st.file_uploader("Загрузите изображение", type=["jpg", "jpeg", "png"])

        # Ползунки для регулировки параметров
        brightness = st.slider("Яркость", -1.0, 1.0, 0.0, step=0.1)
        contrast = st.slider("Контраст", 0.1, 4.0, 2.0, step=0.1)
        scale = st.slider("Масштаб", 0.5, 4.0, 1.0, step=0.5)

        # Чекбоксы для автоповорота и порога
        threshold = st.checkbox("Включить пороговую обработку")
        auto_rotate = st.checkbox("Включить автоповорот")

        # Загрузка эталонного текста для проверки ocr
        if uploaded_img is not None:
            # исходное изображение в формате pil
            original_image = Image.open(uploaded_img)
            # изображение для обработки в формате cv
            rgb_image = np.array(original_image)
            image_cv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
            # загрузка изображения для обработки в формате cv
            img_process.image_fromarray(image_cv)
            # обработка изображения с учетом параметров
            processed_image = img_process.run(
                rotate=auto_rotate, rotation_angle=None,
                brightness_factor=brightness,
                contrast_factor=contrast,
                scale_factor=scale,
                thresholding=threshold
            )
            #загрузка текста для расчета метрик
            uploaded_txt = st.file_uploader("Загрузите проверочный текст ocr", type=["txt"])
            ocr_text_raw = ''
            ocr_text_trans = ''
            ocr_wer_raw = -1
            ocr_werd_raw = -1
            ocr_wer_trans = -1
            ocr_werd_trans = -1
            # Кнопка для обработки
            if uploaded_txt is not None:

                if st.button("Обработать"):
                    ref_text = txt_reader.read_txt_raw(uploaded_txt)
                    ocr_text_raw = ocr_easy.get_text(original_image)
                    ocr_wer_raw = ocr_metrics.calculate(ocr_text_raw, ref_text)
                    ocr_werd_raw = ocr_metrics.calculate(ocr_text_raw, ref_text, mode='digits')
                    ocr_text_trans = ocr_easy.get_text(processed_image)
                    ocr_wer_trans = ocr_metrics.calculate(ocr_text_trans, ref_text)
                    ocr_werd_trans = ocr_metrics.calculate(ocr_text_trans, ref_text, mode='digits')


    # Основная область
    col1, col2 = st.columns(2)

    # Отображение изображений и текстовых полей
    with col1:
        st.header("Исходное изображение")
        if uploaded_img is not None:

            st.image(original_image, caption='Исходное изображение', use_container_width=True)
            st.text_area(f"Текст исходного изображения wer слова/цифры = {ocr_wer_raw:.2f} / {ocr_werd_raw:.2f}",
                         value = ocr_text_raw, height=100)
        else:
            st.text("Пожалуйста, загрузите изображение.")

    with col2:
        st.header("Обработанное изображение")
        if uploaded_img is not None:

            st.image(processed_image, caption='Обработанное изображение', use_container_width=True)
            st.text_area(f"Текст обработанного изображения wer слова/цифры = {ocr_wer_trans:.2f} / {ocr_werd_trans:.2f}",
                         value=ocr_text_trans, height=100)
        else:
            st.text("Пожалуйста, загрузите изображение.")


if __name__ == "__main__":
    ocr_easy = EasyOcrModel()
    ocr_wer = OcrMetrics()
    image_processor = ImgPreprocessing()
    text_reader = TextReader()
    main(ocr_easy, ocr_wer, image_processor, text_reader)
