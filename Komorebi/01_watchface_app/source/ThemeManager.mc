import Toybox.Application;
import Toybox.Graphics;
import Toybox.Lang;
import Toybox.System;

class ThemeManager {
    // 7 个核心色值
    public var colorBg as Number = 0xF3F3F2;         // 表盘底色 (和纸白练)
    public var colorHour as Number = 0x1C1C1C;       // 小时数字色 (水墨黑)
    public var colorMin as Number = 0xB7282E;        // 分钟数字色 (茜素红朱印)
    public var colorSec as Number = 0x787878;        // 秒钟数字色 (素鼠灰)
    public var colorBgLines as Number = 0x9EA1A3;    // 简笔画线条色 (淡墨)
    public var colorData as Number = 0x524E4D;       // 数据指标文字色 (消炭)
    public var colorAccent as Number = 0xB7282E;     // 高亮色/朱印 (茜素红)

    public var fontId as Number = 1;                 // 字体选择 F1~F5 (默认 F1 iPhone裂开Mono)
    public var bgMode as Number = 0;                 // 简笔画模式 B0~B6 (0为自动根据天气/日出日落)
    public var arcMode as Number = 1;                // 边缘进度弧模式 A0~A2 (默认 A1 保留左右双弧)

    // 布局与可自定义数据槽位设置
    public var showWeekday as Boolean = true;
    public var showWeatherCond as Boolean = false;
    public var leftArcMetric as Number = 3;          // 默认身体电量
    public var rightArcMetric as Number = 2;         // 默认步数目标进度
    public var slotWingL as Number = 3;              // 左翼: 身体电量
    public var slotWingR as Number = 2;              // 右翼: 步数
    public var slotBot1 as Number = 1;               // 底部第1行: 心率
    public var slotBot2 as Number = 6;               // 底部第2行左: 距离
    public var slotBot3 as Number = 7;               // 底部第2行右: 海拔
    public var slotBot4 as Number = 5;               // 底部第3行左: 卡路里
    public var slotBot5 as Number = 10;              // 底部第3行右: VO2 Max

    // 4 套预设主题 (AMOLED 色值)
    private static const PRESET_THEMES = [
        // 0: 昼·壱 (白练 · 茜素) - F1 iPhone裂开Mono + A1 左右细弧
        "F1-B0-A1-F3F3F2-1C1C1C-B7282E-787878-9EA1A3-524E4D-B7282E",
        // 1: 昼·弐 (鸟之子 · 青磁)
        "F1-B0-A1-EFEACC-2B373B-69B0AC-828282-BC9F77-494A41-69B0AC",
        // 2: 夜·壱 (胜色 · 樱月)
        "F4-B0-A1-0B1013-F7FCFE-FEDFE1-8899A0-566C73-ADADAD-F596AA",
        // 3: 夜·弐 (消炭 · 琥珀宵)
        "F5-B6-A1-0C0C0C-F4DDA5-CA7A2C-9E9478-5A5359-9E9478-E2943B"
    ];

    function initialize() {
        reloadTheme();
    }

    // 从属性或预设重新加载主题
    public function reloadTheme() as Void {
        var app = Application.getApp();
        var code = app.getProperty("ThemeCode");
        if (code == null || code.equals("")) {
            var presetIdx = app.getProperty("PresetTheme");
            if (presetIdx == null || presetIdx < 0 || presetIdx >= PRESET_THEMES.size()) {
                presetIdx = 0;
            }
            code = PRESET_THEMES[presetIdx];
        }

        parseThemeCode(code);

        showWeekday = readBoolProp(app, "ShowWeekday", true);
        showWeatherCond = readBoolProp(app, "ShowWeatherCond", false);
        leftArcMetric = readNumProp(app, "LeftArcMetric", 3);
        rightArcMetric = readNumProp(app, "RightArcMetric", 2);
        slotWingL = readNumProp(app, "SlotWingL", 3);
        slotWingR = readNumProp(app, "SlotWingR", 2);
        slotBot1 = readNumProp(app, "SlotBot1", 1);
        slotBot2 = readNumProp(app, "SlotBot2", 6);
        slotBot3 = readNumProp(app, "SlotBot3", 7);
        slotBot4 = readNumProp(app, "SlotBot4", 5);
        slotBot5 = readNumProp(app, "SlotBot5", 10);
    }

