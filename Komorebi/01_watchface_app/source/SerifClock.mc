import Toybox.Application;
import Toybox.Graphics;
import Toybox.Lang;
import Toybox.System;

// 严格等宽 Mono 位图字体时钟渲染器：
// - 无论 11:11 还是 23:58，HH、冒号、MM、SS 坐标永远锁死不动！
// - HH 最大，MM 在右上，SS 在 MM 正下方右对齐 (MM:SS 严格 72:18 = 4:1)。
class SerifClock {
    private static var mCachedFontId as Number = -1;
    private static var mFonts = null;

    public static function draw(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager, is24Hour as Boolean, showSeconds as Boolean) as Boolean {
        if (mFonts == null || mCachedFontId != theme.fontId) {
            mCachedFontId = theme.fontId;
            mFonts = loadTiers(h, theme.fontId);
        }
        if (mFonts.size() != 3 || mFonts[0] == null || mFonts[1] == null || mFonts[2] == null) {
            return false;
        }

        var clockTime = System.getClockTime();
        var hour = clockTime.hour;
        if (!is24Hour) {
            hour = hour % 12;
            if (hour == 0) {
                hour = 12;
            }
        }
        var hourStr = pad2(hour);
        var minStr = pad2(clockTime.min);
        var secStr = pad2(clockTime.sec);

        var fontHour = mFonts[0];
        var fontMin = mFonts[1];
        var fontSec = mFonts[2];

        var digitH = dc.getFontHeight(fontHour);
        var minH = dc.getFontHeight(fontMin);
        var secH = dc.getFontHeight(fontSec);

        // 固定用 "00" 测量槽宽（Mono 字库下 00..99 完全等宽，保证坐标永久锁死）
        var hourW = dc.getTextWidthInPixels("00", fontHour);
        var colonW = dc.getTextWidthInPixels(":", fontHour);
        var minW = dc.getTextWidthInPixels("00", fontMin);
        var secW = dc.getTextWidthInPixels("00", fontSec);
        var gap = (w * 0.018).toNumber();

        var totalW = hourW + gap + colonW + gap + minW;
        if (totalW > w * 0.88) {
            return false;
        }

        // 布局居中偏上 (0.19 * h)，整体上提给下方大肥猫与景物留足空间
        var startX = ((w - totalW) / 2).toNumber();
        var topY = (h * 0.19).toNumber();
        var bigCenterY = (topY + digitH / 2).toNumber();

        var colonX = startX + hourW + gap;
        var rightX = colonX + colonW + gap;
        var minTopY = showSeconds ? topY : ((topY + (digitH - minH) / 2).toNumber());
        var minCenterY = (minTopY + minH / 2).toNumber();

        // 1. 小时 HH (最大)
        dc.setColor(theme.colorHour, Graphics.COLOR_TRANSPARENT);
        drawCentered(dc, (startX + hourW / 2).toNumber(), bigCenterY, fontHour, hourStr);

        // 2. 冒号 : (垂直对齐分钟中心，自然上提避开下方肥猫头顶！)
        dc.setColor(theme.colorMin, Graphics.COLOR_TRANSPARENT);
        drawCentered(dc, (colonX + colonW / 2).toNumber(), minCenterY, fontHour, ":");

        // 3. 分钟 MM (右上，72 比例)
        drawCentered(dc, (rightX + minW / 2).toNumber(), minCenterY, fontMin, minStr);

        // 4. 秒钟 SS (MM 下方，18 比例，居中对齐 MM 的最后一个数字，+4px 呼吸缝防重叠)
        if (showSeconds) {
            dc.setColor(theme.colorSec, Graphics.COLOR_TRANSPARENT);
            var lastMinDigitCenterX = (rightX + (minW * 0.75)).toNumber();
            var secCenterY = (topY + digitH - secH / 2 + 4).toNumber();
            drawCentered(dc, lastMinDigitCenterX, secCenterY, fontSec, secStr);
        }
        return true;
    }

    private static function drawCentered(dc as Graphics.Dc, cx as Number, cy as Number, font as Graphics.FontType, text as String) as Void {
        dc.drawText(cx, cy, font, text, Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);
    }

    private static function loadTiers(h as Number, fontId as Number) as Array {
        try {
            if (fontId == 1) {
                if (h >= 380) {
                    return [
                        Application.loadResource(Rez.Fonts.f1_split_big),
                        Application.loadResource(Rez.Fonts.f1_split_mid),
                        Application.loadResource(Rez.Fonts.f1_split_mini)
                    ];
                }
                return [
                    Application.loadResource(Rez.Fonts.f1_split_mip_big),
                    Application.loadResource(Rez.Fonts.f1_split_mip_mid),
                    Application.loadResource(Rez.Fonts.f1_split_mip_mini)
                ];
            }
            if (fontId == 4) {
                if (h >= 380) {
                    return [
                        Application.loadResource(Rez.Fonts.f4_lcd_big),
                        Application.loadResource(Rez.Fonts.f4_lcd_mid),
                        Application.loadResource(Rez.Fonts.f4_lcd_mini)
                    ];
                }
                return [
                    Application.loadResource(Rez.Fonts.f4_lcd_mip_big),
                    Application.loadResource(Rez.Fonts.f4_lcd_mip_mid),
                    Application.loadResource(Rez.Fonts.f4_lcd_mip_mini)
                ];
            }
            if (fontId == 5) {
                if (h >= 380) {
                    return [
                        Application.loadResource(Rez.Fonts.f5_nixie_big),
                        Application.loadResource(Rez.Fonts.f5_nixie_mid),
                        Application.loadResource(Rez.Fonts.f5_nixie_mini)
                    ];
                }
                return [
                    Application.loadResource(Rez.Fonts.f5_nixie_mip_big),
                    Application.loadResource(Rez.Fonts.f5_nixie_mip_mid),
                    Application.loadResource(Rez.Fonts.f5_nixie_mip_mini)
                ];
            }
            if (h >= 380) {
                return [
                    Application.loadResource(Rez.Fonts.f2_mincho_biz_big),
                    Application.loadResource(Rez.Fonts.f2_mincho_biz_mid),
                    Application.loadResource(Rez.Fonts.f2_mincho_biz_mini)
                ];
            }
            return [
                Application.loadResource(Rez.Fonts.f2_mincho_biz_mip_big),
                Application.loadResource(Rez.Fonts.f2_mincho_biz_mip_mid),
                Application.loadResource(Rez.Fonts.f2_mincho_biz_mip_mini)
            ];
        } catch (ex) {
            return [];
        }
    }

    private static function pad2(n as Number) as String {
        if (n < 10) {
            return "0" + n.toString();
        }
        return n.toString();
    }
}
