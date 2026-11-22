# Komorebi — 任务成果与阶段记录 (result.md)

> **Append Only**：各 AI Agent 完成一个分区任务后，按下方格式**追加**记录（勿改写历史）。
> 格式源自 [`ProjectManagementTemplate/RESULT_TEMPLATE.md`](ProjectManagementTemplate/RESULT_TEMPLATE.md)。
> 局部临时看板 `TODO_PARTITION_{N}.md` 在验证通过后须删除，其成果沉淀到本文件。

---

## 任务执行记录

---

### 记录 1：仓库文档体系与工作流初始化（Partition 0: 仓库根）

* **时间**：`2026-11-20 (UTC+8)`
* **客户端（Agent）**：`VS Code Copilot`
* **背景与实现**：
  - 目录重构后（表盘独立顶级目录、网页与文档提升为共享分区），同步全部文档并引入多智能体协同研发体系。
  - **核心成果与组件实现**：
    1. **`README.md`**：重写为仓库总览与索引，工作流程迁出，仅保留阶段速览表。
    2. **`WORKFLOW.md`**：基于 `ProjectManagementTemplate/WORKFLOW_GUIDE.md` 定制，定义 P0 契约区 / P1 网页 / P2 字库 / P3 表盘 的目录锁矩阵、单智能体 SOP、管控节奏与 Garmin 专属注意事项。
    3. **`DECISIONS.md`**：归档 DEC-001~006（短码协议、纯矢量背景、MIP 双端吸附、11 字符字库、目录组织、双分辨率基准）。
    4. **`TODO.md`**：按分区拆解 P0~P3 待办。
    5. **`AI_TASKS.md` / `BUGS.md`**：分区提示词工单与缺陷追踪骨架。
    6. **`Komorebi/README.md`、`Komorebi/PROJECT_PLAN.md`、`Docs_and_Specs/JAPANESE_PALETTE_SPEC.md`**：路径引用更新为新结构。
