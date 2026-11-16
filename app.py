"""LexBridge 主入口。

运行方式：
    streamlit run app.py
"""

import streamlit as st

from src import config, ui
from src.home import render_home
from src.qa import render_qa
from src.compare import render_compare
from src.risk import render_risk

# 必须是第一个 Streamlit 命令
st.set_page_config(
    page_title=config.SITE_NAME,
    page_icon=config.SITE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# 注入全局样式
ui.inject_css()

# 渲染侧边导航栏
ui.render_sidebar()

# 根据当前页面渲染对应内容
page = st.session_state.get(config.KEY_PAGE, config.PAGE_HOME)

if page == config.PAGE_HOME:
    render_home()
elif page == config.PAGE_QA:
    render_qa()
elif page == config.PAGE_COMPARE:
    render_compare()
elif page == config.PAGE_RISK:
    render_risk()
else:
    render_home()

# 全局页脚（含免责声明）
ui.render_footer()
