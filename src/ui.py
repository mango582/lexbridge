"""公共 UI：全局样式、导航、页脚与提示组件。"""

import streamlit as st

from src import config

_CSS = """
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", "Microsoft YaHei", "PingFang SC", "Helvetica Neue", sans-serif;
}
.block-container {
    max-width: 1080px;
    margin: 0 auto;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}
h1, h2, h3, h4 { color: #07355F; font-weight: 700; }
p, li { color: #1B2A38; }

.lexbridge-hero {
    background: #0B4F8A;
    border-radius: 12px;
    padding: 2.4rem 2.6rem;
    margin-bottom: 1.6rem;
}
.lexbridge-hero .brand {
    color: #FFFFFF;
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0 0 0.4rem 0;
}
.lexbridge-hero .tagline {
    color: #D7E7F5;
    font-size: 1.12rem;
    margin: 0;
}

.lexbridge-note {
    background: #F4F8FB;
    border-left: 4px solid #4A9FE0;
    border-radius: 6px;
    padding: 0.85rem 1.1rem;
    color: #31414F;
    font-size: 0.92rem;
    line-height: 1.75;
    margin: 0.7rem 0;
}

.lexbridge-badge-demo {
    display: inline-block;
    background: #FFF3E0;
    color: #B85C00;
    border: 1px solid #F0C36A;
    border-radius: 999px;
    padding: 2px 12px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 0.6rem;
}

.lexbridge-badge-risk {
    display: inline-block;
    border-radius: 999px;
    padding: 2px 12px;
    font-size: 0.8rem;
    font-weight: 700;
    white-space: nowrap;
}
.lexbridge-badge-high { background: #FDECEC; color: #B3261E; border: 1px solid #F2B8B5; }
.lexbridge-badge-medium { background: #FFF6E5; color: #9A6700; border: 1px solid #F2D08A; }
.lexbridge-badge-low { background: #EAF6EE; color: #1E7A46; border: 1px solid #A8D5B8; }

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
}

.lexbridge-footer {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #E2EAF1;
    color: #6B7A88;
    font-size: 0.82rem;
    line-height: 1.8;
}
.lexbridge-copyright {
    color: #8A98A5;
    font-size: 0.78rem;
    text-align: center;
    margin-top: 0.6rem;
}
</style>
"""


def inject_css() -> None:
    """注入全局 CSS。"""
    st.markdown(_CSS, unsafe_allow_html=True)


def render_sidebar() -> None:
    """渲染侧边导航栏。"""
    current = st.session_state.get(config.KEY_PAGE, config.PAGE_HOME)
    with st.sidebar:
        st.markdown(
            f"<div style='font-size:1.45rem;font-weight:800;color:#0B4F8A;'>⚖️ {config.SITE_NAME}</div>",
            unsafe_allow_html=True,
        )
        st.caption("涉外法律信息辅助平台")
        st.markdown("---")
        for label in config.PAGES:
            shown = f"▸ {label}" if label == current else label
            if st.button(shown, key=f"nav_{label}", use_container_width=True):
                st.session_state[config.KEY_PAGE] = label
                st.rerun()
        st.markdown("---")
        st.caption("当前为演示版本，结果仅供参考。")


def page_header(title: str, subtitle: str) -> None:
    """页面标题与副标题。"""
    st.markdown(f"## {title}")
    st.markdown(
        f"<div style='color:#4A5A68;font-size:0.95rem;margin:0.2rem 0 0.8rem 0;'>{subtitle}</div>",
        unsafe_allow_html=True,
    )


def demo_badge() -> None:
    """演示内容徽章。"""
    st.markdown(
        f"<span class='lexbridge-badge-demo'>{config.DEMO_BADGE}</span>",
        unsafe_allow_html=True,
    )


def note(text: str) -> None:
    """浅蓝提示框。"""
    st.markdown(f"<div class='lexbridge-note'>{text}</div>", unsafe_allow_html=True)


def demo_note() -> None:
    """统一的演示模式提示。"""
    note(
        "本页为第一版演示功能：所展示的回答或分析结果为模拟演示，仅用于展示界面与流程，"
        "不构成正式法律意见，也不保证准确。重要事项请咨询专业律师。"
    )


def risk_badge(level: str) -> str:
    """返回风险等级徽章的 HTML。"""
    mapping = {"高": "high", "中": "medium", "低": "low"}
    cls = mapping.get(level, "medium")
    return f"<span class='lexbridge-badge-risk lexbridge-badge-{cls}'>{level}风险</span>"


def render_footer() -> None:
    """全局页脚与免责声明。"""
    st.markdown(
        f"<div class='lexbridge-footer'>{config.DISCLAIMER}</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='lexbridge-copyright'>LexBridge · 法律信息辅助工具 · 演示版本</div>",
        unsafe_allow_html=True,
    )