    private function readNumProp(app as Application.AppBase, key as String, fallback as Number) as Number {
        var val = app.getProperty(key);
        if (val instanceof Number) {
            return val;
        }
        return fallback;
    }

    private function readBoolProp(app as Application.AppBase, key as String, fallback as Boolean) as Boolean {
        var val = app.getProperty(key);
        if (val instanceof Boolean) {
            return val;
        }
        return fallback;
    }

    // 解析形如: F2-B0-A0-F3F3F2-1C1C1C-B7282E-787878-9EA1A3-524E4D-B7282E
    public function parseThemeCode(code as String) as Void {
        if (code == null || code.length() < 10) {
            return;
        }

        try {
            // 切分 '-' 分隔符
            var parts = splitString(code, "-");
            if (parts.size() < 10) {
                return;
            }

            // F{1-5}
            if (parts[0].length() >= 2 && parts[0].substring(0, 1).equals("F")) {
                fontId = parts[0].substring(1, 2).toNumber();
            }
            // B{0-6}
            if (parts[1].length() >= 2 && parts[1].substring(0, 1).equals("B")) {
                bgMode = parts[1].substring(1, 2).toNumber();
            }
            // A{0-2}
            if (parts[2].length() >= 2 && parts[2].substring(0, 1).equals("A")) {
                arcMode = parts[2].substring(1, 2).toNumber();
            }

            colorBg = parseHexColor(parts[3]);
            colorHour = parseHexColor(parts[4]);
            colorMin = parseHexColor(parts[5]);
            colorSec = parseHexColor(parts[6]);
            colorBgLines = parseHexColor(parts[7]);
            colorData = parseHexColor(parts[8]);
            colorAccent = parseHexColor(parts[9]);

        } catch (ex) {
            System.println("Failed to parse theme code: " + ex.getErrorMessage());
        }
    }

    // 将 6 位 16 进制转为 Number 颜色
    private function parseHexColor(hex as String) as Number {
        if (hex == null || hex.length() < 6) {
            return 0x000000;
        }
        var colorVal = 0;
        for (var i = 0; i < 6; i++) {
            var ch = hex.substring(i, i + 1);
            var digit = hexCharToVal(ch);
            colorVal = (colorVal << 4) | digit;
        }
        return colorVal;
    }

    private function hexCharToVal(ch as String) as Number {
        var c = ch.toUpper();
        if (c.equals("0")) { return 0; }
        if (c.equals("1")) { return 1; }
        if (c.equals("2")) { return 2; }
        if (c.equals("3")) { return 3; }
        if (c.equals("4")) { return 4; }
        if (c.equals("5")) { return 5; }
        if (c.equals("6")) { return 6; }
        if (c.equals("7")) { return 7; }
        if (c.equals("8")) { return 8; }
        if (c.equals("9")) { return 9; }
        if (c.equals("A")) { return 10; }
        if (c.equals("B")) { return 11; }
        if (c.equals("C")) { return 12; }
        if (c.equals("D")) { return 13; }
        if (c.equals("E")) { return 14; }
        if (c.equals("F")) { return 15; }
        return 0;
    }

    private function splitString(str as String, sep as String) as Array<String> {
        var list = [] as Array<String>;
        var start = 0;
        var len = str.length();
        for (var i = 0; i < len; i++) {
            if (str.substring(i, i + 1).equals(sep)) {
                if (i > start) {
                    list.add(str.substring(start, i));
                }
                start = i + 1;
            }
        }
        if (start < len) {
            list.add(str.substring(start, len));
        }
        return list;
    }
}
