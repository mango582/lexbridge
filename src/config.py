"""全局配置与常量。"""

SITE_NAME = "LexBridge"
SITE_ICON = "⚖️"
TAGLINE = "让跨境法律信息查询更清晰、更高效。"

PAGE_HOME = "首页"
PAGE_QA = "涉外法律问答"
PAGE_COMPARE = "中国与美国法律比较"
PAGE_RISK = "跨境合规风险分析"
PAGES = [PAGE_HOME, PAGE_QA, PAGE_COMPARE, PAGE_RISK]

# session_state 键名
KEY_PAGE = "page"

# 主题色（与 .streamlit/config.toml 保持一致）
PRIMARY = "#0B4F8A"
PRIMARY_DARK = "#07355F"
ACCENT = "#4A9FE0"
LIGHT_BG = "#F4F8FB"
TEXT = "#1B2A38"
MUTED = "#5B6B7A"

# 演示模式标识
DEMO_BADGE = "演示内容"
DEMO_UPDATED_AT = "2026-11-13（演示示例日期）"

DISCLAIMER = (
    "免责声明：LexBridge 是法律信息辅助工具，仅提供一般性法律信息参考，"
    "不替代律师的正式法律意见；本工具不能保证回答一定正确、完整或及时。"
    "重要事项请务必咨询具备相应执业资格的专业律师。"
)
