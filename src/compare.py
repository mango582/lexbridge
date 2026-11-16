"""中国与美国法律比较。"""

import streamlit as st

from src import ai, config, content_loader, ui


def render_compare() -> None:
    china, usa = content_loader.load_compare()
    is_demo = (not china) or (not usa)

    ui.page_header(
        config.PAGE_COMPARE,
        "以个人信息保护为示例，对照比较中国与美国法律规则。",
    )
    if is_demo:
        ui.demo_badge()
        ui.demo_note()
    else:
        ui.note("以下内容来自团队整理的知识库，仅供参考，不构成法律意见。")

    st.markdown("### 示例主题：个人信息保护")

    ui.note(
        "重要提示：美国没有一部全国统一的综合性个人信息保护联邦法律，各州规定可能不同。"
        "以下为一般性示例比较，不能将某一州的规定视为全美统一规则。"
    )

    col_cn, col_us = st.columns(2)

    with col_cn:
        with st.container(border=True):
            st.markdown("#### 🇨🇳 中国")
            st.markdown(china if china else _china_points())

    with col_us:
        with st.container(border=True):
            st.markdown("#### 🇺🇸 美国")
            st.markdown(usa if usa else _us_points())

    if is_demo:
        ui.note("以上为演示用的一般性示例比较，仅作信息参考，不构成法律意见。具体个案请咨询专业律师。")
    else:
        ui.note("以上比较内容来自知识库，仅作信息参考，不构成法律意见。具体个案请咨询专业律师。")

    _render_ai_compare()


def _china_points() -> str:
    return """
- **立法模式**：中国有一部全国统一适用的个人信息保护专门法律《中华人民共和国个人信息保护法》（2021 年 11 月 1 日起施行）。
- **适用范围**：对个人信息处理活动进行统一规范，并对向境外提供个人信息作出专门规定。
- **核心机制**：以“告知—同意”为重要基础，确立个人信息处理的合法性基础，并对敏感个人信息提出更高保护要求。
- **跨境传输**：向境外提供个人信息通常需满足安全评估、个人信息保护认证或标准合同等条件之一。
- **监管**：由网信部门等依法履行个人信息保护监管职责。
"""


def _us_points() -> str:
    return """
- **立法模式**：美国没有一部统一的综合性联邦个人信息保护法，而是“部门立法 + 州立法”并存。
- **联邦层面**：对健康、金融、儿童等特定领域有专门立法，整体上未形成覆盖所有个人信息的联邦统一框架。
- **州层面**：加州、弗吉尼亚、科罗拉多、康涅狄格、犹他等州分别制定了各自的消费者隐私法。
- **重要区别**：不同州对适用范围、豁免情形、执行主体等规定不同，不能把某一州（如加州）的规定当作全美统一规则。
- **跨境视角**：美国并未像中国那样建立统一的数据出境事前评估机制，具体规则因领域和州而异。
"""


def _render_ai_compare() -> None:
    st.markdown("### AI 对比问答")
    if not ai.is_available():
        ui.note("未配置 DeepSeek API Key，AI 对比问答暂不可用。配置后即可使用。")
        return
    ui.note("输入一个具体的中美法律对比问题，AI 会基于团队填写的知识库作答，不会编造法条。")

    question = st.text_area(
        "你的对比问题",
        height=120,
        placeholder="例如：中国和加州对个人信息跨境传输的规定有什么不同？",
        key="compare_ai_question",
    )
    submitted = st.button("开始对比", type="primary", use_container_width=True, key="compare_ai_submit")

    if submitted:
        if not question.strip():
            st.warning("请先输入你的对比问题。")
        else:
            try:
                with st.spinner("AI 正在分析对比，请稍候…"):
                    result = ai.ask_compare(question.strip(), content_loader.load_all_for_ai(question.strip()))
                _render_compare_result(question.strip(), result)
            except Exception:
                st.error("AI 调用失败，请稍后重试，或检查 API Key 与网络。")


def _render_compare_result(question: str, result: dict) -> None:
    ui.note("以下对比由 AI 大模型基于团队知识库生成，仅供参考，不构成法律意见。")
    st.markdown("#### 问题")
    st.markdown(f"> {question}")

    st.markdown("#### 结论")
    st.markdown(result["conclusion"])

    col_cn, col_us = st.columns(2)
    with col_cn:
        with st.container(border=True):
            st.markdown("#### 🇨🇳 中国")
            st.markdown(result["china"])
    with col_us:
        with st.container(border=True):
            st.markdown("#### 🇺🇸 美国")
            st.markdown(result["usa"])

    st.markdown("#### 回答信息")
    rows = [
        ("法律依据", result["legal_basis"]),
        ("来源", result["sources"]),
        ("适用地区", result["region"]),
        ("更新时间", result["updated_at"]),
    ]
    for label, value in rows:
        st.markdown(f"**{label}**：{value}")

    ui.note("以上为 AI 生成的参考信息，不构成法律意见。重要事项请咨询专业律师。")