* **验证**：全仓库 Markdown 已无 `03_cloudflare_palette_web` / `04_docs_and_specs` 旧路径残留。
* **遗留问题**：`Cloudflare_page\` 与 `02_font_and_vector_assets\` 目前为空目录，待 P1 / P2 分区开工。

---

### 记录 2：F2 衬线字体流水线（BMFont）+ 表盘端衬线大时间渲染器（Partition 2 + Partition 3）

* **时间**：`2026-11-22 (UTC+8)`
* **客户端（Agent）**：`LM Studio Code`
* **背景与实现**：
  - THEME_PROTOCOL 的 `F2`（宋体 / 明朝体·衬线）此前无实现，表盘只有矢量段码。本次打通「TTF → BMFont → Monkey C 渲染」全链路；参考项目以 git submodule 挂在 `reference/Segment34mkII`（其 `.fnt` + 黑底调色板 PNG 是格式权威样本）。
  - **核心成果与组件实现**：
    1. **`Komorebi/02_font_and_vector_assets/build_fonts.py`**：候选字体表内置授权状态（IPA OFL / SIL OFL 标 `OK`，Windows / 方正字体仅 `预览`，禁止打包）；真实墨迹包围盒度量（Pillow 默认锚点是 left-ascender，必须显式 `anchor="ls"`，且 CJK/TTC 的 `textbbox` 会膨胀到前进量宽度，改为逐像素取极值）；BMFont `.fnt` + 黑底色键调色板 PNG 产出；`fonts.xml` 原位 upsert（`antialias="true" filter=" 0123456789:"`）。
    2. **字高三向拟合 `tier_heights()`**：CIQ 位图字体不参与缩放，故按 DEC-006 双基准烘六档固定字号；大时字高同时受「≤34% 屏高」（= `SegmentClock.digitH`）与「组合块 ≤72% 屏宽」（= `SegmentClock.maxW`）约束反推 —— 明朝体前进量 ≈0.62x 字高，比矢量段码（0.46x）宽，只按屏高烘字会让 HH:MM 顶满两侧、压到上下数据字段。默认 `--tracking -0.15` 收紧字距换回字高，下限锁「墨迹宽 +2px」。
    3. **产物**：`resources/fonts/f2_mincho_biz_{big,mid,mini,mip_big,mip_mid,mip_mini}.fnt|.png`（BIZ UDMincho Medium，IPA OFL）。字高 `134/96/24`（AMOLED 454）与 `77/55/14`（MIP 260），单套 2.3~6.2KB，全部满足 DEC-004 的 8KB 硬上限；墨迹灰阶默认 4 档（`--ink-levels`，6 档时 big 会破预算）。
    4. **`source/SerifClock.mc`**：位图字体大时间渲染器。三档字库按屏高选择、任一档加载失败即整体回退；布局与 `SegmentClock` 同构（HH: 大字在左 + MM 小字右上 + SS 迷你垫底，配色沿用 colorHour/colorMin/colorSec）。
    5. **`source/TimeRenderer.mc`**：分发层，`theme.fontId == 2` 走 SerifClock，否则/失败回退 SegmentClock；`WatchFaceView.onUpdate` 改为调用 `TimeRenderer.draw`。
    6. **`02_font_and_vector_assets/preview_serif_layout.py`**：无模拟器条件下的离线版面对账脚本 —— 直接读已产出的 `.fnt/.png`，按渲染器同一套数学画两个基准屏并打印版面数字（是否溢出）。
* **验证**：
  - `monkeyc -d fr965`（MIP）与 `-d fenix7` 均 BUILD SUCCESSFUL；`.prg` 内确认六档字库均已打包。
  - 版面对账：AMOLED 454 → 组合块宽 323/454（留白 65px），MIP 260 → 185/260（留白 37px），均在 72% 横向预算内；产物图 `Komorebi/progress_shots/2026-11-22_F2_serif_layout.png`，选角对比图 `2026-11-22_F2_serif_candidates.png`。
  - SDK 9.3 API 实测（编译探针）：`Dc.getTextWidth()`、`Dc.setTextBaseline()`、`Graphics.TEXT_BASELINE_*` **均已不存在**，只能用 `getTextWidthInPixels(text, font)` / `getFontHeight(font)` + `TEXT_JUSTIFY_CENTER|VCENTER` 中心点定位；`.mc` 里引用资源必须写 `Rez.Fonts.x`（一旦 `import Toybox.Lang`，`@Fonts.` 会被解析成 `Toybox.Lang.Fonts`）。已补进 `Docs_and_Specs/GARMIN_DRAWING_RULES.md`。
* **遗留问题**：
  - 本机无 Connect IQ 模拟器，真机/模拟器上的字形位置与 `antialias="true"` 实际灰阶表现待验证（当前为离线数学对账）。
    （此条已在记录 3 推翻：SDK 目录内一直带着 `bin\simulator.exe`，可脚本化驱动。）
  - 六档字库都放在无限定符的 `resources/fonts/`，每台机型都会带 6 套（合计 23KB）；后续可迁到 `resources-<device>/` 只随包 3 套。
  - 中间尺寸屏（如 fenix 7 的 320x360 MIP）会拿到按 260 基准烘的字，视觉占比偏小；需要更饱满时补一条中间档即可。
  - 顶部/底部数据字段内容与 F2 字体的联动尚未开工（用户明确暂缓）。

---

### 记录 3：模拟器实机验证链路打通 + F2 衬线大时间落墨对账（Partition 3）

* **时间**：`2026-11-22 (UTC+8)`
* **客户端（Agent）**：`LM Studio Code`
* **背景与实现**：
  - 记录 2 的全部结论都是离线数学，缺实机证据；且出现过「push 成功但画面没变化」的假象。本次把模拟器彻底脚本化，拿到**设备逻辑分辨率一比一**的屏幕位图并做像素对账。
  - **核心成果与组件实现**：
    1. **`Komorebi/01_watchface_app/tools/push_sim.ps1`**：清场（杀 `simulator` + monkeydo 残留 `java`）→ 写 `simulator.ini` 的 `LastUsedDevice` → 编译 → 启动模拟器 → `monkeydo` 推送并把 app stdout 落盘。
       **必要性**：`monkeydo` 只认占用调试端口（10642）的那一个模拟器实例，手工多开就会出现「push 成功、看的却是另一个窗口」的错位现象。
    2. **`Komorebi/01_watchface_app/tools/sim_verify.py`**：
       - `shot` —— 模拟器菜单是原生 Win32 菜单（wxWidgets），可直接 `PostMessage(hwnd, WM_COMMAND, id)` 触发，无需鼠标：`File → Save Screen Capture` 的 **命令 ID = 5003**；弹出的 `Save Screenshot` 是标准文件对话框（class `#32770`），往文件名 Edit 写全路径再点「保存」，即得 fr965 的 **454x454 精确位图**。这比抓窗口可靠 —— DPI 非感知进程 `EnumWindows + ImageGrab` 拿到的窗口矩形会被系统缩放（实测 873x1246 vs 真实 454 屏），比例全错。
       - `check` —— 按主题色分离墨迹并断言排版契约：黑 `#1C1C1C`=小时、朱红 `#B7282E`=冒号+分钟（同色，靠列宽与「紧贴小时右侧」区分）、灰 `#787878`=秒钟（先用时/分墨迹膨胀 3px 排除抗锯齿毛边）；只判与缩放无关的量：三档字高、分/时=0.72、秒/主档=0.18、整块 ≤72% 屏宽、主体垂直居中。
       - **坑**：朱红笔画细端只剩几级灰阶，颜色容差必须放宽到 `sum|Δ|≤190`（黑/灰用 90/60），否则明朝体的细瘦字形（如 `1`）会被阈值切掉一半；顶部/底部数据域也用同一个朱色，量大时间前要先按小时的 y 范围裁带。
