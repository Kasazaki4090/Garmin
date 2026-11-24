const I18N = {
  zh: {
    appTitle: "WaTime 和色时光",
    appSubtitle: "Garmin 表盘在线调色与短码生成器",
    mipToggle: "MIP 64色预览",
    toggleWeekday: "顶部星期",
    toggleWeather: "天气状态行",
    shortcodeLabel: "主题短码（复制后粘贴到 Garmin Connect 表盘设置）",
    copyBtn: "一键复制",
    copiedToast: "已复制短码！打开 Garmin Connect → 表盘设置 → 粘贴即可。",
    copyFallback: "已选中短码，请按 Ctrl+C 复制。",
    presetsLabel: "预设和色主题：",
    sec1Title: "1. 版式与水彩背景",
    fontLabel: "主时间字体 (F)",
    bgLabel: "水彩背景 (B)",
    arcLabel: "下半屏弧线 (A)",
    f1: "F1 · 裂开 Mono", f2: "F2 · 明朝衬线", f3: "F3 · 硬派黑体 (矢量)", f4: "F4 · 八段数码管", f5: "F5 · 复古辉光管", f6: "F6 · Sirin 优雅裂开",
    b0: "B0 · 自动 (天气/昼夜)", b1: "B1 · 晴 · 远山日轮", b2: "B2 · 云 · 浮世流云", b3: "B3 · 雾 · 水墨层峦",
    b4: "B4 · 雨 · 细雨涟漪", b5: "B5 · 雪 · 雪峰寒星", b6: "B6 · 夜 · 弦月眠猫",
    a1: "A1 · 下半屏细弧", a2: "A2 · 下半屏粗弧", a0: "A0 · 关闭弧线",
    sec2Title: "2. 部位调色（点选部位，可手动输入 HEX、取色或点选和色）",
    sec3Title: "3. 日本传统和色字典（48 色）",
    presets: ["昼·壱 白练茜素", "昼·弐 鸟之子青磁", "夜·壱 胜色樱月", "夜·弐 消炭琥珀"],
    slots: { bg: "表盘底色", hour: "小时数字", min: "分钟数字", sec: "秒钟数字", lines: "弧线底轨", data: "数据文字", accent: "高亮 / 朱印" },
    cats: { "白·灰·墨": "白·灰·墨", "赤·桃·紅": "赤·桃·紅", "黄·茶·褐": "黄·茶·褐", "緑·青磁": "緑·青磁", "青·藍·紺": "青·藍·紺", "紫·藤": "紫·藤" }
  },
  en: {
    appTitle: "WaTime Palette Studio",
    appSubtitle: "Garmin Watchface Colorway & Shortcode Generator",
    mipToggle: "MIP 64-Color",
    toggleWeekday: "Weekday",
    toggleWeather: "Weather Row",
    shortcodeLabel: "Theme Shortcode (Paste into Garmin Connect Watchface Settings)",
    copyBtn: "Copy Code",
    copiedToast: "Copied! Paste into Garmin Connect → Watchface Settings.",
    copyFallback: "Selected. Press Ctrl+C to copy.",
    presetsLabel: "Curated Wa-Color Presets:",
    sec1Title: "1. Typography & Watercolor Scene",
    fontLabel: "Time Font (F)",
    bgLabel: "Background (B)",
    arcLabel: "Lower Arcs (A)",
    f1: "F1 · Split Mono", f2: "F2 · Mincho Serif", f3: "F3 · Bold Vector", f4: "F4 · 7-Segment LCD", f5: "F5 · Nixie Tube", f6: "F6 · Sirin Stencil",
    b0: "B0 · Auto (Weather / Day-Night)", b1: "B1 · Clear · Fuji & Sun", b2: "B2 · Clouds · Ukiyo", b3: "B3 · Mist · Ink Peaks",
    b4: "B4 · Rain · Ripples", b5: "B5 · Snow · Frost Stars", b6: "B6 · Night · Crescent Cat",
    a1: "A1 · Lower Thin Arcs", a2: "A2 · Lower Bold Arcs", a0: "A0 · Off",
    sec2Title: "2. Zone Colors (Select a zone, type HEX, pick color, or click a swatch)",
    sec3Title: "3. Japanese Traditional Colors (48 Swatches)",
    presets: ["Day I · Shironeri", "Day II · Torinoko", "Night I · Kachiiro", "Night II · Kohaku"],
    slots: { bg: "Background", hour: "Hour Digits", min: "Minute Digits", sec: "Second Digits", lines: "Arc Track", data: "Data Text", accent: "Accent / Seal" },
    cats: { "白·灰·墨": "White / Ink", "赤·桃·紅": "Red / Sakura", "黄·茶·褐": "Gold / Tea", "緑·青磁": "Green / Seiji", "青·藍·紺": "Blue / Indigo", "紫·藤": "Violet / Fuji" }
  },
  ja: {
    appTitle: "WaTime 和色時計",
    appSubtitle: "Garmin ウォッチフェイス配色＆ショートコード生成",
    mipToggle: "MIP 64色プレビュー",
    toggleWeekday: "曜日表示",
    toggleWeather: "天気行表示",
    shortcodeLabel: "テーマコード（コピーして Garmin Connect 設定に貼付）",
    copyBtn: "コピー",
    copiedToast: "コピーしました！Garmin Connect の設定画面に貼り付けてください。",
    copyFallback: "選択しました。Ctrl+C でコピーしてください。",
    presetsLabel: "和色プリセット：",
    sec1Title: "1. フォント・水彩背景",
    fontLabel: "時刻フォント (F)",
    bgLabel: "水彩背景 (B)",
    arcLabel: "下部アーク (A)",
    f1: "F1 · スプリット Mono", f2: "F2 · 明朝体", f3: "F3 · ベクター太字", f4: "F4 · デジタル液晶", f5: "F5 · ニキシー管", f6: "F6 · Sirin ステンシル",
    b0: "B0 · 自動 (天気/昼夜)", b1: "B1 · 晴 · 富士日輪", b2: "B2 · 曇 · 浮世雲", b3: "B3 · 霧 · 水墨山並",
    b4: "B4 · 雨 · 細雨波紋", b5: "B5 · 雪 · 雪峰寒星", b6: "B6 · 夜 · 三日月猫",
    a1: "A1 · 下部細アーク", a2: "A2 · 下部太アーク", a0: "A0 · 非表示",
    sec2Title: "2. パーツ配色（選択して HEX 手入力・ピッカー・和色から指定）",
    sec3Title: "3. 日本の伝統色（48色）",
    presets: ["昼・壱 白練茜", "昼・弐 鳥の子青磁", "夜・壱 勝色桜月", "夜・弐 消炭琥珀"],
    slots: { bg: "文字盤背景", hour: "時 (Hour)", min: "分 (Min)", sec: "秒 (Sec)", lines: "アーク軌道", data: "データ文字", accent: "朱印 / アクセント" },
    cats: { "白·灰·墨": "白・灰・墨", "赤·桃·紅": "赤・桃・紅", "黄·茶·褐": "黄・茶・褐", "緑·青磁": "緑・青磁", "青·藍·紺": "青・藍・紺", "紫·藤": "紫・藤" }
  }
};

