# Garmin Connect IQ (Monkey C) 绘图防坑铁律与标准食谱 (GARMIN_DRAWING_RULES.md)

> **适用范围**：本规范为 `Komorebi\01_watchface_app`（Monkey C 表盘端）与 `Cloudflare_page`（网页 Canvas 预览端）的**强制性几何与 API 契约**。
> **背景教训**：Garmin `Toybox.Graphics.Dc` 的底层光栅化器与 HTML5 Canvas / Android Skia 有巨大差异（无默认抗锯齿路径合并、角度逆时针定义、笔刷状态全局污染、无 `lineCap` 端点修饰）。任何 AI Agent 或开发者编写绘图代码前，**必须逐条遵守以下铁律**（第八条为 SDK 9.3 实测文本 / 字库 API 现实）。

---

## 一、 圆形表盘安全区与垂直分区铁律（Safe Zones & Layout Grid）

所有坐标一律采用归一化比例 `ratio`（`0.000 ~ 1.000`），实际像素由 `(w * ratio).toNumber()` 或 `(h * ratio).toNumber()` 计算。

### 1. 圆形表盘弦长公式（防贴边裁切）
在直径为 $W$（半径 $R = W / 2$）的圆形表盘上，任意高度 $Y$（归一化值 $y \in [0, 1]$）处的**可用水平弦长比例**为：
$$\text{chordRatio}(y) = 2 \times \sqrt{0.25 - (y - 0.5)^2}$$
**安全边距（Safe Padding）**：所有文字和图标距离圆形外缘必须至少保留 `0.06 * W` 的呼吸留白。

| 分区名称 | 垂直范围 ($y = Y/H$) | 可用水平安全区 ($x = X/W$) | 核心承载内容与避让规则 |
| :--- | :--- | :--- | :--- |
| **1. 顶部状态区 (Top Zone)** | `0.10 ~ 0.20`<br/>*(基准线 `y = 0.14`)* | `0.26 ~ 0.74` | 左侧电池（图标+百分比）、居中日期（`MM/DD`）、右侧气温。**严禁超出 `[0.24, 0.76]`，否则会被圆角表圈切掉！** |
| **2. 右上意境区 (Upper-Right Motif)** | `0.19 ~ 0.30` | `0.62 ~ 0.82` | 简笔画远景符号（日轮 / 弦月 / 流云 / 雨丝 / 寒星）。必须避开上方 `y=0.14` 的气温与下方 `y=0.31` 的主时间。 |
| **3. 核心时间区 (Center Clock Zone)** | `0.31 ~ 0.63`<br/>*(高度 `0.32 * H`)* | `0.12 ~ 0.88` | **主从错落大时间**：左侧大号小时 `HH`（高 `0.32`），中间冒号，右上中号分钟 `MM`（高 `0.20`），右下小号秒钟 `SS`（高 `0.10`）。 |
| **4. 简笔地景带 (Landscape Band)** | `0.64 ~ 0.71` | `0.16 ~ 0.84` | **黄金留白画布**：富士山脊、源氏霞云、水波涟漪、山坡眠猫**全部绘制在此水平带内**！向上不压时间，向下不碰数据。 |
| **5. 底部数据矩阵 (Bottom Data Zone)** | `0.73 ~ 0.90`<br/>*(Row1 `0.76`, Row2 `0.85`)* | Row1: `0.20 ~ 0.80`<br/>Row2: `0.26 ~ 0.74` | 2×2 身体数据矩阵（微型矢量图标 + 数值）。**严禁在此区域画任何背景横线！** |

---

## 二、 铁律 1：`dc.drawArc` 极坐标系与顺/逆时针陷阱

### ❌ 昨天的翻车原因
把 Garmin 的 `drawArc` 当成了 CSS/Android 角度（以为 0° 在正上方、顺时针递增），写出了 `dc.drawArc(cx, cy, r, ARC_CLOCKWISE, 130, 95)`，本想画 325° 的大禅圈，结果只在左上角 10 点半到 11 点半画了一小段 35° 的破弧线，还直接穿过 `50%` 电量文字！

