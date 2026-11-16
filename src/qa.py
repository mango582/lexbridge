"""涉外法律问答。"""

import streamlit as st

from src import ai, config, ui
from src.knowledge import demo_qa


def render_qa() -> None:
    ui.page_header(
        config.PAGE_QA,
        "输入你的涉外法律问题，获取结构化的回答。",
    )
    if ai.is_available():
        ui.note(
            "本页已接入 DeepSeek 智能体：AI 会基于团队填写的知识库作答，"
            "资料中没有的内容会明确提示，不会编造法条。所有回答仅供参考，不构成法律意见。"
        )
    else:
        ui.demo_note()

    question = st.text_area(
        "你的法律问题",
        height=180,
        placeholder="例如：我的公司想把中国用户的个人信息发送到美国处理，需要注意哪些合规事项？",
        key="qa_question",
    )

    submitted = st.button("提交问题", type="primary", use_container_width=True, key="qa_submit")

    if submitted:
        if not question.strip():
            st.warning("请先输入你的法律问题。")
        else:
            result = demo_qa.answer(question.strip())
            _render_answer(question.strip(), result)
    else:
        st.info("提交问题后，将在这里显示演示回答。演示回答不代表正式法律意见。")


def _render_answer(question: str, result: dict) -> None:
    if result.get("from_ai"):
        ui.note("以下回答由 AI 大模型基于团队知识库生成，仅供参考，不构成法律意见。")
        answer_heading = "#### AI 回答"
    elif result.get("from_kb"):
        ui.note("以下回答来自团队整理的知识库，仅供参考，不构成法律意见。")
        answer_heading = "#### 回答"
    else:
        ui.demo_badge()
        answer_heading = "#### 演示回答"

    st.markdown("#### 问题")
    st.markdown(f"> {question}")

    st.markdown(answer_heading)
    st.markdown(result["summary"])

    st.markdown("#### 回答信息")
    rows = [
        ("法律依据", result["legal_basis"]),
        ("来源", result["sources"]),
        ("适用地区", result["region"]),
        ("更新时间", result["updated_at"]),
    ]
    for label, value in rows:
        st.markdown(f"**{label}**：{value}")

    if result.get("from_ai"):
        ui.note("以上为 AI 生成的参考信息，不构成法律意见。重要事项请咨询专业律师。")
    elif result.get("from_kb"):
        ui.note("以上回答来自知识库，不构成法律意见。重要事项请咨询专业律师。")
    else:
        ui.note("以上为演示回答，仅供参考。正式法律意见请咨询专业律师。")
