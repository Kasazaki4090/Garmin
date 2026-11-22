# Komorebi 插画出图指南 (Flux 鲜艳手绘水彩 · 纯白底版)

结合你刚才 `b4~b6` 的手绘墨线质感，去掉灰蒙蒙的淡墨雾气，升级为 **“锐利墨线 + 鲜艳饱满水彩/浮世绘色块 + 纯白背景”**，出图后直接脚本一刀去白底透明化！

---

## ⚙️ 生成参数（Flux）
- **尺寸**：`1024 × 384` 或 `1152 × 384`（`3:1` 扁横幅）
- **关键控制**：不要写 `sumi-e` 或 `misty`（这两个词会让 Flux 画出整片灰雾背景，既显淡又难抠图）；改用 `crisp ink line art with vibrant saturated watercolor, pure clean white background`。

---

## 🎨 全套 6 张 Flux 鲜艳版提示词（直接复制）

### 1. 晴 · 富士山与朱红日轮 (`b1`)
```text
Japanese hand-drawn ink line art with vibrant saturated watercolor illustration, horizontal panoramic composition, isolated on a pure clean white background. On the right, an iconic Mount Fuji with crisp ink outlines, bright cobalt-indigo mountain body, snow cap, and a vivid vermilion-red sun rising behind it with warm golden accents. On the left, a lush emerald pine branch extending inward. No grey sky, no fog, bright vivid colors, generous pure white empty space in the center.
```

### 2. 云 · 青磁海波与飞燕 (`b2`)
```text
Japanese hand-drawn ink line art with vibrant saturated watercolor illustration, horizontal panoramic composition, isolated on a pure clean white background. Along the bottom edge, stylized Japanese ocean waves and curling clouds drawn with crisp ink strokes in vivid turquoise-teal, cerulean blue, and white foam. Two bright navy and crimson-red swallows soaring above. No grey sky, no fog, vivid cheerful colors, generous pure white empty space in the center.
```

### 3. 阴/静 · 京都朱红鸟居与石灯笼 (`b3`)
```text
Japanese hand-drawn ink line art with vibrant saturated watercolor illustration, horizontal panoramic composition, isolated on a pure clean white background. On the right, a vivid vermilion-red Japanese Torii gate beside a moss-green stone lantern and fresh emerald-green lakeside reeds along a clear teal-blue water edge. No grey fog, no dark sky, bright vivid traditional colors, generous pure white empty space in the center and left.
```

### 4. 雨 · 翠竹、和伞与水涟漪 (`b4`)
```text
Japanese hand-drawn ink line art with vibrant saturated watercolor illustration, horizontal panoramic composition, isolated on a pure clean white background. On the left, vibrant emerald-green bamboo stalks and leaves with fresh raindrops; on the right, a bright indigo-blue and vermilion traditional Japanese wagasa umbrella resting beside mossy green rocks and clear sky-blue water ripples. No grey sky, no fog, crisp vivid colors, generous pure white empty space in the center.
```

### 5. 雪 · 冰蓝雪峰与红梅 (`b5`)
```text
Japanese hand-drawn ink line art with vibrant saturated watercolor illustration, horizontal panoramic composition, isolated on a pure clean white background. On the left, a gnarled dark branch blooming with vivid crimson-red plum blossoms and snow; on the right, crisp winter mountain peaks in bright cerulean blue and pure white snow, with a few light ice-blue snowflakes. No grey overcast sky, clean bright vivid colors, generous pure white empty space in the center.
```

### 6. 夜 · 琥珀弯月、黑猫与樱花 (`b6`)
```text
Japanese hand-drawn ink line art with vibrant saturated watercolor illustration, horizontal panoramic composition, isolated on a pure clean white background. Sitting on a deep indigo tiled roof along the bottom left, a sleek black cat silhouette looking up at a glowing bright amber-gold crescent moon, framed by lush bamboo leaves and vivid sakura-pink cherry blossoms. No dark grey background sky, clean pure white background around the elements, vivid contrast, generous white empty space on the right.
```

---

## 📁 跑完放哪里？
全部丢进 **`d:\Garmin\Komorebi\02_font_and_vector_assets\sd_raw\`**（直接覆盖原文件即可），告诉我一声，我马上跑脚本**自动去白底转透明 + 压成 Garmin 轻量贴片 + 重构表盘代码**！
