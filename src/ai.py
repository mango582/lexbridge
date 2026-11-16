"""DeepSeek 大模型接入（法律问答智能体）。

通过 DeepSeek 的 OpenAI 兼容接口调用 deepseek-chat 模型。
API Key 从 .streamlit/secrets.toml 的 [deepseek] api_key 或环境变量读取。
未配置 Key 时，问答自动回退到本地知识库 / 演示逻辑，不会报错。
"""

import json
import os
import re

import requests

DEEPSEEK_BASE = "https://api.deepseek.com"
DEEPSEEK_MODEL = os.environ.get("LEXBRIDGE_MODEL", "deepseek-chat")


def get_api_key() -> str:
    """读取 DeepSeek API Key（优先 Streamlit secrets，其次环境变量）。"""
    try:
        import streamlit as st

        val = st.secrets["deepseek"]["api_key"]
        if val:
            return str(val).strip()
    except Exception:
        pass
    for name in ("LEXBRIDGE_DEEPSEEK_API_KEY", "DEEPSEEK_API_KEY"):
        val = os.environ.get(name)
        if val:
            return val.strip()
    return ""


def is_available() -> bool:
    return bool(get_api_key())


def _system_prompt() -> str:
    return (
        "你是 LexBridge 的法律信息助手，面向中国用户，提供中国与美国之间的涉外法律信息辅助。\n"
        "严格遵守以下规则：\n"
        "1. 只能依据【参考资料】作答；资料中没有的内容，直接写“资料中暂未覆盖”，绝不编造法律名称、法条、条文编号或案例。\n"
        "2. 涉及美国时，必须区分联邦层面与各州，不能把某一州的规定说成全美统一。\n"
        "3. 只输出一个 JSON 对象，不要输出任何多余文字，字段固定为：回答、法律依据、来源、适用地区、更新时间。\n"
        "4. “回答”要条理清晰、面向普通用户；“法律依据”写明依据的法条或规则（资料没有则写“暂缺”）；"
        "“来源”写资料出处（没有则写“暂无”）；“更新时间”写资料的更新日期（没有则写“未填写”）。\n"
        "5. 在“回答”末尾必须加一句提醒：本内容仅为法律信息参考，不构成法律意见，重要事项请咨询专业律师。\n"
        "输出示例：{\"回答\":\"……\",\"法律依据\":\"……\",\"来源\":\"……\",\"适用地区\":\"……\",\"更新时间\":\"……\"}"
    )


def build_messages(question: str, kb_text: str) -> list:
    user = f"【参考资料】\n{kb_text}\n\n【用户问题】\n{question}"
    return [
        {"role": "system", "content": _system_prompt()},
        {"role": "user", "content": user},
    ]


def _parse(content: str) -> dict:
    text = content.strip()
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if m:
        text = m.group(0)
    data = json.loads(text)
    return {
        "summary": data.get("回答", "").strip() or "（AI 未返回回答内容）",
        "legal_basis": data.get("法律依据", "").strip() or "暂缺",
        "sources": data.get("来源", "").strip() or "暂无",
        "region": data.get("适用地区", "").strip() or "未填写",
        "updated_at": data.get("更新时间", "").strip() or "未填写",
        "from_ai": True,
    }


def ask(question: str, kb_text: str) -> dict:
    key = get_api_key()
    resp = requests.post(
        DEEPSEEK_BASE + "/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": DEEPSEEK_MODEL,
            "messages": build_messages(question, kb_text),
            "temperature": 0.2,
            "stream": False,
        },
        timeout=60,
    )
    resp.raise_for_status()
    payload = resp.json()
    content = payload["choices"][0]["message"]["content"]
    return _parse(content)


def _compare_system_prompt() -> str:
    return (
        "你是 LexBridge 的法律对比助手，专门比较中国与美国（含美国各州）的涉外法律规则。\n"
        "严格遵守以下规则：\n"
        "1. 只能依据【参考资料】作答；资料中没有的内容，直接写“资料中暂未覆盖”，绝不编造法律名称、法条、条文编号或案例。\n"
        "2. 涉及美国时，必须区分联邦层面与各州，不能把某一州的规定说成全美统一。\n"
        "3. 只输出一个 JSON 对象，字段固定为：结论、中国、美国、法律依据、来源、适用地区、更新时间。\n"
        "4. “结论”用一两句话概括异同；“中国”“美国”分别写各自规则要点；"
        "“法律依据”写依据（资料没有则写“暂缺”）；“来源”写资料出处（没有则写“暂无”）；"
        "“适用地区”写“中国 / 美国”或具体州；“更新时间”写资料更新日期（没有则写“未填写”）。\n"
        "5. 在“结论”末尾加一句：本内容仅为法律信息参考，不构成法律意见，重要事项请咨询专业律师。\n"
        "输出示例：{\"结论\":\"……\",\"中国\":\"……\",\"美国\":\"……\",\"法律依据\":\"……\",\"来源\":\"……\",\"适用地区\":\"……\",\"更新时间\":\"……\"}"
    )


def _parse_compare(content: str) -> dict:
    text = content.strip()
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if m:
        text = m.group(0)
    data = json.loads(text)
    return {
        "conclusion": data.get("结论", "").strip() or "（AI 未返回结论）",
        "china": data.get("中国", "").strip() or "资料中暂未覆盖",
        "usa": data.get("美国", "").strip() or "资料中暂未覆盖",
        "legal_basis": data.get("法律依据", "").strip() or "暂缺",
        "sources": data.get("来源", "").strip() or "暂无",
        "region": data.get("适用地区", "").strip() or "未填写",
        "updated_at": data.get("更新时间", "").strip() or "未填写",
        "from_ai": True,
    }


def ask_compare(question: str, kb_text: str) -> dict:
    key = get_api_key()
    resp = requests.post(
        DEEPSEEK_BASE + "/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": _compare_system_prompt()},
                {"role": "user", "content": f"【参考资料】\n{kb_text}\n\n【用户问题】\n{question}"},
            ],
            "temperature": 0.2,
            "stream": False,
        },
        timeout=60,
    )
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    return _parse_compare(content)
