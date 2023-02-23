import streamlit as st
import base64


def header_ui(title="S2U Route Optimization"):
    st.markdown(
        """
        <style>
        .pageheader {
            padding: 0px;
            width: 100%;
            margin-left: 0px;
            margin-top: -60px;
            margin-bottom: 50px;
        }
        .pagetitle {
            text-align: center; 
            #position: absolute; 
            width: 100%;  
            margin-bottom: 10px; 
            border: 2px solid black;
            font-size: 30px;
            font-weight: bold;
            padding: 10px;
            border-radius: 10px;
            background-color: #004B93;
            #color: black; 
            color: white;
        }
    """,
        unsafe_allow_html=True,
    )

    metric_style = f"""
    <style>
    div.css-1r6slb0.e1tzin5v2 {{ 
        border: 1.5px solid black;
        padding: 5px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 20px;
        background-color: #F9F9F9;
        }}
    div.row-widget.stButton {{
        text-align: center;
    }}
    button.css-629wbf.edgvbvh10 {{
        border: 1px solid black;
        background-color: #004B93;
        color: white;
        margin: auto;
    }}
    <style>
    """
    st.markdown(metric_style, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='pageheader'>
            <p class='pagetitle'>
                {title}
            </p>
        </div>""",
        unsafe_allow_html=True,
    )


def sidebar_ui():
    img = "./pepsico-logo.png"
    st.markdown(
        f"""
    <div style="margin-top: -30px; margin-bottom: 30px;">
        <center><img  src="data:image/png;base64,{base64.b64encode(open(img, "rb").read()).decode()}"></center>
    </div>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='text-align: center; color: black;'>DC Capacity</h3>",
        unsafe_allow_html=True,
    )