* **验证**（fr965 / 454x454，主题默认「昼·壱」= F2 路径）：
  - app stdout：`[SerifClock] SERIF tier=amoled 屏=454x454 字高=134/96/24 版面宽=327` —— 走的是衬线分支、三档字库全部加载成功、无异常、未回退段码。
  - `sim_verify.py check`：**8/8 PASS** —— 小时墨迹高 132（烘 134）、分钟 92（96）、秒钟 24（24）；分/时 = 0.70，秒/主档 = 0.18；整块 x=85..365 = 61.7% 屏宽（预算 72%，**无需再收紧字距**，记录 2 里担心的 `327 > 326.9` 只是排版框宽度，实际墨迹有余量）；主体中心 y=228 vs 屏心 227；小时两字之间留 4px 空隙、无粘连。
  - 结论：`lineHeight == base == 数字墨迹高` 的紧字模契约在真机渲染下成立，`getFontHeight()` 就是视觉字高，中心点定位方案（SDK 9.3 无 baseline API）落位准确。
* **遗留问题**：
  - `resources/drawables/bg_1..6.png` 是 SD 产物（360x135 RGBA），既没写进 `drawables.xml`、也被 `source/*.mc` 零引用，因此**根本不可能出现在表盘上**；且单张按 2bpp 展开约 95KB，六张 ≈570KB，远超 watchFace 的 128KB（131072B）内存上限 —— 与 DEC-002「背景保持纯矢量」冲突，需要决策：改造成矢量/极小调色板条带后接入 B 槽，或从仓库删除。
  - 字形观感层面发现一处字体本身的问题：BIZ UDMincho 的 `1` 墨迹在 96px 档只有 ~11px 宽（同档 `4` 有 53px），是一根明显偏细偏斜的笔画，含 `1` 的时间会显得左右配重不均；换字族或给 `1` 做视觉补偿待用户定夺。
  - 中间尺寸屏（fenix 7 320x360）与 per-device `resources-<device>/` 分包仍未处理，同记录 2。

### 记录 4：字库重烘后的复验 + 校验器改写成「几何对账」型（Partition 3）

* **背景**：本轮重新编译（`BUILD SUCCESSFUL`，`bin\komorebi_fr965.prg` 438,476B）并干净拉起模拟器
  （先杀残留 `simulator`/`java`，写 `LastUsedDevice=fr965`，等窗口标题出现设备名再 monkeydo），
  app stdout：`[SerifClock] SERIF tier=amoled 屏=454x454 字高=124/78/34 版面宽=313` —— F2 衬线分支仍生效。
