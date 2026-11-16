# LexBridge · 涉外法律信息辅助平台

LexBridge 是一个面向普通用户和跨境经营者的涉外法律信息辅助平台，第一版重点展示中国与美国之间的跨境经营、个人信息保护和合规法律信息。

> 免责声明：LexBridge 是法律信息辅助工具，不替代律师的正式法律意见；不能保证回答一定正确；重要事项应咨询专业律师。

## 已实现的功能（第一版）

- 首页：网站名称、一句话介绍、三个功能入口、底部免责声明。
- 涉外法律问答：输入问题返回回答，并预留法律依据、来源、适用地区、更新时间。
- 中国与美国法律比较：个人信息保护主题的中美对照示例，并提示美国各州规定不同。
- 跨境合规风险分析：输入业务场景，返回高/中/低风险分级的分析结果。

当前版本不调用收费 API、不需要登录、不使用数据库。法律内容由团队填写的 `content/` 文件夹提供；未填写时显示“演示内容”。

## 团队协作：填写法律内容

法律内容统一放在 `content/` 文件夹，是纯文字（Markdown）文件，不写代码也能编辑。填写说明和模板见：

- [content/README.md](content/README.md)

核心规则：只写真实可核验的法条并注明出处；没有可靠资料就写“暂缺”，绝不编造；涉及美国要区分联邦与各州。

## 接入 DeepSeek（可选，让问答变成真 AI 智能体）

网站默认不依赖 AI，问答使用本地知识库 + 演示兜底。配置后，“涉外法律问答”会调用 DeepSeek 大模型，基于团队填写的知识库生成回答；“中国与美国法律比较”页面也会新增一个“AI 对比问答”，同样基于知识库做中美对比。

1. 到 https://platform.deepseek.com 注册并创建一个 API Key（DeepSeek 按量计费，价格很低，请自行确认账户余额）。
2. 打开项目里的 `.streamlit/secrets.toml` 文件，把 Key 填进 `api_key = "..."` 的引号里并保存。
3. 重新双击 `启动网站.bat` 即可生效。

没有配置 Key 时，问答会自动回退到本地知识库 / 演示逻辑，不会报错。`.streamlit/secrets.toml` 已被 `.gitignore` 忽略，不会被提交或发布。

## 启动网站（推荐：双击运行）

在项目文件夹中双击 `启动网站.bat`，等待命令行窗口出现地址后，用浏览器打开：

```text
http://localhost:8501
```

## 停止网站

- 双击 `停止网站.bat`，即可停止正在运行的网站；
- 或者在你启动网站的那个黑色命令行窗口里按 `Ctrl + C`（如果窗口还开着的话）。

## 首次安装依赖（换新电脑或删除了 .venv 时需要）

本机已创建好 `.venv` 虚拟环境并装好依赖，正常情况下直接双击 `启动网站.bat` 即可。

如果换到新电脑，请在项目文件夹打开命令行（PowerShell），依次执行：

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

> 说明：本项目使用 Python + Streamlit。如果你电脑上没有安装 Python，请先从 https://www.python.org/downloads/ 安装 Python 3.10 或更高版本（安装时勾选 “Add Python to PATH”）。

## 项目结构

```text
.
├── app.py                  # 程序入口与页面路由
├── requirements.txt        # 依赖清单
├── README.md               # 说明文档
├── 启动网站.bat             # 双击启动
├── 停止网站.bat             # 双击停止
├── .streamlit/
│   └── config.toml         # 主题与基础配置
├── content/                # 团队填写的法律内容（Markdown）
│   ├── README.md           # 填写说明与模板
│   ├── qa.md               # 问答知识库
│   ├── compare_china.md    # 中国部分
│   ├── compare_usa.md      # 美国部分
│   └── risk.md             # 合规风险参考规则
└── src/
    ├── config.py           # 网站名称、页面、颜色等常量
    ├── content_loader.py   # 读取 content/ 内容的加载器
    ├── ui.py               # 全局样式、导航、页脚、提示组件
    ├── home.py             # 首页
    ├── qa.py               # 涉外法律问答
    ├── compare.py          # 中国与美国法律比较
    ├── risk.py             # 跨境合规风险分析
    └── knowledge/
        ├── demo_qa.py      # 问答逻辑（知识库优先，演示兜底）
        └── demo_risk.py    # 演示风险分析逻辑
```

## 未来扩展方向

- 在 `content/` 下持续补充真实、可核验的法律资料。
- 用真实的 AI 模型替换 `demo_qa.py`、`demo_risk.py` 中的演示逻辑。
- 为回答添加可追溯的法条、案例与来源链接。
