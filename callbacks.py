import streamlit as st
from streamlit.components.v1 import html

def reset_image():
    if "image" in st.session_state:
        st.session_state.image = None

# def set_zone_input():
#     selected_zone = st.session_state.zone_input
#     st.session_state["zone_input"] = selected_zone

# def set_age_input():
#     selected_zone = st.session_state.zone_input
#     st.session_state["selected_zone"] = selected_zone

def scroll_to_bottom():
    # Use JS to scroll the main page’s .main container to bottom
    js = """
    <script>
    window.parent.document.documentElement.scrollTo({
      top: 0,
      behavior: "smooth"
    });
    </script>
    """
    html(js)#, height=0)
