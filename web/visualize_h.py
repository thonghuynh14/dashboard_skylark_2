import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime


st.set_page_config(page_title="Dashboard", layout="wide")
# Thêm chú thích "Edit by" ở góc phải trên cùng
# Function to load data with caching to improve performance
@st.cache_data
def load_data():
    # Load data
    data = pd.read_excel('D:\Decisions_tree\web\data_visualize.xlsx')
    data['Doanh thu thực thu'] = data['Doanh thu thực thu'].replace(r'^\s*$', np.nan, regex=True)
    data['Doanh thu thực thu'] = pd.to_numeric(data['Doanh thu thực thu'], errors='coerce').fillna(0)
    bins = [3, 6, 15, 22, 38, 100]
    labels = ['Trẻ em', 'Thiếu niên', 'Thanh niên','Trung niên','Người già']
    data['Khoảng Tuổi'] = pd.cut(data['Tuổi'], bins=bins, labels=labels, right=False)
    return data

def main():
    data = load_data()
    
    # Create header in the center
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 60px;'>Dashboard doanh thu</h1>", unsafe_allow_html=True)
    
    # Tách cột 'Ngày liên hệ' thành các cột ngày, tháng, năm
    data['Ngày liên hệ'] = pd.to_datetime(data['Ngày liên hệ'])
    data['Ngày'] = data['Ngày liên hệ'].dt.day
    data['Tháng'] = data['Ngày liên hệ'].dt.month
    data['Năm'] = data['Ngày liên hệ'].dt.year
    # Hiển thị các chỉ số quan trọng
    total_revenue = data['Doanh thu thực thu'].sum()
    total_customers = len(data)
    col_metric1, col_metric2 = st.columns(2)
    col_metric1.metric("Tổng Doanh Thu", f"{total_revenue:,.0f} VND")  # Format as currency
    col_metric2.metric("Tổng Số Khách Hàng", f"{total_customers}")
    # Trực quan hóa biểu đồ cột ( doanh thu theo Nguồn và theo Nhân viên)
    col4, col5 = st.columns(2)
    with col4:
        group_data = data.groupby('Giao cho nhân viên Sale')['Doanh thu thực thu'].sum().reset_index()
        fig = px.bar(group_data, x='Giao cho nhân viên Sale', y='Doanh thu thực thu',
                     title='Doanh thu thực thu theo Nhân viên',
                     color='Doanh thu thực thu',
                     color_continuous_scale=px.colors.sequential.Rainbow)
        fig.update_layout(title='<b>Doanh thu theo Nhân viên</b>',
                          xaxis_title="Nhân viên",
                          yaxis_title="Doanh thu thực thu")
        st.plotly_chart(fig)

    with col5:
        monthly_revenue = data.groupby('Nguồn')['Doanh thu thực thu'].sum().reset_index()
        fig2 = px.bar(monthly_revenue, x='Nguồn', y='Doanh thu thực thu',
                      title='Doanh thu thực thu theo Nguồn',
                      color='Nguồn')
        fig2.update_layout(title='<b>Doanh thu theo Nguồn</b>',
                           xaxis_title="Nguồn",
                           yaxis_title="Doanh thu thực thu",
                           xaxis=dict(tickmode='linear'))
        st.plotly_chart(fig2)
    col8,col9 = st.columns(2)
    with col8:
        group_data = data.groupby('Khóa học')['Doanh thu thực thu'].sum().reset_index()
        fig8 = px.bar(group_data, x='Khóa học', y='Doanh thu thực thu',
                        title='Doanh thu thực thu theo Nhân viên',
                        color='Doanh thu thực thu',
                        color_continuous_scale=px.colors.sequential.Rainbow)
        fig8.update_layout(title='<b>Doanh thu theo Khóa học</b>',
                            xaxis_title="Khóa học",
                            yaxis_title="Doanh thu thực thu")
        st.plotly_chart(fig8)
    with col9:
        age_data = data.groupby('Khoảng Tuổi')['Doanh thu thực thu'].sum().reset_index().sort_values(by='Doanh thu thực thu', ascending=False)
        age_data['Cummulative %'] = (age_data['Doanh thu thực thu'].cumsum() / age_data['Doanh thu thực thu'].sum()) * 100
        # Plotting Pareto chart
        fig = go.Figure()
        # Thêm biểu đồ cột
        fig.add_trace(go.Bar(
            x=age_data['Khoảng Tuổi'],
            y=age_data['Doanh thu thực thu'],
            name='Doanh thu',
            marker=dict(color=px.colors.qualitative.Plotly)  # Bảng màu sáng
        ))

        # Thêm biểu đồ đường cho phần trăm tích lũy
        fig.add_trace(go.Scatter(
            x=age_data['Khoảng Tuổi'],
            y=age_data['Cummulative %'],
            name='Cumulative %',
            marker_color='yellow',  # Thay đổi màu đường thành màu vàng
            yaxis='y2'
        ))

        # Cập nhật bố cục với hai trục y
        fig.update_layout(
            title='<b>Biểu đồ Pareto Doanh thu theo Khoảng Tuổi</b>',
            xaxis_title="Khoảng Tuổi",
            yaxis=dict(
                title='Doanh thu thực thu',
                titlefont=dict(color='white'),  # Thay đổi màu chữ thành trắng
                tickfont=dict(color='white')  # Thay đổi màu số liệu trục thành trắng
            ),
            yaxis2=dict(
                title='Cumulative Percentage',
                titlefont=dict(color='yellow'),  # Thay đổi màu chữ của trục y2
                tickfont=dict(color='yellow'),  # Thay đổi màu số liệu trục y2
                anchor='x',
                overlaying='y',
                side='right'
            )
        )

        # Hiển thị biểu đồ
        st.plotly_chart(fig)
    # Trực quan hóa doanh thu theo tháng và lượng liên hệ trong cùng một hàng( doanh thu và số lượng liên hệ theo tháng)
    col6, col7 = st.columns(2)
    with col6:
        monthly_revenue = data.groupby('Tháng')['Doanh thu thực thu'].sum().reset_index()
        fig3 = px.line(monthly_revenue, x='Tháng', y='Doanh thu thực thu',
                       title='Doanh thu thực thu theo Tháng',
                       markers=True)
        fig3.update_layout(title='<b>Doanh thu theo Tháng</b>',
                           xaxis_title="Tháng",
                           yaxis_title="Doanh thu thực thu",
                           xaxis=dict(tickmode='linear'))
        st.plotly_chart(fig3)

    with col7:
        month_counts = data['Tháng'].value_counts().sort_index()
        month_counts = month_counts.reset_index()
        month_counts.columns = ['Tháng', 'Số Lượng']
        fig4 = px.line(month_counts, x='Tháng', y='Số Lượng',
                       title='Số lượng ghi nhận theo Tháng',
                       markers=True)
        fig4.update_layout(title='<b>Lượng liên hệ theo Tháng</b>',
                           xaxis_title="Tháng",
                           yaxis_title="Số Lượng",
                           xaxis=dict(tickmode='linear'))
        st.plotly_chart(fig4)

    
if __name__ == "__main__":
    main()
    