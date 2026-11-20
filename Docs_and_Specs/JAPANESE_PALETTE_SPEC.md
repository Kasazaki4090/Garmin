# 日本传统色系 (日本の伝統色) 表盘色卡与 6 套日系简笔画规范

> 参考色库：[Japanese Traditional Colors (日本の伝統色)](https://www.color5.com/color-system/japanese-traditional-colors/)
> 本规范直接供 `Cloudflare_page`（网页调色器）与 `Komorebi\01_watchface_app\source\ThemeManager.mc` 调用。

---

## 一、 4 套默认日系昼夜主题色值表（含 AMOLED 原生色 & MIP 64色映射）

### 1. 昼 · 壱：【白练 · 茜素】(Shironeri & Akane) —— 和纸水墨朱印风
- **设计印象**：日本神社御朱印帐质感。白练和纸底，墨色主字，分钟如一方茜色朱印，远山简笔画如素鼠淡墨。
- **预设短码 (AMOLED)**：`F2-B0-A0-F3F3F2-1C1C1C-B7282E-787878-9EA1A3-524E4D-B7282E`
- **预设短码 (MIP 64色)**：`F2-B0-A0-FFFFFF-000000-AA0000-555555-AAAAAA-555555-AA0000`

### 2. 昼 · 弐：【鸟之子 · 青磁】(Torinoko & Seiji) —— 京都和纸与青瓷风
- **设计印象**：温润的淡卵壳色（鸟之子色）护眼底，搭配深沉的铁御纳户色主字与青磁色分钟，白茶色简笔线条。
- **预设短码 (AMOLED)**：`F1-B0-A0-EFEACC-2B373B-69B0AC-828282-BC9F77-494A41-69B0AC`
- **预设短码 (MIP 64色)**：`F1-B0-A0-FFFFAA-000055-00AAAA-555555-AA5500-555500-00AA55`

### 3. 夜 · 壱：【胜色 · 樱月】(Kachiiro & Sakura) —— 京都夜樱与蓝染风
- **设计印象**：深邃黑橡/胜色夜空底，卯之花白主字，分钟点缀温柔的樱色，蓝鼠色勾勒夜月与小猫简笔画。
- **预设短码 (AMOLED)**：`F3-B0-A0-0B1013-F7FCFE-FEDFE1-8899A0-566C73-ADADAD-F596AA`
- **预设短码 (MIP 64色)**：`F3-B0-A0-000000-FFFFFF-FFAAAA-5555AA-5555AA-AAAAAA-FF55AA`

### 4. 夜 · 弐：【消炭 · 琥珀宵】(Keshizumi & Kohaku) —— 昭和暖灯与辉光风
- **设计印象**：吕色暗底，砥粉暖米色主字与琥珀色分钟，搭配藤煤竹色背景线条，夜间看表极度护眼。
- **预设短码 (AMOLED)**：`F5-B0-A0-0C0C0C-F4DDA5-CA7A2C-9E9478-5A5359-9E9478-E2943B`
- **预设短码 (MIP 64色)**：`F5-B0-A0-000000-FFFFAA-FF5500-AA5500-555555-AAAA55-FFAA00`

---

## 二、 网页调色器内置「日本传统色」精选字典 (JSON 数据源规范)

网页调色盘将内置以下 6 大类共 **48 种经典日本传统色**，点击即可赋色：

| 色系分类 | 传统和色名称 (日文 / 罗马音 / HEX) | 推荐表盘用途 |
| :--- | :--- | :--- |
| **1. 白・灰・墨系**<br>*(和纸与水墨)* | • `白練` (Shironeri `#F3F3F2`)<br>• `胡粉` (Gofun `#FFFFFB`)<br>• `卯の花色` (Unohana `#F7FCFE`)<br>• `素鼠` (Sunezumi `#9EA1A3`)<br>• `銀鼠` (Ginnezumi `#91989F`)<br>• `薄鈍` (Usunibi `#ADADAD`)<br>• `消炭色` (Keshizumi `#524E4D`)<br>• `墨色` (Sumi `#1C1C1C`)<br>• `呂色` (Roiro `#0C0C0C`) | 白昼背景和纸、夜间底色、水墨主字、简笔画淡墨线 |
| **2. 赤・桃・紅系**<br>*(朱印与春樱)* | • `桜色` (Sakura `#FEDFE1`)<br>• `退紅` (Arazome `#F8C3CD`)<br>• `撫子` (Nadeshiko `#DC9FB4`)<br>• `珊瑚色` (Sango `#F596AA`)<br>• `朱色` (Shuiro `#EB6101`)<br>• `茜色` (Akane `#B7282E`)<br>• `弁柄色` (Bengara `#8F2E14`)<br>• `蘇芳` (Suou `#9E3D3F`) | 分钟数字点缀、心率/低电量高亮、日轮简笔画 |
| **3. 黄・茶・褐系**<br>*(和纸与秋叶)* | • `鳥の子色` (Torinoko `#EFEACC`)<br>• `砥粉色` (Tonoko `#F4DDA5`)<br>• `山吹色` (Yamabuki `#F8B500`)<br>• `鬱金` (Ukon `#EFBB24`)<br>• `琥珀色` (Kohaku `#CA7A2C`)<br>• `白茶` (Shiracha `#BC9F77`)<br>• `灰汁色` (Akuiro `#9E9478`)<br>• `千歳茶` (Chitosecha `#494A41`) | 复古暖调背景、夜间护眼大字、大地远山简笔线 |
| **4. 緑・青磁系**<br>*(竹林与青瓷)* | • `白緑` (Byakuroku `#DAEAD0`)<br>• `若竹色` (Wakatake `#68BE8D`)<br>• `青磁色` (Seiji `#69B0AC`)<br>• `錆青磁` (Sabiseiji `#89A894`)<br>• `青竹色` (Aotake `#00896C`)<br>• `常磐色` (Tokiwa `#007B43`)<br>• `千歳緑` (Chitosemidori `#316745`)<br>• `老竹色` (Oitake `#5E644F`) | 分钟清爽配色、身体电量健康色、简笔山林线条 |
| **5. 青・藍・紺系**<br>*(浮世绘与海波)* | • `瓶覗` (Kamenozoki `#A2D7DD`)<br>• `白群` (Byakugun `#78C2C4`)<br>• `浅葱色` (Asagi `#00A3AF`)<br>• `露草色` (Tsuyukusa `#38A1DB`)<br>• `群青色` (Gunjou `#4C6CB3`)<br>• `藍鼠` (Ainezumi `#566C73`)<br>• `鉄御納戸` (Tetsuonando `#2B373B`)<br>• `勝色` (Kachiiro `#181B26`)<br>• `黒橡` (Kurotsurubami `#0B1013`) | 夜间深蓝染背景、白昼沉稳主字、雨丝与水波简笔线 |
| **6. 紫・藤系**<br>*(藤花与暮色)* | • `薄色` (Usuiro `#A87CA0`)<br>• `藤色` (Fujiiro `#AFB4DB`)<br>• `桔梗色` (Kikyou `#5654A2`)<br>• `江戸紫` (Edomurasaki `#745399`)<br>• `葡萄鼠` (Budounezumi `#705B67`)<br>• `藤煤竹` (Fujisusutake `#5A5359`)<br>• `茄子紺` (Nasukon `#47266E`) | 暮色/夜间简笔线条、雅致分钟点缀色 |

---

## 三、 6 套日系简笔画背景 (Minimalist Wa-Art) 几何绘制规范

所有简笔画均在表盘中心时间底层或侧边留白处绘制，仅使用 `1px~2px` 矢量几何线条：

1. **`B1` 晴 · 远山日轮 (Fuji & Sun)**
   - 左侧或右下柔和的富士山对称折线山脊（`drawLine` 4段折线）+ 右上角一轮细线圆环太阳（`drawCircle`）+ 两条横穿山腰的断续平云线。
2. **`B2` 云 · 浮世流云 (Ukiyo Clouds)**
   - 借鉴日式屏风画中的“源氏云（すやり霞）”，用两组平行圆角横线（`drawRoundedRectangle` 或平直短线+半圆弧头）在时间上下方形成优雅的水平透气留白。
3. **`B3` 阴/雾 · 水墨层峦 (Misty Peaks)**
   - 前后两层高低错落的山峰折线，山脚配 3 根不同长度的水平虚线，表现山间云雾。
4. **`B4` 雨 · 细雨涟漪 (Rain & Ripples)**
   - 右上两道极简云弧 + 5 根 60° 倾角的细短斜线雨丝 + 时间底部一圈扁平椭圆水波涟漪。
5. **`B5` 雪 · 雪峰寒星 (Snow Crest)**
   - 带有山尖折线雪冠的远山 + 散落在空白处的 4~5 颗米字形（`*` 3线交叉）极简几何雪花。
6. **`B6` 夜 · 弦月眠猫 (Crescent & Cat)**
   - 右上角一弯纤细新月（双圆弧勾勒）+ 2 颗十字星点 + 时间右下角弧坡上趴着一只极简线条勾勒的圆背小猫背影（双耳三角形 + 圆弧背 + 弯曲小尾巴）。