const PRESETS = [
  { code: "F1-B1-A1-F3F3F2-1C1C1C-B7282E-787878-9EA1A3-524E4D-B7282E" },
  { code: "F1-B2-A1-EFEACC-2B373B-69B0AC-828282-BC9F77-494A41-69B0AC" },
  { code: "F4-B6-A1-0B1013-F7FCFE-FEDFE1-8899A0-566C73-ADADAD-F596AA" },
  { code: "F5-B6-A1-0C0C0C-F4DDA5-CA7A2C-9E9478-5A5359-9E9478-E2943B" }
];

const COLOR_SLOT_KEYS = ["bg", "hour", "min", "sec", "lines", "data", "accent"];

const WA_COLORS = {
  "白·灰·墨": [
    ["白練", "F3F3F2"], ["胡粉", "FFFFFB"], ["卯の花", "F7FCFE"],
    ["素鼠", "9EA1A3"], ["銀鼠", "91989F"], ["薄鈍", "ADADAD"],
    ["消炭色", "524E4D"], ["墨色", "1C1C1C"], ["呂色", "0C0C0C"]
  ],
  "赤·桃·紅": [
    ["桜色", "FEDFE1"], ["退紅", "F8C3CD"], ["撫子", "DC9FB4"],
    ["珊瑚色", "F596AA"], ["朱色", "EB6101"], ["茜色", "B7282E"],
    ["弁柄色", "8F2E14"], ["蘇芳", "9E3D3F"]
  ],
  "黄·茶·褐": [
    ["鳥の子", "EFEACC"], ["砥粉色", "F4DDA5"], ["山吹色", "F8B500"],
    ["鬱金", "EFBB24"], ["琥珀色", "CA7A2C"], ["白茶", "BC9F77"],
    ["灰汁色", "9E9478"], ["千歳茶", "494A41"]
  ],
  "緑·青磁": [
    ["白緑", "DAEAD0"], ["若竹色", "68BE8D"], ["青磁色", "69B0AC"],
    ["錆青磁", "89A894"], ["青竹色", "00896C"], ["常磐色", "007B43"],
    ["千歳緑", "316745"], ["老竹色", "5E644F"]
  ],
  "青·藍·紺": [
    ["瓶覗", "A2D7DD"], ["白群", "78C2C4"], ["浅葱色", "00A3AF"],
    ["露草色", "38A1DB"], ["群青色", "4C6CB3"], ["藍鼠", "566C73"],
    ["鉄御納戸", "2B373B"], ["勝色", "181B26"], ["黒橡", "0B1013"]
  ],
  "紫·藤": [
    ["薄色", "A87CA0"], ["藤色", "AFB4DB"], ["桔梗色", "5654A2"],
    ["江戸紫", "745399"], ["葡萄鼠", "705B67"], ["藤煤竹", "5A5359"],
    ["茄子紺", "47266E"]
  ]
};