### ✅ Garmin `dc.drawArc` 唯一正确坐标系
```text
                  90° (12点钟 / 正上)
                      │
       135° (10点半)   │   45° (1点半)
             ╲        │        ╱
               ╲      │      ╱
180° (9点钟/正左) ─────┼───── 0° (3点钟 / 正右)
               ╱      │      ╲
             ╱        │        ╲
       225° (7点半)    │   315° (4点半)
                      │
                 270° (6点钟 / 正下)
```
1. **0° 永远在 3 点钟方向（正右）**。
2. **角度数值沿【逆时针】方向递增**：`0°(右) -> 90°(上) -> 180°(左) -> 270°(下) -> 360°(右)`。
3. **`attr` 方向参数含义**：
   - `Graphics.ARC_COUNTER_CLOCKWISE`（逆时针画弧）：从 `degreeStart` 沿**角度增大**的方向画到 `degreeEnd`。
   - `Graphics.ARC_CLOCKWISE`（顺时针画弧）：从 `degreeStart` 沿**角度减小**的方向画到 `degreeEnd`。

### 📋 常用弧线标准速查公式（直接照抄，禁止自己瞎算）

| 需求场景 | 起点位置 | 终点位置 | 扫掠方向 (`attr`) | `degreeStart` | `degreeEnd` | 扫过圆心角 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **圆相禅圈 (Ensō)**<br/>*(左下 7点~8点留缺口)* | 8点钟 (`205°`) | 7点钟 (`235°`) | `ARC_CLOCKWISE`<br/>*(顺时针绕一整圈)* | `205` | `235` | `330°` |
| **左侧进度弧 (Left Arc)**<br/>*(由下往上增长：7点半 -> 10点半)* | 7点半 (`220°`) | `220 - pct * 80`<br/>*(满格 10点半 `140°`)* | `ARC_CLOCKWISE`<br/>*(顺时针向上)* | `220` | `(220 - pct * 80).toNumber()` | `0° ~ 80°` |
| **右侧进度弧 (Right Arc)**<br/>*(由下往上增长：4点半 -> 1点半)* | 4点半 (`320°`) | `(320 + pct * 80) % 360`<br/>*(满格 1点半 `40°`)* | `ARC_COUNTER_CLOCKWISE`<br/>*(逆时针向上)* | `320` | `((320 + pct * 80).toNumber()) % 360` | `0° ~ 80°` |
| **上半圆拱 (Top Dome)** | 9点钟 (`180°`) | 3点钟 (`0°`) | `ARC_CLOCKWISE` | `180` | `0` | `180°` |
| **下半圆碗 (Bottom Bowl)** | 9点钟 (`180°`) | 3点钟 (`0°`) | `ARC_COUNTER_CLOCKWISE` | `180` | `0` | `180°` |

> **⚠️ 0% 进度特判铁律**：当 `degreeStart == degreeEnd` 时，Garmin 某些固件会把 `0°` 弧画成 **360° 整圆**！因此在画动态进度弧前，**必须判断 `if (pct <= 1) { return; }`**。

---

## 三、 铁律 2：画笔状态污染与重置（PenWidth Reset Rule）

### ❌ 昨天的翻车原因
`SegmentClock.drawDigit` 里设置了 `dc.setPenWidth(t)`（`t ≈ 14px`），紧接着在 `drawColon` 里调用 `dc.drawRectangle(...)` 画空心方点，**却忘了把 `penWidth` 重置为 `1`**，导致空心小方点被 `14px` 的巨粗边框向外膨胀成了两块巨大的红砖！

### ✅ 强制规范
1. **实心几何块一律用 `fill*`**：画冒号点、进度块、实心日轮、图标填充时，**必须使用 `dc.fillRectangle`、`dc.fillRoundedRectangle`、`dc.fillCircle`、`dc.fillPolygon`**（`fill*` 不受 `penWidth` 影响，边缘最干净）。
2. **用完粗画笔立即归位**：任何函数只要修改了 `dc.setPenWidth(k)`（$k > 1$），在该函数结束前**必须显式调用 `dc.setPenWidth(1)`**！

---

## 四、 铁律 3：自绘几何数码管必须用 `fillPolygon` 六边形段码（严禁用 `drawLine`）

### ❌ 昨天的翻车原因
用 `dc.setPenWidth(t)` + `dc.drawLine` 画七段数码管，因为 `drawLine` 是平头矩形（Butt Cap），横竖交界处要么重叠发黑、要么退缩 `t/2` 后露出十字断裂缺口。

