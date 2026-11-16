"""涉外法律问答逻辑。

第一版不调用任何收费 API。优先从 content/qa.md 知识库匹配回答；
知识库没有命中时，使用内置的演示回答兜底。
未来可在本模块中替换为真实资料库检索 + AI 生成。
"""

import re

from src import ai, config, content_loader

_NO_BASIS = "演示模式下暂不提供具体法条，避免编造。接入真实法律资料库后，将在此显示对应依据。"
_NO_SOURCE = "演示模式暂无可靠来源。接入真实资料库后，将在此显示来源。"


def answer(question: str) -> dict:
    # 0) 若已配置 DeepSeek，优先用 AI 智能体回答
    if ai.is_available():
        try:
            return ai.ask(question, content_loader.load_all_for_ai(question))
        except Exception:
            pass

    # 1) 优先从团队填写的知识库匹配
    for entry in content_loader.load_qa_entries():
        if _matches(question, entry):
            return _from_entry(entry)

    # 2) 知识库没有命中，使用演示回答
    q = question.lower()

    if any(k in q for k in ["个人信息", "隐私", "数据", "出境", "跨境传输", "pii"]):
        return _personal_info()

    if any(k in q for k in ["公司", "设立", "注册", "经营主体", "投资", "落地"]):
        return _business_setup()

    if any(k in q for k in ["合同", "协议", "违约", "交易", "买卖"]):
        return _contract()

    if any(k in q for k in ["合规", "风险", "审查", "许可", "监管", "准入"]):
        return _compliance()

    return _fallback()


def _matches(question: str, entry: dict) -> bool:
    q = question.lower()
    keywords = entry.get("关键词", "")
    for kw in re.split(r"[,，、]", keywords):
        kw = kw.strip()
        if kw and kw.lower() in q:
            return True
    title = (entry.get("title") or "").strip()
    if title and title.lower() in q:
        return True
    return False


def _from_entry(entry: dict) -> dict:
    return {
        "summary": entry.get("回答") or "（该条目尚未填写“回答”内容，请补充。）",
        "legal_basis": entry.get("法律依据") or "暂缺（该条目尚未填写法律依据）",
        "sources": entry.get("来源") or "暂无（该条目尚未填写来源）",
        "region": entry.get("适用地区") or "未填写",
        "updated_at": entry.get("更新时间") or "未填写",
        "from_kb": True,
    }


def _personal_info() -> dict:
    return {
        "summary": (
            "跨境个人信息处理通常需要重点关注几个方面：其一，是否具备合法、正当、必要的处理基础，"
            "并履行告知与同意等要求；其二，向境外提供个人信息时，是否需要完成安全评估、认证或签订标准文件等程序；"
            "其三，接收方所在地区的法律环境与保护水平；其四，发生安全事件时的响应与通知义务。"
            "中国与美国在个人信息保护上采用不同的制度路径，具体应结合所涉司法辖区与业务场景判断。"
        ),
        "legal_basis": _NO_BASIS,
        "sources": _NO_SOURCE,
        "region": "中国 / 美国（美国各州规定可能不同）",
        "updated_at": config.DEMO_UPDATED_AT,
    }


def _business_setup() -> dict:
    return {
        "summary": (
            "跨境经营涉及主体设立时，一般需要关注：经营所在地对外资准入、行业许可和注册登记的要求；"
            "公司治理与税务安排；劳动用工与签证或工作许可；以及知识产权与数据合规等。"
            "中国与美国在准入与监管上差异较大，建议结合具体行业与目标地区进一步确认。"
        ),
        "legal_basis": _NO_BASIS,
        "sources": _NO_SOURCE,
        "region": "中国 / 美国（视具体场景）",
        "updated_at": config.DEMO_UPDATED_AT,
    }


def _contract() -> dict:
    return {
        "summary": (
            "跨境合同一般需要关注：适用的法律与争议解决条款（诉讼或仲裁、管辖地）；"
            "付款、交付与验收；知识产权归属与保密；违约责任与解除条件；以及跨境数据与合规条款。"
            "不同司法辖区的合同解释规则不同，正式签署前建议由专业律师审阅。"
        ),
        "legal_basis": _NO_BASIS,
        "sources": _NO_SOURCE,
        "region": "中国 / 美国（视合同约定）",
        "updated_at": config.DEMO_UPDATED_AT,
    }


def _compliance() -> dict:
    return {
        "summary": (
            "跨境合规一般需要结合具体业务，评估数据与隐私、行业准入、贸易管制、劳动用工、"
            "税务与反商业贿赂等多个维度。演示模式无法针对你的具体情况作出判断，仅提示常见的合规关注方向。"
        ),
        "legal_basis": _NO_BASIS,
        "sources": _NO_SOURCE,
        "region": "中国 / 美国（视业务场景）",
        "updated_at": config.DEMO_UPDATED_AT,
    }


def _fallback() -> dict:
    return {
        "summary": (
            "演示模式暂未收录与该问题直接对应的知识。为避免给出不准确的信息，"
            "我不会编造具体的法律名称、法条或案例。建议把问题聚焦到个人信息保护、"
            "公司设立、跨境合同或合规风险等主题，或在实际业务中咨询专业律师。"
        ),
        "legal_basis": _NO_BASIS,
        "sources": _NO_SOURCE,
        "region": "暂不确定",
        "updated_at": config.DEMO_UPDATED_AT,
    }