const state = {
  lang: "zh",
  font: 1,
  bgMode: 1,
  arcMode: 1,
  colors: {
    bg: "F3F3F2",
    hour: "1C1C1C",
    min: "B7282E",
    sec: "787878",
    lines: "9EA1A3",
    data: "524E4D",
    accent: "B7282E"
  },
  activeSlot: "hour",
  activeCat: Object.keys(WA_COLORS)[0],
  mipMode: false,
  showWeekday: true,
  showWeatherCond: false
};

const bgImages = {};
for (let i = 1; i <= 6; i++) {
  const img = new Image();
  img.src = `assets/bg_${i}.webp`;
  img.onload = () => drawWatch();
  bgImages[i] = img;
}

function quantizeChannelMIP(val) {
  const levels = [0, 85, 170, 255];
  let best = 0;
  let minDiff = 999;
  for (const lv of levels) {
    const d = Math.abs(val - lv);
    if (d < minDiff) { minDiff = d; best = lv; }
  }
  return best;
}

function toMIPHex(hex) {
  const r = quantizeChannelMIP(parseInt(hex.slice(0, 2), 16));
  const g = quantizeChannelMIP(parseInt(hex.slice(2, 4), 16));
  const b = quantizeChannelMIP(parseInt(hex.slice(4, 6), 16));
  return [r, g, b].map(v => v.toString(16).padStart(2, "0").toUpperCase()).join("");
}

function normalizeHex(raw) {
  const clean = raw.trim().replace(/^#/, "").toUpperCase();
  if (/^[0-9A-F]{6}$/.test(clean)) return clean;
  if (/^[0-9A-F]{3}$/.test(clean)) {
    return clean.split("").map(c => c + c).join("");
  }
  return null;
}

function getEffectiveHex(key) {
  const raw = state.colors[key];
  return state.mipMode ? toMIPHex(raw) : raw;
}

function isDarkHex(hex) {
  const r = parseInt(hex.slice(0, 2), 16);
  const g = parseInt(hex.slice(2, 4), 16);
  const b = parseInt(hex.slice(4, 6), 16);
  return (0.299 * r + 0.587 * g + 0.114 * b) < 110;
}

function buildShortcode() {
  const cols = COLOR_SLOT_KEYS.map(k => getEffectiveHex(k)).join("-");
  return `F${state.font}-B${state.bgMode}-A${state.arcMode}-${cols}`;
}

function parseShortcode(code) {
  const parts = code.trim().toUpperCase().split("-");
  if (parts.length < 10) return false;
  if (/^F[1-6]$/.test(parts[0])) state.font = Number(parts[0][1]);
  if (/^B[0-6]$/.test(parts[1])) state.bgMode = Number(parts[1][1]);
  if (/^A[0-2]$/.test(parts[2])) state.arcMode = Number(parts[2][1]);
  COLOR_SLOT_KEYS.forEach((k, idx) => {
    if (/^[0-9A-F]{6}$/.test(parts[3 + idx])) {
      state.colors[k] = parts[3 + idx];
    }
  });
  return true;
}

function applyI18n() {
  const dict = I18N[state.lang];
  document.documentElement.lang = state.lang === "zh" ? "zh-CN" : state.lang;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) el.textContent = dict[key];
  });
  document.querySelectorAll(".lang-btn").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("data-lang") === state.lang);
  });
  renderPresets();
  renderSlots();
  renderCategories();
}