### ✅ 标准六边形斜切段码（Chamfered Hexagon Segments）食谱
每个段码由 **6 个顶点** 的多边形 `dc.fillPolygon(pts)` 构成，两端呈 45° 钻石尖角，段与段之间留 `g = 1 ~ 2px` 的斜缝（Miter Gap），拼合后严丝合缝，完全媲美真实液晶屏/现代几何字体：

```text
      (x+t/2+g, y) ─────────────────── (x+w-t/2-g, y)
         ╱                                         ╲
(x+g, y+t/2)                                     (x+w-g, y+t/2)
         ╲                                         ╱
      (x+t/2+g, y+t) ───────────────── (x+w-t/2-g, y+t)
```

- **水平段函数 `fillHSeg(dc, x1, x2, cy, t)`**（中心线为 `cy`，左端点 `x1`，右端点 `x2`，厚度 `t`，半厚 `h = t / 2`）：
  ```monkeyc
  var h = (t / 2).toNumber();
  if (h < 1) { h = 1; }
  dc.fillPolygon([
      [x1, cy],
      [x1 + h, cy - h],
      [x2 - h, cy - h],
      [x2, cy],
      [x2 - h, cy + h],
      [x1 + h, cy + h]
  ]);
  ```
- **垂直段函数 `fillVSeg(dc, cx, y1, y2, t)`**（中心线为 `cx`，上端点 `y1`，下端点 `y2`，厚度 `t`，半厚 `h = t / 2`）：
  ```monkeyc
  var h = (t / 2).toNumber();
  if (h < 1) { h = 1; }
  dc.fillPolygon([
      [cx, y1],
      [cx + h, y1 + h],
      [cx + h, y2 - h],
      [cx, y2],
      [cx - h, y2 - h],
      [cx - h, y1 + h]
  ]);
  ```

---

## 五、 铁律 4：错落大时间排版与数字 `1` 视觉居中（Optical Kerning & Spacing）

### ❌ 昨天的翻车原因
1. **漏算间距**：`totalW` 只算了小时里的 2 个 `gap`，**冒号与分钟之间、分钟十位与个位之间、秒钟十位与个位之间的间距全部是 `0`**，导致冒号贴死分钟 `2`，秒钟 `3` 和 `4` 直接重叠成乱码！
2. **数字 `1` 的左侧幽灵空白**：数字 `1` 只画在字框最右侧 `x + dw`，当显示 `11:21` 时，左边空出整整一个字宽，两个 `1` 之间隔了 `dw + gap`，整个表盘重心向右塌陷。

### ✅ 黄金错落排版公式（严格 5 段间距 + 数字 `1` 动态紧缩）

设主时间总高度 `digitH = (h * 0.32).toNumber()`：

1. **三层字号比例**：
   - **小时 (`HH`)**：高 `digitH`，标准字宽 `digitW = (digitH * 0.48).toNumber()`，笔画厚 `thick = (digitH * 0.11).toNumber()`，字间距 `hGap = (digitW * 0.22).toNumber()`。
   - **冒号 (`:`)**：槽宽 `colonW = (digitW * 0.28).toNumber()`，左右各留一个完整 `hGap`！方点边长 `dot = thick`，上下方点中心位于 `topY + digitH * 0.35` 与 `topY + digitH * 0.65`。
   - **分钟 (`MM`)**：高 `minH = (digitH * 0.62).toNumber()`，标准字宽 `minW = (minH * 0.50).toNumber()`，笔画厚 `minT = (minH * 0.12).toNumber()`，**分钟两字间距 `minGap = (minW * 0.24).toNumber()`（绝不可为 0！）**。
   - **秒钟 (`SS`)**：高 `secH = (digitH * 0.26).toNumber()`，标准字宽 `secW = (secH * 0.54).toNumber()`，笔画厚 `secT = (secH * 0.15).toNumber()`（最小 `2px`），**秒钟两字间距 `secGap = (secW * 0.28).toNumber()`（绝不可为 0！）**。
   - **垂直对齐约束**：
     - 分钟顶部与小时顶部平齐：`minTopY = topY`（息屏隐藏秒钟时，`minTopY = topY + (digitH - minH) / 2`）。
     - 秒钟底部与小时底部平齐：`secTopY = topY + digitH - secH`。
     - 秒钟水平右对齐于分钟右边缘：`secTotalW = adv(s1) + secGap + adv(s2)`，`secStartX = minRightEdge - secTotalW`。

