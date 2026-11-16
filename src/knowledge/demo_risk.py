"""演示版跨境合规风险分析逻辑。"""


def analyze(scenario: str) -> dict:
    s = scenario.lower()

    high: list = []
    medium: list = []
    low: list = []

    if any(k in s for k in ["个人信息", "隐私", "数据", "姓名", "地址", "购买记录", "pii", "传输", "出境"]):
        high.append("涉及个人信息的跨境处理与传输：需重点关注处理的合法性与告知同意、跨境传输合规程序，以及接收方所在地的保护水平。")
        medium.append("数据最小化与留存：建议仅收集实现业务目的所必需的信息，并明确保存期限。")

    if any(k in s for k in ["美国", "境外", "海外", "跨境", "出口", "进口"]):
        high.append("业务或数据跨境：不同司法辖区的规则差异可能带来合规风险，需结合目标地区逐一确认。")

    if any(k in s for k in ["支付", "收款", "结算", "付款", "资金", "钱"]):
        medium.append("跨境支付与结算：需关注资金结算渠道、税务与反洗钱等合规要求。")

    if any(k in s for k in ["合同", "协议", "采购", "销售", "订单", "交易"]):
        medium.append("合同与交易：建议明确适用法律、争议解决、交付与验收、违约责任等条款。")

    if any(k in s for k in ["员工", "雇员", "招聘", "用工", "团队"]):
        medium.append("劳动用工：跨境用工需关注签证、劳动法适用与用工合规。")

    if any(k in s for k in ["物流", "仓储", "运输", "清关", "发货", "快递"]):
        low.append("物流与清关：需了解进出口申报、商品合规与关税等要求。")

    if not (high or medium or low):
        medium.append("演示模式无法针对该描述作出具体判断，仅提示常见的跨境合规关注方向（数据、合同、税务、准入等）。")

    if len(high) >= 2:
        overall = "高"
    elif len(high) == 1 or len(medium) >= 2:
        overall = "中"
    else:
        overall = "低"

    overall_summary = {
        "高": "综合演示判断：该场景涉及多个高风险因素，建议在正式开展业务前，由专业律师进行合规审查。",
        "中": "综合演示判断：该场景存在若干需要关注的合规点，建议进一步核实并采取针对性措施。",
        "低": "综合演示判断：该场景演示风险相对较低，但仍建议结合实际业务细节保持关注。",
    }[overall]

    suggestion = (
        "演示建议：梳理业务涉及的数据与主体；明确目标司法辖区；"
        "在正式签约或上线前，由具备相应执业资格的律师进行正式审查。"
    )

    return {
        "overall": overall,
        "overall_summary": overall_summary,
        "high": high,
        "medium": medium,
        "low": low,
        "suggestion": suggestion,
    }