function syncUI() {
  document.getElementById("fontSelect").value = String(state.font);
  document.getElementById("bgSelect").value = String(state.bgMode);
  document.getElementById("arcSelect").value = String(state.arcMode);
  document.getElementById("themeCodeInput").value = buildShortcode();
  renderSlots();
  drawWatch();
}

function renderPresets() {
  const container = document.getElementById("presetButtons");
  const names = I18N[state.lang].presets;
  container.innerHTML = "";
  PRESETS.forEach((p, idx) => {
    const parts = p.code.split("-");
    const btn = document.createElement("button");
    btn.className = "preset-btn";
    btn.innerHTML = `
      <span class="preset-dots">
        <i style="background:#${parts[3]}"></i>
        <i style="background:#${parts[4]}"></i>
        <i style="background:#${parts[5]}"></i>
      </span>
      <span>${names[idx]}</span>
    `;
    btn.onclick = () => {
      parseShortcode(p.code);
      syncUI();
    };
    container.appendChild(btn);
  });
}

function renderSlots() {
  const container = document.getElementById("colorSlots");
  const slotNames = I18N[state.lang].slots;
  container.innerHTML = "";
  COLOR_SLOT_KEYS.forEach(key => {
    const hex = getEffectiveHex(key);
    const el = document.createElement("div");
    el.className = `slot-item ${state.activeSlot === key ? "active" : ""}`;
    el.innerHTML = `
      <div class="slot-meta">
        <span class="slot-name">${slotNames[key]}</span>
        <span class="slot-hex-wrap">#<input type="text" class="slot-hex-input" maxlength="7" value="${hex}" spellcheck="false" /></span>
      </div>
      <input type="color" class="slot-picker" value="#${hex}" />
    `;

    el.onclick = (e) => {
      if (e.target.tagName !== "INPUT") {
        state.activeSlot = key;
        renderSlots();
      }
    };

    const hexInput = el.querySelector(".slot-hex-input");
    const picker = el.querySelector(".slot-picker");

    hexInput.onfocus = () => {
      state.activeSlot = key;
      document.querySelectorAll(".slot-item").forEach(item => item.classList.remove("active"));
      el.classList.add("active");
    };

    hexInput.oninput = (e) => {
      const norm = normalizeHex(e.target.value);
      if (norm) {
        state.colors[key] = norm;
        const eff = getEffectiveHex(key);
        picker.value = `#${eff}`;
        document.getElementById("themeCodeInput").value = buildShortcode();
        drawWatch();
      }
    };

    hexInput.onblur = () => {
      hexInput.value = getEffectiveHex(key);
    };

    picker.oninput = (e) => {
      state.activeSlot = key;
      state.colors[key] = e.target.value.slice(1).toUpperCase();
      syncUI();
    };

    container.appendChild(el);
  });
}

function renderCategories() {
  const tabs = document.getElementById("catTabs");
  const catNames = I18N[state.lang].cats;
  tabs.innerHTML = "";
  Object.keys(WA_COLORS).forEach(cat => {
    const btn = document.createElement("button");
    btn.className = `cat-tab ${state.activeCat === cat ? "active" : ""}`;
    btn.textContent = catNames[cat] || cat;
    btn.onclick = () => {
      state.activeCat = cat;
      renderCategories();
      renderSwatches();
    };
    tabs.appendChild(btn);
  });
}

function renderSwatches() {
  const grid = document.getElementById("swatchesGrid");
  grid.innerHTML = "";
  WA_COLORS[state.activeCat].forEach(([name, hex]) => {
    const card = document.createElement("div");
    card.className = "swatch-card";
    card.innerHTML = `
      <div class="swatch-color" style="background:#${hex}"></div>
      <div class="swatch-info">
        <span class="swatch-name">${name}</span>
        <span class="swatch-hex">#${hex}</span>
      </div>
    `;
    card.onclick = () => {
      state.colors[state.activeSlot] = hex;
      syncUI();
    };
    grid.appendChild(card);
  });
}