2. **数字 `1` 的动态紧缩字宽 (`getDigitAdvance`)**：
   - 普通数字（`0, 2..9`）的占用宽度为标准字宽 `dw`，在 `[x, x + dw]` 内绘制。
   - **数字 `1` 的占用宽度紧缩为 `dw * 0.36`**！并且数字 `1` 的竖线绘制在该紧缩槽位的**水平正中央 `x + advance / 2`**（而不是靠右边缘）。
   - **效果**：无论是 `11:21`、`01:11` 还是 `23:59`，每一位的视觉间距完全均匀，整个 `HH : MM/SS` 组合的真实像素宽度 `totalW` 由实际数字宽度累加得出，再通过 `startX = (w - totalW) / 2` 严格水平居中！

---

## 六、 铁律 5：微型矢量图标库与顶/底数据排版（Micro-Vector Icons）

底部和顶部数据区**严禁只写干瘪的 `"HR 80"` 纯文本**。每个数据槽位由 **左侧微型矢量图标 (`10x10` ~ `14x14` 相对尺寸) + 右侧数值文字** 组成：

| 槽位 | 位置坐标 $(cx, cy)$ | 图标颜色 | 微型矢量绘制方法（纯代码几何，零图片） | 文字内容 |
| :--- | :--- | :--- | :--- | :--- |
| **顶部左：电池** | `(0.29 * w, 0.14 * h)` | 正常 `colorData`<br/>`≤20%` `colorAccent` | 圆角外框 `16×9px` + 右侧极耳 `2×4px` + 内部按电量比例 `fillRectangle` | `"50%"` |
| **顶部中：日期** | `(0.50 * w, 0.14 * h)` | `colorData` | 无图标，干净展示月/日 | `"11/20"` |
| **顶部右：气温** | `(0.71 * w, 0.14 * h)` | `colorData` | 小太阳/云点图标或直接紧跟温度符号 | `"9°C"` |
| **底排1左：心率 (HR)** | `(0.33 * w, 0.77 * h)` | `colorAccent` (茜红) | **矢量小爱心**：左右两个 `fillCircle(r=3)` + 下方倒三角 `fillPolygon` | `"80"` |
| **底排1右：身体电量 (BB)** | `(0.67 * w, 0.77 * h)` | `colorMin` / `colorAccent` | **矢量小闪电**：6 顶点折角闪电 `fillPolygon` | `"88"` |
| **底排2左：步数 (STEPS)** | `(0.34 * w, 0.86 * h)` | `colorData` | **矢量双脚印/行者**：两个错位小椭圆点或简洁阶梯图标 + 步数 | `"6420"` / `"12.4k"` |
| **底排2右：压力 (STRESS)** | `(0.66 * w, 0.86 * h)` | `colorData` | **矢量脉冲菱形**：空心/实心小菱形图标 + 压力值 | `"35"` |

---

## 七、 铁律 6：MIP 64 色硬件最近邻吸附公式

MIP 反射屏每个 RGB 通道只有 `0x00 (0)`, `0x55 (85)`, `0xAA (170)`, `0xFF (255)` 四个合法台阶。
在 `ThemeManager.mc` 中，当检测到设备为 MIP 屏（或 `ForceMIPQuantize == true` 且非真彩屏）时，必须通过以下公式量化：
```monkeyc
// 单通道 (0~255) 映射到 0x00, 0x55, 0xAA, 0xFF
private function quantizeChannel(v as Number) as Number {
    // 阈值中点：42, 128, 213
    if (v < 43)  { return 0x00; }
    if (v < 128) { return 0x55; }
    if (v < 213) { return 0xAA; }
    return 0xFF;
}
```
> **注意**：AMOLED 机型（如 `fr965`, `fr265`, `epix2`, `venu3`，屏幕宽度 `>= 360` 或色深 `> 64`）应默认展示原生日本传统和色（24-bit 真彩），仅在 MIP 机型（屏幕宽度 `<= 280`）或用户强制开启 MIP 预览时吸附到 64 色！

---

## 八、 文本定位与自定义位图字体（SDK 9.3 实测 API 现实）

下列结论由 SDK 9.3（`connectiq-sdk-win-9.3.0-2026-10-20`）编译探针逐条验证，不是文档转述：

