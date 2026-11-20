# TODO — Garmin Connect IQ 仓库待办

> 任务来源：[`Komorebi/PROJECT_PLAN.md`](Komorebi/PROJECT_PLAN.md)（愿景/里程碑）、[`Docs_and_Specs/`](Docs_and_Specs)（接口契约）、[`WORKFLOW.md`](WORKFLOW.md)（分区划分）、源码现状。
> 优先级：`P0` MVP 必需 · `P1` 首个可用版本 · `P2` 体验增强 · `P3` 可选探索。
> 缺陷不写在本文件，记录到 `BUGS.md`（如启用）。

---

## 1. 环境与契约（P0 前置）

- [ ] P0 [环境] 运行 `环境检查.bat`，确认 JDK 17 / 私钥 / SDK Manager / SDK / Monkey C 插件 5 项全 OK
- [ ] P0 [环境] `启动SDK管理器.bat` 下载最新 SDK 并 **Use as current SDK**，勾选目标机型固件
- [ ] P0 [决策] 确认目标手表具体型号（决定 MIP 260x260 还是 AMOLED 454x454 为第一优先基准）
- [ ] P0 [契约] 冻结 `THEME_PROTOCOL.md` v1 字段（此后改动须同步网页端与表盘端）
- [ ] P1 [契约] 在 `Docs_and_Specs\` 补充 `resources\settings\` 设置项清单与短码输入框校验规则

## 2. Partition 1 · 网页调色盘（`Cloudflare_page\`）

- [ ] P0 搭建单页骨架：`index.html` / `style.css` / `app.js`，手机与桌面响应式
- [ ] P0 实现主题短码生成器与解析器，用协议中 4 套默认主题做断言自测
- [ ] P0 内置 48 种日本传统和色色卡（6 大色系分类，含日文/罗马音/HEX）
- [ ] P1 Canvas 1:1 表盘仿真预览（错落大时间 + 6 套简笔画 + 弧线开关）
- [ ] P1 MIP 64 色量化预览模式（原始色 vs 量化色对比）
- [ ] P1 一键复制短码 + 粘贴指引文案（Garmin Connect 设置项位置说明）
- [ ] P2 部署到 Cloudflare Pages，产出可分享 URL
- [ ] P2 5 种字体在网页端的等效预览（Web Font 近似，标注与真机字库差异）

## 3. Partition 2 · 字体与矢量资源（`Komorebi\02_font_and_vector_assets\`）

- [ ] P1 编写 `build_fonts.py`（Pillow）：TTF → Garmin `.fnt + .png`，仅导出 `0-9 :`
- [ ] P1 字符集与体积校验：单套字库 ≤ 8KB，超出即报错
- [ ] P2 5 套风格字库产出（裂开数字 / 宋体衬线 / 硬派黑体 / 八段数码管 / 辉光管）
- [ ] P3 自动特效脚本：为任意 TTF 生成"中间裂开"镂空与数码管网格镂空

## 4. Partition 3 · 表盘工程（`Komorebi\01_watchface_app\`）

- [ ] P0 `ThemeManager.mc` 短码解析：非法输入必须安全回落到默认主题，不得抛异常
- [ ] P0 `TimeRenderer.mc` 错落大时间排版（小时居左偏中 / 分钟贴右弧 / 秒钟补齐落差）
- [ ] P0 `WatchFaceView.mc` AOD 息屏保护：休眠隐藏秒针与重度图层
- [ ] P1 秒钟 `onPartialUpdate` 局部裁剪刷新（省电）
- [ ] P1 `MinimalBgDrawer.mc` 6 套矢量简笔背景（B1~B6）与 B0 自动跟随天气/日出日落
- [ ] P1 `DataFieldsDrawer.mc` 顶部电池+天气、底部身体数据矩阵（HR/BB/压力/步数/卡路里/血氧/日期）
- [ ] P1 MIP 64 色最近邻吸附，确保与网页预览零色差
- [ ] P2 左右弧形进度条三档开关（关闭 / 细弧 / Enduro 分段）
- [ ] P2 接入 P2 分区产出的字库到 `resources\fonts\` 并做多字体切换
- [ ] P3 真机续航实测与降频策略调优

## 5. 集成与验收

- [ ] P0 模拟器 `F5` 跑通全链路：短码 → 解析 → 换肤
- [ ] P1 `Build for Device` 导出 `.prg` 并拖入 `/GARMIN/APPS/` 真机验收
- [ ] P1 网页 → Garmin Connect → 手表 配色同步链路实测（延迟 < 1s）
- [ ] P2 对照本文件输出 `TODO_missing.md` 盲区清单
