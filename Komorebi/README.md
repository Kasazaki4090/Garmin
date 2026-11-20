# Komorebi (木漏日 · 和色时光) - 佳明 Garmin Connect IQ 极简定制表盘

> **Komorebi (こもれび)** —— 阳光穿过树梢筛落的斑驳光影。  
> 专为 Garmin 智能手表打造的高颜值、错落大时间、日系传统和色与纯代码极简矢量简笔画表盘。

---

## ✨ 核心特性

- **大时间错落排版**：大号小时居左偏中，中号分钟右侧贴合圆形边缘，小号秒钟巧妙承接，兼顾极高可读性与视觉美感。
- **6 套纯代码矢量日系简笔画**：无需加载重度位图，超低功耗、零内存浪费：
  - `B1` 晴 · 远山日轮 (富士山与日轮)
  - `B2` 云 · 浮世流云 (日式源氏霞云)
  - `B3` 阴/雾 · 水墨层峦 (双层山脊与晨雾)
  - `B4` 雨 · 细雨涟漪 (斜雨丝与水波)
  - `B5` 雪 · 雪峰寒星 (带雪冠山峦与几何雪花)
  - `B6` 夜 · 弦月眠猫 (弯月星宿与趴坡小猫)
- **48 种日本传统和色字典**：内置白练、茜色、鸟之子、青磁、胜色、樱月、消炭等经典配色。
- **MIP 64 色原生量化**：针对 Fenix / Forerunner 等 MIP 反射屏自动做 64 色硬件级吸附，真机零色差；同时完美支持 AMOLED 高清绚丽屏。
- **超长续航与 AOD 息屏保护**：休眠状态智能降频、隐藏秒针与重度图层，极度省电。
- **Cloudflare Pages 静态调色盘**：手机或电脑浏览器打开网页调色盘，一键生成复制主题短码，无缝同步到 Garmin Connect 手机设置。

---

## 📁 项目目录结构

```text
d:\Garmin\Komorebi\
├── README.md                       # 【本文件】表盘说明书
├── PROJECT_PLAN.md                 # 表盘全栈规划书（UI/配色/路线图）
├── 01_watchface_app\               # Garmin Monkey C 表盘工程源码
│   ├── manifest.xml                # 设备兼容与权限配置
│   ├── monkey.jungle               # 编译脚本入口
│   ├── resources\                  # 字符串、设置项定义与图标
│   │   ├── drawables\              #   启动图标等资源
│   │   ├── settings\               #   手机端设置项 (properties.xml / settings.xml)
│   │   └── strings\                #   多语言文案
│   └── source\                     # 7 大核心渲染与数据聚合模块
│       ├── WatchFaceApp.mc         #   应用入口与配置监听
│       ├── WatchFaceView.mc        #   主渲染管线与 AOD 息屏保护
│       ├── ThemeManager.mc         #   和色主题字典 + 短码解析器
│       ├── TimeRenderer.mc         #   错落大时间渲染
│       ├── MinimalBgDrawer.mc      #   6 套纯代码矢量简笔背景
│       ├── DataFieldsDrawer.mc     #   顶部状态 + 底部身体数据矩阵
│       └── DataProvider.mc         #   传感器与天气数据聚合缓存
└── 02_font_and_vector_assets\      # 极简数字字库提取与矢量工具脚本

# 以下为共享分区（位于仓库根 d:\Garmin\，供后续多个表盘复用）
d:\Garmin\Cloudflare_page\          # HTML5 网页调色盘与实时预览器（Cloudflare Pages）
d:\Garmin\Docs_and_Specs\           # 和色色卡规范与主题短码通信协议
d:\Garmin\启动SDK管理器.bat          # 一键启动 Garmin SDK Manager
d:\Garmin\环境检查.bat              # 一键体检 Java/SDK/私钥环境
```

---

## 🛠️ 本地开发与编译

1. **依赖环境**：
   - OpenJDK 17
   - Garmin Connect IQ SDK 7.x+
   - VS Code + `Monkey C` 插件
2. **调试运行**：
   - VS Code 中按 `F5` 选择目标设备启动模拟器。
3. **打包真机**：
   - 执行 `Monkey C: Build for Device` 导出 `.prg` 文件，直接拖入手表 `/GARMIN/APPS/` 即可。

---

## 🔗 项目协同文档（仓库根）

| 文档 | 用途 |
| :--- | :--- |
| [`../WORKFLOW.md`](../WORKFLOW.md) | 多智能体协同研发工作流、分区目录锁与 SOP |
| [`../AI_TASKS.md`](../AI_TASKS.md) | 分区工单提示词（P1 网页 / P2 字库 / P3 表盘） |
| [`../DECISIONS.md`](../DECISIONS.md) | 架构决策记录（短码协议、纯矢量背景、MIP 吸附等） |
| [`../TODO.md`](../TODO.md) · [`../BUGS.md`](../BUGS.md) · [`../result.md`](../result.md) | 待办 / 缺陷 / 成果归档 |

---

## 📄 开源许可
MIT License