* **字库来源变更**：磁盘上的 `.fnt/.png` 被 `02_font_and_vector_assets\fix_fonts.py`（未入库、作者待认）重烘成
  big/mid/mini = **124/78/34**、mip = **72/46/22**，并给 `1` 与 `:` 缩小了 `xadvance`（×0.78 / ×0.65）以缓解
  记录 3 提到的「`1` 太细」问题；同时它也**绕过了 build_fonts.py 的授权标记与 8KB 预算检查**，实测
  big 档 `.png+.fnt` = **17,349B（RGBA）**、mid 11,024B、mip_big 10,177B，三处超 DEC-004 的 8KB/套上限。
* **校验器重写**（`tools\sim_verify.py::check`）：旧的「到主题色的欧氏距离 + 整行 y 带」分色在真图上不可靠 ——
  暖底 `#F6F2F6` 的黑字抗锯齿毛边本身偏暖（`#524c4a`），会被判成朱红而把整行糊成一坨。现改成三条**通道特征**
  判据 + 连通组件：墨黑＝小时（`lum≤60` 且 `R−max(G,B)<25`）、朱红＝冒号/分钟（`R−max(G,B)>45`）、
  中性灰＝秒钟（三通道互差 <12）；再用**填充率**把水彩晕染切掉（字形 0.37~0.66，晕染 0.02~0.10），
  用 `_columns(max_vgap=0.5·字高)` 把明朝体冒号的两个菱形点并成一个整字（不限制纵向间隙就会把数字下方 40px 的
  朱砂点缀并进字里，量出 129px 的假字高）。断言全部从 `.fnt` 度量 + `SerifClock.mc` 公式现推，不再写死像素：
  小时/分钟/秒钟字高 == 三档 `lineHeight`、顶边 == `h·0.25`、冒号中心 == `topY+digitH/2`、
  冒号落墨区间 == `[yoffset, yoffset+height]`、共顶线、分/时 == 烘焙比、秒钟右缘贴分钟块右缘、左右留白相等、≤72% 屏宽。
* **验证**（fr965 / 454x454，新构建 + 新字库）：**12/12 PASS** ——
  小时 x=79..222 y=113..239（字高 126/123，烘 124），冒号 x=238..274 y=133..220（中心 y=176 vs 期望 175；
  落墨 133..220 vs 字库 133..217），分钟 x=291..377 y=115..193（字高 78 == 烘 78，分/时 = 0.62 ≈ 烘焙比 0.63），
  秒钟 x=343..381 y=204..241（灰 `#787878`，字高 37 vs 烘 34，右缘 381 vs 分钟 377 = 步进盒余量），
  整块 x=79..381 = **66.5% 屏宽**、左留白 79 vs 右留白 73（居中偏差 ≤3px）。
* **灵敏度回归**：同一套判据跑旧烘焙（134/96/24）时期的截图，精确地在「三档字高」上报 FAIL
  （134≠124、87≠78、24≠34），证明 PASS 不是判据太松；也说明**截图与磁盘 `.fnt` 必须同批**，否则期望值会随字库漂移。
* **待用户拍板**：① 字体来源 —— 用 `build_fonts.py` 重烘恢复 8KB 预算 + 授权闸门，还是采纳 `fix_fonts.py`
  的度量并改写 DEC-004/预算检查；② `bg_1..6.png` 与 DEC-002 的冲突处理（见记录 3 遗留问题）。

### 记录 5：位图背景上线 + 字库再放大后的复验（Partition 4）

* **本轮变更**（用户在仓库外自行处理）：① `02_font_and_vector_assets\process_backgrounds.py` 产出六张
  RGBA 水彩景物贴片，落进 `resources/drawables/bg_1..6.png`（360x135 RGBA，75~112KB/张），并在
  `drawables.xml` 里声明成 `BgScene1..6`（`dithering="none"`），`MinimalBgDrawer.mc` 改写成「按 mode 取图 → 缓存
  → `drawBitmap((w-bw)/2, h·0.50)`」的位图抽屉；② 字库重烘成 big/mid/mini = **181/113/46**、mip = **104/65/28**，
  `SerifClock.mc` 的主体顶边从 `h·0.25` 上移到 `h·0.21`，给下半区的景物让位。**DEC-002「背景保持纯矢量」本轮被用户否决**。
