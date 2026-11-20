# 佳明 Garmin Connect IQ 开发仓库

> Connect IQ 全栈开发工作区：表盘源码、字体/矢量资源、Cloudflare Pages 网页调色盘与规范文档统一分区管理。

---

## ⌚ 表盘列表

| # | 名称 | 状态 | 说明 |
| :--- | :--- | :--- | :--- |
| 1 | **Komorebi（木漏日 · 和色时光）** | 开发中 | 错落大时间 + 6 套纯代码矢量日系简笔背景 + 48 种日本传统和色 + Cloudflare 网页调色盘。详见 [`Komorebi/README.md`](Komorebi/README.md) |

## 📱 应用列表

| # | 名称 | 状态 | 说明 |
| :--- | :--- | :--- | :--- |
| 1 | *（预留：新 app 在此登记，并新建同名顶级目录）* | — | — |

---

## 📁 仓库目录结构

```text
d:\Garmin\
├── README.md                       # 【本文件】仓库总览与索引
├── WORKFLOW.md                     # 协同研发工作流（协作模型、目录锁、SOP、管控节奏）
├── AI_TASKS.md                     # 分区工单：可直接复制给 AI 会话的提示词（P1/P2/P3）
├── DECISIONS.md                    # 架构决策记录 ADR（短码协议、纯矢量背景、MIP 吸附…）
├── TODO.md                         # 宏观待办与优先级（P0~P3）
├── BUGS.md                         # 缺陷分级与回归追踪
├── result.md                       # 阶段成果与工程事件归档（Append Only）
├── developer_key.der               # 开发者签名私钥（已 gitignore，勿提交）
├── 启动SDK管理器.bat                # 一键启动 tools\sdkmanager 内的 SDK Manager
├── 环境检查.bat                    # 一键体检 Java / SDK / 私钥 / VS Code 插件
│
├── Komorebi\                       # 【表盘 1】Komorebi 木漏日
│   ├── README.md                   #   表盘说明书（特性、结构、编译）
│   ├── PROJECT_PLAN.md             #   表盘全栈规划书（UI/配色/路线图）
│   ├── 01_watchface_app\           #   Monkey C 表盘工程（manifest + source + resources）
│   └── 02_font_and_vector_assets\  #   数字字库提取与矢量工具脚本
│
├── Cloudflare_page\                # 【网页】Cloudflare Pages 静态调色盘（HTML5 零后端）
│
├── Docs_and_Specs\                 # 【文档】跨表盘共享的规范与接口定义
│   ├── JAPANESE_PALETTE_SPEC.md    #   48 种日本传统和色色卡与 6 套简笔画规范
│   └── THEME_PROTOCOL.md           #   网页调色盘 <-> 表盘 主题短码通信协议
│
├── ProjectManagementTemplate\      # 【模板】多智能体协同研发管理体系模板（只读参考）
│
├── tools\                          # 【工具】SDK Manager 等本地开发工具（已 gitignore）
└── .vscode\                        # 【IDE】Monkey C / JDK 工作区配置（已 gitignore）
```

> **新表盘/新 app 约定**：每个表盘或应用一个顶级目录（如 `Komorebi\`），内部沿用 `01_xxx_app`、`02_xxx_assets` 的数字分区；网页与文档统一放 `Cloudflare_page\` 与 `Docs_and_Specs\`，避免重复。

---

## 🔁 工作流程

完整的多智能体协同研发工作流（协作模型、分区目录锁、单智能体 SOP、管控节奏、真机注意事项）见 [`WORKFLOW.md`](WORKFLOW.md)。

速览：

| 阶段 | 做什么 | 位置 |
| :--- | :--- | :--- |
| **P0 环境** | 环境体检 → 装 SDK → 校验 Monkey C 插件 | `环境检查.bat` / `启动SDK管理器.bat` |
| **P0 契约** | 冻结主题短码协议与和色字典（此后改动须同步三方） | `Docs_and_Specs\` |
| **P1 网页** | 开发/部署 HTML5 调色盘，产出主题短码 | `Cloudflare_page\` |
| **P2 字库** | TTF → 仅含 `0-9 :` 的 `.fnt + .png`（≤8KB/套） | `Komorebi\02_font_and_vector_assets\` |
| **P3 表盘** | Monkey C 编码、模拟器预览、导出 `.prg` 上真机 | `Komorebi\01_watchface_app\` |

进度与成果：待办记录在 [`TODO.md`](TODO.md)，每个分区完成后按格式追加到 [`result.md`](result.md)。

---

## 📄 开源许可

MIT License
