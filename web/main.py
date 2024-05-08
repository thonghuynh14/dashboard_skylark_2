import streamlit as st
from streamlit_option_menu import option_menu

import predict,visualize_h

class MultiApp:

    def __init__(self):
        self.apps = []

    # def add_app(self, title, func):

    #     self.apps.append({
    #         "title": title,
    #         "function": func
    #     })

    def run():
        st.markdown("""
            <style>
            .menu-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: white;
                padding: 5px;
                border-radius: 5px;
            }
            .menu-container .menu-title {
                font-size: 20px;
                font-weight: bold;
            }
            .menu-container .additional-info {
                font-size: 18px;
                color: black;
            }
            </style>
            <div class="menu-container">
                <span class="menu-title"></span>
                <span class="additional-info">Edit by: Ngô Thị Diễm Gà</span>
            </div>
        """, unsafe_allow_html=True)

        app = option_menu(
            menu_title = "MAIN MENU", 
            options = ["Dashboard", "Predict"],
            # icons = ["car-front", "calculator", "search", "info-circle-fill"],
            default_index = 0,
            orientation = "horizontal",
            styles={
                    "container": {"padding": "5!important","background-color":'white'},
                    "icon": {"color": "black", "font-size": "23px"}, 
                    "nav-link": {"color":"black","font-size": "20px", "text-align": "center", "margin":"0px", "--hover-color": "#BDE4F5"},
                    "nav-link-selected": {"background-color": "#2BB2EF"},
                    }
            )

        if app == "Predict":
            predict.app()
        if app == "Dashboard":
            visualize_h.main()


    run()