* **构建**：`BUILD SUCCESSFUL` —— `komorebi_fr965.prg` **441,340B**、`komorebi_fenix7.prg` 426,716B；
  app stdout `[SerifClock] SERIF tier=amoled 屏=454x454 字高=181/113/46 版面宽=401`，仍走衬线分支、未回退段码。
* **校验器补强**（`tools\sim_verify.py::check`）：
  1. `topY` 的比例改成**从 `SerifClock.mc` 源码正则读出**（`topY = (h * x)`），工具里不再存第二份常量；
  2. `_columns()` 增加 `max_h`：逐块合并时纵向间隙是拿「已合并框」的下缘比的，会滚雪球 —— 冒号点与景物朱砂点缀
     实测间隙 74px < vgap 90px，被并成 217px 的假字导致冒号「查无此列」。现在按「这一列最多就是冒号自己那么高」
     （`max_h = height+8`）封顶，并把检测判据从「居中才算冒号」改成「落在小时右缘→分钟左缘的 x 区间内就算」，
     居中偏差交给断言去量化；找不到时会把该区间内的候选列全部打出来，绝不留一句查无实据的报错；
  3. 两处 FAIL 各自附 `INFO` 归因（字模 yoffset / 烘焙档位），避免把烘焙问题误报成渲染器 bug。
* **验证**（fr965 / 454x454，同批构建 + 同批字库）：**10 PASS / 2 FAIL** ——
  小时 x=29..246 y=95..278（字高 183/178 vs 烘 181），顶边 95 == `h·0.21`，分钟字高 114 vs 烘 113 且与小时共顶线，
  分/时 = 0.62 == 烘焙比，秒钟灰字 x=367..426 字高 45 vs 烘 46 且右缘贴住分钟块（424/426），整块左右留白 29/28px；
  景物贴片确实画出来了：`x=47..407 y=300..360` 带内非底色像素 **13.1%**，其中 **71%** 带色相（青 `#94babd`/`#5a9d9c`
  + 朱 `#b42829`），与旧矢量抽屉那种「只有细黑线」的底部完全不同。
* **两处真缺陷**：
  1. **冒号铅垂偏低 25px** —— 实测墨迹 y=148..274，与字库期望 `yoffset=53 → 148..272` 完全吻合，所以不是渲染器定位错，
     而是 `:` 这个字模在 181 的紧格子里没居中：`height=124`、理想 yoffset = `(181-124)/2 = 28`，现在是 53。
     CIQ 用 `TEXT_JUSTIFY_VCENTER` 按 lineHeight 居中，字模在格子内偏下，屏幕上就跟着偏下；烘一行代码就能修（短字统一
     `yoff = (lineHeight - height) // 2`）。
  2. **横向占用 87.4%**（x=29..426）超出 SegmentClock 的 0.72 屏宽预算 —— 同样不是渲染器算错，主档字高
     `181/454 = 39.9%` 已超 DEC-006 的 34%，块宽随字高等比例放大。要么按 `build_fonts.py::DIGIT_H_RATIO` 重烘，要么正式修订 DEC-006。
* **新增待拍板**：① DEC-004「每套字库 ≤8KB」仍被违反（big **24,025B**、mid 14,878B、mip_big 13,649B、mip_mid 8,927B；
  mini/mip_mini 合格）；② DEC-006 的高度比例（实测 39.9% vs 规定 34%）；③ 六张 RGBA 背景在 MIP/低内存机型上的可用性 ——
  单张 360x135 RGBA 解码后约 **190KB**（磁盘 PNG 75~112KB），`MinimalBgDrawer` 虽只缓存一张，仍需按目标机型实测；
  ④ `fix_fonts.py` 仍绕过授权闸门与墨迹度量，字库来源未收口。

