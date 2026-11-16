"""读取 content/ 目录中团队填写的法律内容。

所有内容文件都是纯文本（Markdown），非程序员也能用记事本编辑。
本模块负责把内容读进来，并在内容缺失时返回空字符串，由各页面回退到演示内容。
"""

import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(_ROOT, "content")
LAWS_DIR = os.path.join(CONTENT_DIR, "laws")

# 每条法律对应的检索关键词（用户问题命中关键词时，才会把该法律送入 AI）
_LAW_KEYWORDS = {
    "个人信息保护法": ["个人信息", "隐私", "同意", "敏感个人信息", "出境", "告知"],
    "数据安全法": ["数据安全", "重要数据", "分类分级", "安全评估", "数据出境"],
    "网络数据安全管理条例": ["网络数据", "个人信息出境", "重要数据出境", "安全评估", "跨境"],
    "出口管制法": ["出口管制", "管制物项", "出口许可", "管控名单", "最终用户", "对等"],
    "两用物项出口管制条例": ["两用物项", "最终用户", "最终用途", "出口许可", "关注名单"],
    "反不正当竞争法": ["商业秘密", "不正当竞争", "反不正当竞争"],
    "民法典": ["合同", "格式条款", "违约责任", "人格权", "要约", "承诺", "隐私", "买卖"],
    "涉外民事关系法律适用法": ["涉外", "准据法", "法律适用", "涉外民事", "知识产权侵权"],
    "CCPA": ["ccpa", "cpra", "加州", "california", "消费者隐私", "privacy", "退出售卖", "删除", "更正", "敏感信息"],
    "EAR736": ["ear", "商业管制清单", "bureau of industry", "bis", "许可例外", "736", "出口管制"],
    "EAR744": ["ear", "实体清单", "entity list", "军事最终用户", "军事情报", "744", "bis"],
    "FIRRMA_FAQs": ["firrma", "cfius", "外资", "国家安全审查", "covered investment", "房地产", "受控投资"],
    "DTSA": ["dtsa", "商业秘密", "trade secret", "utsa", "窃取"],
}


def _read(rel_path: str) -> str:
    """读取内容文件，兼容 UTF-8 / UTF-8 BOM / GBK 编码。"""
    path = os.path.join(CONTENT_DIR, rel_path)
    if not os.path.exists(path):
        return ""
    for enc in ("utf-8", "utf-8-sig", "gbk"):
        try:
            with open(path, encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except OSError:
            return ""
    return ""


def _clean(text: str) -> str:
    """去掉 HTML 注释（<!-- ... -->）和空行，返回实际内容。"""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    lines = [ln.strip() for ln in text.splitlines()]
    return "\n".join([ln for ln in lines if ln]).strip()


def load_compare() -> tuple:
    """返回 (中国部分, 美国部分)，为空字符串表示未填写。"""
    return _clean(_read("compare_china.md")), _clean(_read("compare_usa.md"))


def load_risk_reference() -> str:
    """返回风险分析页的“团队整理参考规则”内容。"""
    return _clean(_read("risk.md"))


def load_qa_entries() -> list:
    """解析 qa.md 中的问答条目，返回 dict 列表。"""
    text = _read("qa.md")
    if not text:
        return []
    return _parse_qa(text)


def load_law_texts() -> dict:
    """读取 content/laws/ 下所有 .txt 法律全文，返回 {名称: 文本}。"""
    texts = {}
    if not os.path.isdir(LAWS_DIR):
        return texts
    for name in sorted(os.listdir(LAWS_DIR)):
        if name.lower().endswith(".txt"):
            stem = os.path.splitext(name)[0]
            try:
                with open(os.path.join(LAWS_DIR, name), encoding="utf-8") as f:
                    texts[stem] = f.read()
            except OSError:
                continue
    return texts


def retrieve_laws(question: str, per_law_cap: int = 10000, max_laws: int = 4, total_cap: int = 30000) -> list:
    """根据问题关键词，检索相关的法律条文（带截断，避免超出上下文）。"""
    q = (question or "").lower()
    hits = []
    for stem, text in load_law_texts().items():
        keywords = _LAW_KEYWORDS.get(stem, [])
        if any(k.lower() in q for k in keywords):
            hits.append((stem, text))
    for stem, text in load_law_texts().items():
        if stem.lower() in q and not any(h[0] == stem for h in hits):
            hits.append((stem, text))

    result = []
    used = 0
    for stem, text in hits[:max_laws]:
        piece = text[:per_law_cap]
        result.append((stem, piece))
        used += len(piece)
        if used >= total_cap:
            break
    return result


def load_all_for_ai(question: str = "") -> str:
    """把 content/ 下的所有内容拼成一段文本，供 AI 智能体作为参考资料。"""
    parts = []

    entries = load_qa_entries()
    if entries:
        lines = ["【问答知识库】"]
        for e in entries:
            lines.append("## " + (e.get("title") or "未命名条目"))
            for key, label in [
                ("关键词", "关键词"),
                ("适用地区", "适用地区"),
                ("更新时间", "更新时间"),
                ("回答", "回答"),
                ("法律依据", "法律依据"),
                ("来源", "来源"),
            ]:
                val = e.get(key)
                if val:
                    lines.append(f"{label}：{val}")
        parts.append("\n".join(lines))

    china, usa = load_compare()
    if china:
        parts.append("【中国 · 个人信息保护】\n" + china)
    if usa:
        parts.append("【美国 · 个人信息保护】\n" + usa)

    risk = load_risk_reference()
    if risk:
        parts.append("【跨境合规风险参考规则】\n" + risk)

    sources = _clean(_read("sources.md"))
    if sources:
        parts.append("【法规来源清单】\n" + sources)

    for name, text in retrieve_laws(question):
        parts.append(f"【法律条文 · {name}】\n{text}")

    return "\n\n".join(parts) if parts else "（知识库目前为空）"


def _parse_qa(text: str) -> list:
    entries = []
    # 以行首 "## " 作为每条条目的分隔
    blocks = re.split(r"(?m)^##\s+", text)
    for block in blocks[1:]:
        lines = block.splitlines()
        title = lines[0].strip() if lines else ""
        fields = {}
        current = None
        for line in lines[1:]:
            m = re.match(r"^(关键词|适用地区|更新时间|回答|法律依据|来源)[：:]\s*(.*)$", line)
            if m:
                current = m.group(1)
                fields[current] = m.group(2).strip()
            else:
                if current and line.strip():
                    fields[current] = (fields.get(current, "") + "\n" + line.strip()).strip()
        if title:
            fields["title"] = title
            entries.append(fields)
    return entries