function getFontFamily(fontId) {
  switch (fontId) {
    case 2: return '"Noto Serif SC", "Songti SC", Georgia, serif';
    case 3: return '"Arial Black", "Helvetica Neue", sans-serif';
    case 4:
    case 5: return '"Courier New", ui-monospace, monospace';
    default: return '"SF Pro Display", "Segoe UI", system-ui, sans-serif';
  }
}

function drawWatch() {
  const canvas = document.getElementById("watchCanvas");
  const ctx = canvas.getContext("2d");
  const S = canvas.width;

  const cBg = `#${getEffectiveHex("bg")}`;
  const cHour = `#${getEffectiveHex("hour")}`;
  const cMin = `#${getEffectiveHex("min")}`;
  const cSec = `#${getEffectiveHex("sec")}`;
  const cLines = `#${getEffectiveHex("lines")}`;
  const cData = `#${getEffectiveHex("data")}`;
  const cAccent = `#${getEffectiveHex("accent")}`;

  ctx.clearRect(0, 0, S, S);
  ctx.save();
  ctx.beginPath();
  ctx.arc(S / 2, S / 2, S / 2, 0, Math.PI * 2);
  ctx.clip();

  ctx.fillStyle = cBg;
  ctx.fillRect(0, 0, S, S);

  const sceneIdx = state.bgMode === 0 ? 1 : state.bgMode;
  const img = bgImages[sceneIdx];
  if (img && img.complete && img.naturalWidth > 0) {
    ctx.drawImage(img, 0, 0, S, S);
    if (isDarkHex(getEffectiveHex("bg"))) {
      ctx.fillStyle = cBg;
      ctx.globalAlpha = 0.58;
      ctx.fillRect(0, 0, S, S);
      ctx.globalAlpha = 1;
    }
  }

  // 1. 顶部电量
  const topY = S * 0.085;
  ctx.font = '600 15px "Segoe UI", sans-serif';
  ctx.textBaseline = "middle";
  const battText = "85%";
  const bw = 24, bh = 12, gap = 7;
  const tw = ctx.measureText(battText).width;
  const bx = (S - (bw + 2 + gap + tw)) / 2;
  ctx.strokeStyle = cData;
  ctx.lineWidth = 1.5;
  ctx.strokeRect(bx, topY - bh / 2, bw, bh);
  ctx.fillStyle = cData;
  ctx.fillRect(bx + bw, topY - 3, 2, 6);
  ctx.fillRect(bx + 2, topY - bh / 2 + 2, (bw - 4) * 0.85, bh - 4);
  ctx.textAlign = "left";
  ctx.fillText(battText, bx + bw + 2 + gap, topY);

  // 2. 第二行：日期 - 星期 - 气温
  ctx.textAlign = "center";
  ctx.fillStyle = cData;
  const line2 = state.showWeekday ? "11/23 MON 18°" : "11/23 18°";
  ctx.fillText(line2, S / 2, S * 0.152);

  // 3. 可选天气状态
  if (state.showWeatherCond) {
    ctx.fillStyle = cLines;
    ctx.fillText("CLEAR", S / 2, S * 0.205);
  }

  // 4. 大时间
  const timeTop = S * (state.showWeatherCond ? 0.245 : 0.215);
  const ff = getFontFamily(state.font);
  ctx.fillStyle = cHour;
  ctx.font = `700 118px ${ff}`;
  ctx.fillText("11", S * 0.30, timeTop + 56);
  ctx.fillStyle = cMin;
  ctx.fillText(":", S * 0.50, timeTop + 44);
  ctx.font = `700 84px ${ff}`;
  ctx.fillText("36", S * 0.69, timeTop + 42);
  ctx.fillStyle = cSec;
  ctx.font = `700 24px ${ff}`;
  ctx.fillText("42", S * 0.77, timeTop + 100);

  // 5. 下半屏左右弧线进度条
  if (state.arcMode !== 0) {
    const r = S / 2 - 7;
    ctx.lineWidth = state.arcMode === 1 ? 4 : 6;
    ctx.lineCap = "round";

    ctx.strokeStyle = cLines;
    ctx.beginPath();
    ctx.arc(S / 2, S / 2, r, (122 * Math.PI) / 180, (180 * Math.PI) / 180);
    ctx.stroke();

    ctx.strokeStyle = cAccent;
    ctx.beginPath();
    ctx.arc(S / 2, S / 2, r, (132 * Math.PI) / 180, (180 * Math.PI) / 180);
    ctx.stroke();

    ctx.strokeStyle = cLines;
    ctx.beginPath();
    ctx.arc(S / 2, S / 2, r, 0, (58 * Math.PI) / 180);
    ctx.stroke();

    ctx.strokeStyle = cMin;
    ctx.beginPath();
    ctx.arc(S / 2, S / 2, r, (20 * Math.PI) / 180, (58 * Math.PI) / 180);
    ctx.stroke();
  }

  // 6. 两翼指标
  const wy = S * 0.575;
  ctx.fillStyle = cAccent;
  ctx.font = '600 14px "Segoe UI", sans-serif';
  ctx.fillText("⚡", S * 0.22, wy - 24);
  ctx.fillStyle = cHour;
  ctx.font = '700 26px "Segoe UI", sans-serif';
  ctx.fillText("88", S * 0.22, wy);
  ctx.fillStyle = cData;
  ctx.font = '600 12px "Segoe UI", sans-serif';
  ctx.fillText("BODY BAT", S * 0.22, wy + 22);

  ctx.fillStyle = cMin;
  ctx.font = '600 14px "Segoe UI", sans-serif';
  ctx.fillText("👟", S * 0.78, wy - 24);
  ctx.fillStyle = cHour;
  ctx.font = '700 26px "Segoe UI", sans-serif';
  ctx.fillText("6 420", S * 0.78, wy);
  ctx.fillStyle = cData;
  ctx.font = '600 12px "Segoe UI", sans-serif';
  ctx.fillText("64%", S * 0.78, wy + 22);

  // 7. 底部 1-2-2 数据矩阵
  ctx.font = '600 15px "Segoe UI", sans-serif';
  ctx.fillStyle = cAccent;
  ctx.fillText("♥ HR 72 bpm", S * 0.50, S * 0.695);
  ctx.fillStyle = cData;
  ctx.fillText("◎ 4.8 km", S * 0.35, S * 0.780);
  ctx.fillText("▲ ALT 210 m", S * 0.65, S * 0.780);
  ctx.fillText("🔥 340 kcal", S * 0.37, S * 0.865);
  ctx.fillText("VO2 48", S * 0.63, S * 0.865);

  ctx.restore();
}

