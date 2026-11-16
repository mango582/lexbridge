"""首页。"""

import streamlit as st

from src import config, ui


def render_home() -> None:
    # 英雄区
    st.markdown(
        f"""
        <div class="lexbridge-hero">
            <div class="brand">⚖️ {config.SITE_NAME}</div>
            <p class="tagline">{config.TAGLINE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 选择一项功能开始使用")

    features = [
        {
            "icon": "💬",
            "title": config.PAGE_QA,
            "desc": "输入涉外法律问题，获取结构化的演示回答，并预留法律依据与来源位置。",
            "target": config.PAGE_QA,
        },
        {
            "icon": "⚖️",
            "title": config.PAGE_COMPARE,
            "desc": "以个人信息保护为示例，对照比较中国与美国法律规则的异同。",
            "target": config.PAGE_COMPARE,
        },
        {
            "icon": "🛡️",
            "title": config.PAGE_RISK,
            "desc": "描述你的跨境业务场景，查看高、中、低风险分级的演示分析结果。",
            "target": config.PAGE_RISK,
        },
    ]

    cols = st.columns(3)
    for idx, (col, feat) in enumerate(zip(cols, features)):
        with col:
            with st.container(border=True):
                st.markdown(
                    f"<div style='font-size:1.9rem;'>{feat['icon']}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='color:#0B4F8A;font-weight:700;font-size:1.08rem;margin:0.35rem 0;'>{feat['title']}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='color:#4A5A68;font-size:0.9rem;line-height:1.65;min-height:3.7rem;'>{feat['desc']}</div>",
                    unsafe_allow_html=True,
                )
                if st.button("进入功能", key=f"home_go_{idx}", use_container_width=True):
                    st.session_state[config.KEY_PAGE] = feat["target"]
                    st.rerun()

    ui.note(
        "LexBridge 第一版重点展示中国与美国之间的跨境经营、个人信息保护与合规法律信息。"
        "当前为演示版本，暂不接入真实法律资料库与 AI 模型。"
    )
