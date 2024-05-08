import streamlit as st
import numpy as np
import pandas as pd
import base64
import requests
import joblib
import json

def app():
    # st.header('Dự đoán')
    # Load models and scalers
    model = joblib.load('D:\Decisions_tree\web\desicion_tree.joblib')

    # Creating two columns
    # col1, col2 = st.columns(2)

    # Column for technical specifications

    # Column for design and style

        # Danh sách các hãng xe
    source = ['Fanpage', 'Data cũ', 'Hotline', 'Người quen', 'HV giới thiệu',
'Đến trung tâm', 'Data mua', 'Seeding', 'Website']
    # Sắp xếp danh sách theo thứ tự bảng chữ cái
    employee = ['Thu', 'Linh', 'Duyên ', 'Phương', 'Loan', 'Ánh', 'Cúc', 'Yến',
'Thảo']
    # Sử dụng danh sách đã sắp xếp trong selectbox
    source = st.selectbox('Nguồn', options=source)
    year = st.slider('Tuổi', min_value=3, max_value=70)
    sale_employee = st.selectbox('Nhân viên', options=employee)
    tested = st.selectbox('Đã test', options=['Không', 'Có'])
    month = st.slider('Tháng', min_value=1, max_value=12, value=1)
    facebook = st.selectbox('Liên hệ qua Facebook', options=['Có','Không'])
    zalo = st.selectbox('Liên hệ qua Zalo', options=['Có','Không'])
    phone = st.selectbox('Liên hệ qua Số Điện Thoại', options=['Có','Không'])
    
    encoding_dict = {
        'Data cũ': 0, 'Data mua': 1, 'Fanpage': 2, 'HV giới thiệu': 3,
        'Hotline': 4, 'Người quen': 5, 'Seeding': 6, 'Website': 7, 'Đến trung tâm': 8,
        'Cúc': 0, 'Duyên ': 1, 'Linh': 2, 'Loan': 3, 'Phương': 4,
        'Thu': 5, 'Thảo': 6, 'Yến': 7, 'Ánh': 8,
        'Chốt': 0, 'Từ chối': 1,
        'Có': 0, 'Không': 1
    }
    def map_value(value):
        return encoding_dict.get(value, None)

    # Predict button in the center or under columns
    if st.button('Dự đoán'):
        # Encode and predict
        features = [source, sale_employee, tested,facebook,zalo,phone]
        nume = [year,month]
        mapped_data = [map_value(value) for value in features]
        all_features = np.hstack((mapped_data,nume))
        prediction = model.predict(all_features.reshape(1, -1))
        if prediction == 1:
            res = 'Chốt'
        else:
            res = 'Không học'
        st.write(f'Dự đoán : {res}')