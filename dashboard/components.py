import streamlit as st

def kpi_card(title, value, icon):
    st.markdown(
        f"""
        <div style="
            background-color:#181818;
            padding:20px;
            border-radius:15px;
            border:1px solid #333;
            text-align:center;
            ">
            <div style="font-size:30px;">{icon}</div>
            <div style="font-size:18px;color:#b3b3b3;">
                {title}
            </div>
            <div style="
                font-size:32px;
                font-weight:bold;
                color:#1DB954;
                ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
