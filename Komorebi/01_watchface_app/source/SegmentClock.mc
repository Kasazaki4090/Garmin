import Toybox.Graphics;
import Toybox.Lang;
import Toybox.System;
import Toybox.Time;
import Toybox.Time.Gregorian;

// 矢量段码时钟：自绘七段数码，尺寸可控，让 HH:MM 占据屏幕主体
class SegmentClock {
    // 每个数字用 7 段的开关表示 (a,b,c,d,e,f,g)
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

    // 绘制主时间 HH:MM，居中，占据约 40% 屏高
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

        // ===== 主从式布局：HH 大字在左，MM 小字在右上，SS 迷你字在右下 =====
        // 约束：分 + 秒 的总高 = 时字高度；整体水平垂直居中
        var digitH = (h * 0.34).toNumber();          // 时字高度（主）
        var digitW = (digitH * 0.46).toNumber();
        var thick = (digitH * 0.09).toNumber();

        var minH = (digitH * 0.72).toNumber();       // 分字高度
        var minW = (minH * 0.46).toNumber();
        var minT = (minH * 0.09).toNumber();

        var secH = (digitH * 0.18).toNumber();       // 秒字高度（分+隙+秒 = digitH）
        var secW = (secH * 0.46).toNumber();
        var secT = (secH * 0.10).toNumber();
        var msGap = digitH - minH - secH;            // 分秒之间的空隙

        var gap = (digitW * 0.22).toNumber();
        var colonW = (digitW * 0.45).toNumber();
        var totalW = digitW * 2 + gap * 2 + colonW + minW * 2;
        var maxW = w * 0.72;
        if (totalW > maxW) {
            var scale = maxW / totalW;
            digitH = (digitH * scale).toNumber();
            digitW = (digitW * scale).toNumber();
            thick = (thick * scale).toNumber();
            minH = (minH * scale).toNumber();
            minW = (minW * scale).toNumber();
            minT = (minT * scale).toNumber();
            secH = (secH * scale).toNumber();
            secW = (secW * scale).toNumber();
            secT = (secT * scale).toNumber();
            msGap = (msGap * scale).toNumber();
            gap = (gap * scale).toNumber();
            colonW = (colonW * scale).toNumber();
            totalW = (digitW * 2 + gap * 2 + colonW + minW * 2).toNumber();
        }
        var startX = ((w - totalW) / 2).toNumber();
        var topY = ((h - digitH) / 2).toNumber();

        var s1 = (clockTime.sec / 10).toNumber();
        var s2 = clockTime.sec % 10;
        // 秒不显示时，分钟垂直居中于时字高度；显示时上对齐、秒垫底
        var minTopY = showSeconds ? topY : ((topY + (digitH - minH) / 2).toNumber());
        var rightX = (startX + digitW * 2 + gap * 2 + colonW).toNumber();

        var x = startX;
        // 小时（十位、个位）— 大字
        drawDigit(dc, x, topY, digitW, digitH, thick, h1, theme.colorHour);
        x += digitW + gap;
        drawDigit(dc, x, topY, digitW, digitH, thick, h2, theme.colorHour);
        x += digitW + gap;
        // 冒号（朱印红，垂直居中）
        drawColon(dc, x, topY, colonW, digitH, thick, theme.colorMin);
        x += colonW + gap;
        // 分钟（十位、个位）— 小字
        drawDigit(dc, rightX, minTopY, minW, minH, minT, m1, theme.colorMin);
        drawDigit(dc, (rightX + minW).toNumber(), minTopY, minW, minH, minT, m2, theme.colorMin);

        // 秒钟：迷你段码字，垫在分钟正下方（息屏隐藏）
        if (showSeconds) {
            var secTopY = (minTopY + minH + msGap).toNumber();
            drawDigit(dc, (rightX + minW - secW).toNumber(), secTopY, secW, secH, secT, s1, theme.colorSec);
            drawDigit(dc, (rightX + minW).toNumber(), secTopY, secW, secH, secT, s2, theme.colorSec);
        }
    }

    // 绘制单个段码数字
    private static function drawDigit(dc as Graphics.Dc, x as Number, y as Number, dw as Number, dh as Number, t as Number, digit as Number, color as Number) as Void {
        var seg = DIGITS[digit];
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.setPenWidth(t);
        var half = (t / 2).toNumber();
        var midY = (y + dh / 2).toNumber();
        var x2 = (x + dw).toNumber();
        var yb = (y + dh).toNumber();

        // a 顶
        if (seg[0] == 1) { dc.drawLine(x + half, y, x2 - half, y); }
        // b 右上
        if (seg[1] == 1) { dc.drawLine(x2, y + half, x2, midY - half); }
        // c 右下
        if (seg[2] == 1) { dc.drawLine(x2, midY + half, x2, yb - half); }
        // d 底
        if (seg[3] == 1) { dc.drawLine(x + half, yb, x2 - half, yb); }
        // e 左下
        if (seg[4] == 1) { dc.drawLine(x, midY + half, x, yb - half); }
        // f 左上
        if (seg[5] == 1) { dc.drawLine(x, y + half, x, midY - half); }
        // g 中
        if (seg[6] == 1) { dc.drawLine(x + half, midY, x2 - half, midY); }
    }

    // 绘制冒号（两个方点）
    private static function drawColon(dc as Graphics.Dc, x as Number, y as Number, cw as Number, dh as Number, t as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        var dot = (t * 1.1).toNumber();
        var cx = (x + cw / 2).toNumber();
        var y1 = (y + dh * 0.34).toNumber();
        var y2 = (y + dh * 0.66).toNumber();
        dc.drawRectangle((cx - dot / 2).toNumber(), (y1 - dot / 2).toNumber(), dot, dot);
        dc.drawRectangle((cx - dot / 2).toNumber(), (y2 - dot / 2).toNumber(), dot, dot);
    }
}
