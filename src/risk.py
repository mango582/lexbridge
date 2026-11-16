"""跨境合规风险分析。"""

import streamlit as st

from src import config, content_loader, ui
from src.knowledge import demo_risk


def render_risk() -> None:
    ui.page_header(
        config.PAGE_RISK,
        "描述你的跨境业务场景，查看高、中、低风险分级的演示分析结果。",
    )
    ui.demo_note()

    scenario = st.text_area(
        "业务场景描述",
        height=180,
        placeholder="例如：我的跨境电商公司把中国用户的姓名、地址和购买记录传输到美国，用于订单处理和客服。",
        key="risk_scenario",
    )

    submitted = st.button("开始分析", type="primary", use_container_width=True, key="risk_submit")

    if submitted:
        if not scenario.strip():
            st.warning("请先描述你的业务场景。")
        else:
            result = demo_risk.analyze(scenario.strip())
            _render_result(scenario.strip(), result)
    else:
        st.info("提交场景描述后，将在这里显示高、中、低风险的演示分析结果。")

    ref = content_loader.load_risk_reference()
    if ref:
        st.markdown("---")
        st.markdown("#### 团队整理的合规参考规则")
        st.markdown(ref)


def _render_result(scenario: str, result: dict) -> None:
    ui.demo_badge()
    st.markdown("#### 场景")
    st.markdown(f"> {scenario}")

    st.markdown("#### 整体风险等级")
    st.markdown(ui.risk_badge(result["overall"]), unsafe_allow_html=True)
    st.markdown(result["overall_summary"])

    st.markdown("#### 风险提示明细")
    _render_risk_items("高风险", result["high"], "高")
    _render_risk_items("中风险", result["medium"], "中")
    _render_risk_items("低风险", result["low"], "低")

    st.markdown("#### 后续建议（演示）")
    st.markdown(result["suggestion"])

    ui.note("本结果为模拟演示，并非正式法律审查，不构成法律意见。正式合规判断请咨询专业律师。")


def _render_risk_items(title: str, items: list, level: str) -> None:
    st.markdown(f"**{title}**（{len(items)} 项）")
    if not items:
        st.markdown("_暂无_")
        return
    for item in items:
        st.markdown(f"{ui.risk_badge(level)} {item}", unsafe_allow_html=True)
