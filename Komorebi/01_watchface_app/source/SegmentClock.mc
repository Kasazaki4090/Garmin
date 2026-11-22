import Toybox.Graphics;
import Toybox.Lang;
import Toybox.System;

// 矢量段码时钟：45°斜切六边形段码 + 数字1动态紧缩 + 严格5段间距
class SegmentClock {
    private static const DIGITS = [
        [1, 1, 1, 1, 1, 1, 0], // 0
        [0, 1, 1, 0, 0, 0, 0], // 1
        [1, 1, 0, 1, 1, 0, 1], // 2
        [1, 1, 1, 1, 0, 0, 1], // 3
        [0, 1, 1, 0, 0, 1, 1], // 4
        [1, 0, 1, 1, 0, 1, 1], // 5
        [1, 0, 1, 1, 1, 1, 1], // 6
        [1, 1, 1, 0, 0, 0, 0], // 7
        [1, 1, 1, 1, 1, 1, 1], // 8
        [1, 1, 1, 1, 0, 1, 1]  // 9
    ];

    public static function draw(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager, is24Hour as Boolean, showSeconds as Boolean) as Void {
        var clockTime = System.getClockTime();
        var hour = clockTime.hour;
        if (!is24Hour) {
            hour = hour % 12;
            if (hour == 0) {
                hour = 12;
            }
        }
        var h1 = (hour / 10).toNumber();
        var h2 = hour % 10;
        var m1 = (clockTime.min / 10).toNumber();
        var m2 = clockTime.min % 10;
        var s1 = (clockTime.sec / 10).toNumber();
        var s2 = clockTime.sec % 10;

        var digitH = (h * 0.30).toNumber();
        var digitW = (digitH * 0.48).toNumber();
        var thick = (digitH * 0.115).toNumber();

        var minH = (digitH * 0.60).toNumber();
        var minW = (minH * 0.50).toNumber();
        var minT = (minH * 0.12).toNumber();

        var secH = (digitH * 0.27).toNumber();
        var secW = (secH * 0.54).toNumber();
        var secT = (secH * 0.15).toNumber();
        if (secT < 2) { secT = 2; }

        var hGap = (digitW * 0.22).toNumber();
        var colonW = (digitW * 0.24).toNumber();
        var minGap = (minW * 0.25).toNumber();
        var secGap = (secW * 0.28).toNumber();

        var advH1 = getAdvance(h1, digitW);
        var advH2 = getAdvance(h2, digitW);
        var advM1 = getAdvance(m1, minW);
        var advM2 = getAdvance(m2, minW);
        var advS1 = getAdvance(s1, secW);
        var advS2 = getAdvance(s2, secW);

        var minTotalW = advM1 + minGap + advM2;
        var secTotalW = advS1 + secGap + advS2;
        var rightColW = minTotalW > secTotalW ? minTotalW : secTotalW;

        var totalW = advH1 + hGap + advH2 + hGap + colonW + hGap + rightColW;
        var startX = ((w - totalW) / 2).toNumber();
        var topY = (h * 0.25).toNumber();

        var x = startX;
        drawDigit(dc, x, topY, digitW, digitH, thick, h1, theme.colorHour);
        x += advH1 + hGap;
        drawDigit(dc, x, topY, digitW, digitH, thick, h2, theme.colorHour);
        x += advH2 + hGap;

        drawColon(dc, x, topY, colonW, digitH, thick, theme.colorMin);
        x += colonW + hGap;

        var minTopY = showSeconds ? topY : ((topY + (digitH - minH) / 2).toNumber());
        drawDigit(dc, x, minTopY, minW, minH, minT, m1, theme.colorMin);
        drawDigit(dc, x + advM1 + minGap, minTopY, minW, minH, minT, m2, theme.colorMin);

        if (showSeconds) {
            var minRight = x + minTotalW;
            var secX = minRight - secTotalW;
            var secY = topY + digitH - secH;
            drawDigit(dc, secX, secY, secW, secH, secT, s1, theme.colorSec);
            drawDigit(dc, secX + advS1 + secGap, secY, secW, secH, secT, s2, theme.colorSec);
        }
        dc.setPenWidth(1);
    }

    private static function getAdvance(digit as Number, dw as Number) as Number {
        return digit == 1 ? (dw * 0.36).toNumber() : dw;
    }

    private static function drawDigit(dc as Graphics.Dc, x as Number, y as Number, dw as Number, dh as Number, t as Number, digit as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        var midY = (y + dh / 2).toNumber();
        var yb = y + dh;

        if (digit == 1) {
            var cx = x + (getAdvance(1, dw) / 2).toNumber();
            fillVSeg(dc, cx, y, midY, t);
            fillVSeg(dc, cx, midY, yb, t);
            return;
        }

        var x2 = x + dw;
        var seg = DIGITS[digit];
        if (seg[0] == 1) { fillHSeg(dc, x, x2, y, t); }
        if (seg[1] == 1) { fillVSeg(dc, x2, y, midY, t); }
        if (seg[2] == 1) { fillVSeg(dc, x2, midY, yb, t); }
        if (seg[3] == 1) { fillHSeg(dc, x, x2, yb, t); }
        if (seg[4] == 1) { fillVSeg(dc, x, midY, yb, t); }
        if (seg[5] == 1) { fillVSeg(dc, x, y, midY, t); }
        if (seg[6] == 1) { fillHSeg(dc, x, x2, midY, t); }
    }

    private static function fillHSeg(dc as Graphics.Dc, x1 as Number, x2 as Number, cy as Number, t as Number) as Void {
        var h = (t / 2).toNumber();
        if (h < 1) { h = 1; }
        var g = (t * 0.14).toNumber();
        if (g < 1) { g = 1; }
        var ax1 = x1 + g;
        var ax2 = x2 - g;
        if (ax2 <= ax1 + 2 * h) { return; }
        dc.fillPolygon([
            [ax1, cy],
            [ax1 + h, cy - h],
            [ax2 - h, cy - h],
            [ax2, cy],
            [ax2 - h, cy + h],
            [ax1 + h, cy + h]
        ]);
    }

    private static function fillVSeg(dc as Graphics.Dc, cx as Number, y1 as Number, y2 as Number, t as Number) as Void {
        var h = (t / 2).toNumber();
        if (h < 1) { h = 1; }
        var g = (t * 0.14).toNumber();
        if (g < 1) { g = 1; }
        var ay1 = y1 + g;
        var ay2 = y2 - g;
        if (ay2 <= ay1 + 2 * h) { return; }
        dc.fillPolygon([
            [cx, ay1],
            [cx + h, ay1 + h],
            [cx + h, ay2 - h],
            [cx, ay2],
            [cx - h, ay2 - h],
            [cx - h, ay1 + h]
        ]);
    }

    private static function drawColon(dc as Graphics.Dc, x as Number, y as Number, cw as Number, dh as Number, t as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        var dot = (t * 0.95).toNumber();
        if (dot < 2) { dot = 2; }
        var cx = (x + cw / 2).toNumber();
        var y1 = (y + dh * 0.34).toNumber();
        var y2 = (y + dh * 0.66).toNumber();
        dc.fillRectangle((cx - dot / 2).toNumber(), (y1 - dot / 2).toNumber(), dot, dot);
        dc.fillRectangle((cx - dot / 2).toNumber(), (y2 - dot / 2).toNumber(), dot, dot);
    }
}
