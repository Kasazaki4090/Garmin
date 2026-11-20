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

    public var fontId as Number = 2;                 // 字体选择 F1~F5
    public var bgMode as Number = 0;                 // 简笔画模式 B0~B6 (0为自动根据天气/日出日落)
    public var arcMode as Number = 0;                // 边缘进度弧模式 A0~A2 (0关闭, 1细线, 2分段)

    // 4 套预设主题 (AMOLED 色值)
    private static const PRESET_THEMES = [
        // 0: 昼·壱 (白练 · 茜素)
        "F2-B0-A0-F3F3F2-1C1C1C-B7282E-787878-9EA1A3-524E4D-B7282E",
        // 1: 昼·弐 (鸟之子 · 青磁)
        "F1-B0-A0-EFEACC-2B373B-69B0AC-828282-BC9F77-494A41-69B0AC",
        // 2: 夜·壱 (胜色 · 樱月)
        "F3-B0-A0-0B1013-F7FCFE-FEDFE1-8899A0-566C73-ADADAD-F596AA",
        // 3: 夜·弐 (消炭 · 琥珀宵)
        "F5-B6-A0-0C0C0C-F4DDA5-CA7A2C-9E9478-5A5359-9E9478-E2943B"
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