| 写法 | 结果 |
| :--- | :--- |
| `dc.getTextWidth(text)` | **不存在**（`Undefined symbol ':getTextWidth'`）。用 `dc.getTextWidthInPixels(text, font)` |
| `dc.setTextBaseline(...)` / `Graphics.TEXT_BASELINE_*` | **已全部移除**。不要再写「基线对齐」相关代码 |
| `@Fonts.xxx`（文件里只要有一句 `import Toybox.Lang;`） | 被解析成 `Toybox.Lang.Fonts` → `Cannot find symbol`。必须写 `Rez.Fonts.xxx` |
| `dc.getFontHeight(font)` / `dc.getTextWidthInPixels(text, font)` | 可用（API Level 1.0.0），自定义 BMFont 同样有效 |

### 1. 只用「中心点 + 双向居中」定位文本
`drawText(x, y, ...)` 的 `y` 语义不可依赖（不同 SDK / 字体类型不一致，且已无基线开关）。所有文本一律：
```monkeyc
dc.drawText(cx, cy, font, text, Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);
```
需要「左对齐 / 右对齐」时，用 `getTextWidthInPixels()` 量宽后自行换算中心点（`cx = left + w/2`），
分段着色（如小时与冒号异色）就分段各自居中，误差不会累积。

### 2. 自定义位图字体不缩放 —— 字号在构建期烘死
CIQ 的 BMFont 字库是**固定像素**位图，运行时拉伸只会糊。因此：
* 按 DEC-006 双基准（MIP 260x260 / AMOLED 454x454）各烘「大 / 中 / 迷你」三档，运行时只挑档不缩放；
* 每档字高由脚本 `build_fonts.py::tier_heights()` 同时按「≤34% 屏高」与「组合块 ≤72% 屏宽」（`SegmentClock.maxW`）反推 —— 衬线体前进量约 0.62x 字高，比矢量段码（0.46x）宽，只按屏高烘字会挤掉数据字段；
* `.fnt` 采用**紧字模契约**：`lineHeight == base == 数字墨迹高`，于是 `getFontHeight()` 直接等于视觉字高，排版无需再猜 ascent/descent；
* 字符集固定「空格 + `0-9 :`」（DEC-004），单套 ≤8KB，脚本内硬校验。

### 3. MIP 上的墨迹形态
黑 = CIQ 色键（透明），灰阶 = 抗锯齿强度，绘制颜色由 `dc.setColor()` 决定；字库 PNG 必须是「黑底白字」的调色板图（与 `reference/Segment34mkII` 一致），`fonts.xml` 里写 `antialias="true"`。

## 九、铁律 8：验证排版只能拿模拟器自绘位图，抓窗口不可信

* **抓窗口在 DPI 缩放下是错的**：DPI 非感知进程用 `EnumWindows + GetWindowRect + ImageGrab` 截模拟器，得到的是被系统虚拟化过的矩形（实测 fr965 窗口 873x1246，而屏幕只有 454x454），所有像素比例失真。要么先 `SetProcessDPIAware()`，要么干脆别抓窗口。
* **正道：让模拟器自己导出屏幕**。它的菜单是原生 Win32 菜单（wxWidgets），可以不走鼠标直接触发：

  ```python
  user32.PostMessageW(hwnd, WM_COMMAND, 5003, 0)   # File → Save Screen Capture，ID 实测 5003
  ```

  随后弹出标准文件对话框（class `#32770`），把目标全路径写进文件名 Edit（`WM_SETTEXT`）、再点「保存」按钮，即可得到**与设备逻辑分辨率一比一**的 PNG。实现见 `Komorebi/01_watchface_app/tools/sim_verify.py`。
* **推送前必须清场**：`monkeydo` 只连接占用调试端口的那一个模拟器实例；手工多开（或 VS Code 的 Run）会造成「push 成功但画面不变」的假象。用 `tools/push_sim.ps1`，它会先杀掉残留 `simulator` / `java` 再启动、编译、推送，并把 app 的 `System.println` 落到日志。
* **按色分离墨迹时的容差**：黑/灰主题色用 `sum|Δ| ≤ 60~90`，朱红（`#B7282E`）这类细笔画要放宽到 `≤190`；同色的多个元素（冒号与分钟、数据域高亮）要先按主体 y 范围裁带、再按列宽区分，否则会把数据域文字误判成时钟。