// 语言切换
document.getElementById("langSwitch").onclick = (e) => {
  const btn = e.target.closest(".lang-btn");
  if (!btn) return;
  state.lang = btn.getAttribute("data-lang");
  applyI18n();
};

// 控制项事件绑定
document.getElementById("fontSelect").onchange = (e) => { state.font = Number(e.target.value); syncUI(); };
document.getElementById("bgSelect").onchange = (e) => { state.bgMode = Number(e.target.value); syncUI(); };
document.getElementById("arcSelect").onchange = (e) => { state.arcMode = Number(e.target.value); syncUI(); };
document.getElementById("mipToggle").onchange = (e) => { state.mipMode = e.target.checked; syncUI(); };
document.getElementById("showWeekday").onchange = (e) => { state.showWeekday = e.target.checked; drawWatch(); };
document.getElementById("showWeatherCond").onchange = (e) => { state.showWeatherCond = e.target.checked; drawWatch(); };

document.getElementById("themeCodeInput").oninput = (e) => {
  if (parseShortcode(e.target.value)) {
    document.getElementById("fontSelect").value = String(state.font);
    document.getElementById("bgSelect").value = String(state.bgMode);
    document.getElementById("arcSelect").value = String(state.arcMode);
    renderSlots();
    drawWatch();
  }
};

document.getElementById("copyBtn").onclick = async () => {
  const input = document.getElementById("themeCodeInput");
  const dict = I18N[state.lang];
  input.select();
  try {
    await navigator.clipboard.writeText(input.value);
    document.getElementById("copyToast").textContent = dict.copiedToast;
  } catch {
    document.execCommand("copy");
    document.getElementById("copyToast").textContent = dict.copyFallback;
  }
  setTimeout(() => { document.getElementById("copyToast").textContent = ""; }, 3000);
};

// 初始化
applyI18n();
renderSwatches();
syncUI();
