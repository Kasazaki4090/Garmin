import Toybox.Graphics;
import Toybox.Lang;
import Toybox.Time;
import Toybox.Time.Gregorian;

class DataFieldsDrawer {
    private static const WEEKDAYS = ["", "SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];

    // 渲染顶部状态栏：
    //   第1行 (到顶): 电池图标 + 百分比 (居中)
    //   第2行: 日期 - 星期(可选) - 气温 (居中)
    //   第3行 (可选): 天气状态 (居中)
    public static function drawTopZone(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager) as Void {
        // 1. 顶部居中：电池图标 + 百分比 (上提至 0.070h 留出呼吸空间)
        var topY = (h * 0.070).toNumber();
        var batt = DataProvider.getBattery();
        var battColor = batt <= 20 ? theme.colorAccent : theme.colorData;
        var battStr = Lang.format("$1$%", [batt]);

        var bw = (w * 0.052).toNumber();
        var bh = (h * 0.026).toNumber();
        if (bw < 14) { bw = 14; }
        if (bh < 8) { bh = 8; }
        var textW = dc.getTextWidthInPixels(battStr, Graphics.FONT_XTINY);
        var gap = (w * 0.015).toNumber();
        if (gap < 4) { gap = 4; }
        var totalBattW = bw + 2 + gap + textW;

        var bx = ((w - totalBattW) / 2).toNumber();
        var by = (topY - bh / 2).toNumber();

        dc.setColor(battColor, Graphics.COLOR_TRANSPARENT);
        dc.setPenWidth(1);
        dc.drawRectangle(bx, by, bw, bh);
        var nubH = (bh * 0.5).toNumber();
        dc.fillRectangle(bx + bw, (topY - nubH / 2).toNumber(), 2, nubH);
        var innerW = (((bw - 4) * batt) / 100.0).toNumber();
        if (innerW > 0) {
            dc.fillRectangle(bx + 2, by + 2, innerW, bh - 4);
        }
        dc.drawText(
            bx + bw + 2 + gap,
            topY,
            Graphics.FONT_XTINY,
            battStr,
            Graphics.TEXT_JUSTIFY_LEFT | Graphics.TEXT_JUSTIFY_VCENTER
        );

        // 2. 第二行：日期 - 星期(可选) - 气温
        var row2Y = (h * 0.132).toNumber();
        var now = Time.now();
        var info = Gregorian.info(now, Time.FORMAT_SHORT);
        var dateStr = Lang.format("$1$/$2$", [info.month.format("%02d"), info.day.format("%02d")]);
        var tempStr = DataProvider.getWeatherInfo();

        var line2 = dateStr;
        if (theme.showWeekday && info.day_of_week >= 1 && info.day_of_week <= 7) {
            line2 = line2 + " " + WEEKDAYS[info.day_of_week];
        }
        line2 = line2 + " " + tempStr;

        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            (w * 0.50).toNumber(),
            row2Y,
            Graphics.FONT_XTINY,
            line2,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );

        // 3. 第三行（可选）：天气状态
        if (theme.showWeatherCond) {
            var row3Y = (h * 0.188).toNumber();
            dc.setColor(theme.colorBgLines, Graphics.COLOR_TRANSPARENT);
            dc.drawText(
                (w * 0.50).toNumber(),
                row3Y,
                Graphics.FONT_XTINY,
                DataProvider.getWeatherConditionStr(),
                Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
            );
        }
    }

    // 渲染下半屏两翼指标 + 底部 1-2-2 数据矩阵 (全部槽位可在设置中自由替换)
    public static function drawBottomZone(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager) as Void {
        // 1. 下半屏左右两翼（贴合弧线内侧）
        var wingY = (h * 0.575).toNumber();
        drawWingSlot(dc, w, h, (w * 0.22).toNumber(), wingY, theme.slotWingL, theme.colorAccent, theme);
        drawWingSlot(dc, w, h, (w * 0.78).toNumber(), wingY, theme.slotWingR, theme.colorMin, theme);

        // 2. 底部第 1 行（1 个居中突出显示，默认心率）
        var bot1Y = (h * 0.695).toNumber();
        if (theme.slotBot1 != 0) {
            drawCompactMetric(dc, w, (w * 0.50).toNumber(), bot1Y, theme.slotBot1, theme.colorAccent, theme);
        }

        // 3. 底部第 2 行（2 个并排；若隐藏其中一个则自动居中）
        var bot2Y = (h * 0.780).toNumber();
        drawBottomPair(dc, w, bot2Y, (w * 0.35).toNumber(), (w * 0.65).toNumber(), theme.slotBot2, theme.slotBot3, theme);

        // 4. 底部第 3 行（2 个并排；若隐藏其中一个则自动居中）
        var bot3Y = (h * 0.865).toNumber();
        drawBottomPair(dc, w, bot3Y, (w * 0.37).toNumber(), (w * 0.63).toNumber(), theme.slotBot4, theme.slotBot5, theme);

        dc.setPenWidth(1);
    }

    // 绘制下半屏左右弧线进度条 (238°->180° 左下弧, 302°->360° 右下弧，绝不遮挡时钟)
    public static function drawArcs(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager) as Void {
        if (theme.arcMode == 0) {
            return;
        }
        var cx = (w / 2).toNumber();
        var cy = (h / 2).toNumber();
        var r = ((w / 2) - 6).toNumber();
        var penW = theme.arcMode == 1 ? 4 : 6;
        dc.setPenWidth(penW);

        // 左下弧
        if (theme.leftArcMetric != 0) {
            // 底轨
            dc.setColor(theme.colorBgLines, Graphics.COLOR_TRANSPARENT);
            dc.drawArc(cx, cy, r, Graphics.ARC_CLOCKWISE, 238, 180);

            var leftPct = DataProvider.getArcProgress(theme.leftArcMetric);
            if (leftPct > 1) {
                var leftEnd = (238 - ((leftPct / 100.0) * 58.0)).toNumber();
                dc.setColor(theme.colorAccent, Graphics.COLOR_TRANSPARENT);
                dc.drawArc(cx, cy, r, Graphics.ARC_CLOCKWISE, 238, leftEnd);
            }
        }

        // 右下弧
        if (theme.rightArcMetric != 0) {
            // 底轨
            dc.setColor(theme.colorBgLines, Graphics.COLOR_TRANSPARENT);
            dc.drawArc(cx, cy, r, Graphics.ARC_COUNTER_CLOCKWISE, 302, 0);

            var rightPct = DataProvider.getArcProgress(theme.rightArcMetric);
            if (rightPct > 1) {
                var rightEnd = ((302 + ((rightPct / 100.0) * 58.0)).toNumber()) % 360;
                dc.setColor(theme.colorMin, Graphics.COLOR_TRANSPARENT);
                dc.drawArc(cx, cy, r, Graphics.ARC_COUNTER_CLOCKWISE, 302, rightEnd);
            }
        }
        dc.setPenWidth(1);
    }

    // 绘制左右两翼槽位：小图标与数值同行居中 + 下方小标签，绝不与上方时钟和下方标签重叠
    private static function drawWingSlot(dc as Graphics.Dc, w as Number, h as Number, cx as Number, cy as Number, metricId as Number, iconColor as Number, theme as ThemeManager) as Void {
        if (metricId == 0) {
            return;
        }
        var valStr = DataProvider.getWingValue(metricId);
        var valY = (cy - h * 0.015).toNumber();
        var subY = (cy + h * 0.048).toNumber();

        var valW = dc.getTextWidthInPixels(valStr, Graphics.FONT_SMALL);
        var iconSpace = (w * 0.032).toNumber();
        if (iconSpace < 12) { iconSpace = 12; }
        var totalW = iconSpace + valW;
        var startX = (cx - totalW / 2).toNumber();

        drawMetricIcon(dc, metricId, startX + 4, valY, iconColor);

        dc.setColor(theme.colorHour, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            startX + iconSpace,
            valY,
            Graphics.FONT_SMALL,
            valStr,
            Graphics.TEXT_JUSTIFY_LEFT | Graphics.TEXT_JUSTIFY_VCENTER
        );

        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            cx,
            subY,
            Graphics.FONT_XTINY,
            DataProvider.getWingSubLabel(metricId),
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );
    }

    private static function drawBottomPair(dc as Graphics.Dc, w as Number, y as Number, xLeft as Number, xRight as Number, leftId as Number, rightId as Number, theme as ThemeManager) as Void {
        if (leftId != 0 && rightId != 0) {
            drawCompactMetric(dc, w, xLeft, y, leftId, theme.colorData, theme);
            drawCompactMetric(dc, w, xRight, y, rightId, theme.colorData, theme);
        } else if (leftId != 0) {
            drawCompactMetric(dc, w, (w * 0.50).toNumber(), y, leftId, theme.colorData, theme);
        } else if (rightId != 0) {
            drawCompactMetric(dc, w, (w * 0.50).toNumber(), y, rightId, theme.colorData, theme);
        }
    }

    // 绘制紧凑型单指标：[图标] [标签 数值] 整体水平居中于 cx
    private static function drawCompactMetric(dc as Graphics.Dc, w as Number, cx as Number, cy as Number, metricId as Number, iconColor as Number, theme as ThemeManager) as Void {
        var pair = DataProvider.getMetricDisplay(metricId);
        var label = pair[0];
        var val = pair[1];
        if (val.equals("")) {
            return;
        }
        var fullText = label.equals("") ? val : (label + " " + val);
        var textW = dc.getTextWidthInPixels(fullText, Graphics.FONT_XTINY);
        var iconSpace = (w * 0.032).toNumber();
        if (iconSpace < 12) { iconSpace = 12; }
        var totalW = iconSpace + textW;
        var startX = (cx - totalW / 2).toNumber();

        drawMetricIcon(dc, metricId, startX + 4, cy, metricId == 1 ? theme.colorAccent : iconColor);

        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            startX + iconSpace,
            cy,
            Graphics.FONT_XTINY,
            fullText,
            Graphics.TEXT_JUSTIFY_LEFT | Graphics.TEXT_JUSTIFY_VCENTER
        );
    }

    // --- 微型矢量图标库 (零位图、抗锯齿实心多边形) ---
    private static function drawMetricIcon(dc as Graphics.Dc, metricId as Number, cx as Number, cy as Number, color as Number) as Void {
        switch (metricId) {
            case 1:  drawHeartIcon(dc, cx, cy, color); break;
            case 2:
            case 12: drawFootIcon(dc, cx, cy, color); break;
            case 3:
            case 9:  drawBoltIcon(dc, cx, cy, color); break;
            case 5:  drawFlameIcon(dc, cx, cy, color); break;
            case 6:
            case 11: drawDotRingIcon(dc, cx, cy, color); break;
            case 7:
            case 8:  drawMountainIcon(dc, cx, cy, color); break;
            default: drawDiamondIcon(dc, cx, cy, color); break;
        }
    }

    private static function drawHeartIcon(dc as Graphics.Dc, cx as Number, cy as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.fillCircle(cx - 3, cy - 2, 3);
        dc.fillCircle(cx + 3, cy - 2, 3);
        dc.fillPolygon([[cx - 6, cy - 1], [cx + 6, cy - 1], [cx, cy + 6]]);
    }

    private static function drawBoltIcon(dc as Graphics.Dc, cx as Number, cy as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.fillPolygon([
            [cx + 2, cy - 6],
            [cx - 4, cy + 1],
            [cx,     cy + 1],
            [cx - 2, cy + 6],
            [cx + 4, cy - 1],
            [cx,     cy - 1]
        ]);
    }

    private static function drawFootIcon(dc as Graphics.Dc, cx as Number, cy as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.fillCircle(cx - 2, cy - 3, 2);
        dc.fillCircle(cx + 2, cy + 2, 2);
    }

    private static function drawMountainIcon(dc as Graphics.Dc, cx as Number, cy as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.fillPolygon([[cx - 6, cy + 4], [cx - 1, cy - 5], [cx + 4, cy + 4]]);
        dc.fillPolygon([[cx, cy + 4], [cx + 4, cy - 2], [cx + 7, cy + 4]]);
    }

    private static function drawFlameIcon(dc as Graphics.Dc, cx as Number, cy as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.fillCircle(cx, cy + 2, 3);
        dc.fillPolygon([[cx - 3, cy + 2], [cx, cy - 6], [cx + 3, cy + 2]]);
    }

    private static function drawDotRingIcon(dc as Graphics.Dc, cx as Number, cy as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.setPenWidth(1);
        dc.drawCircle(cx, cy, 4);
        dc.fillCircle(cx, cy, 2);
    }

    private static function drawDiamondIcon(dc as Graphics.Dc, cx as Number, cy as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.setPenWidth(1);
        dc.drawLine(cx, cy - 5, cx + 5, cy);
        dc.drawLine(cx + 5, cy, cx, cy + 5);
        dc.drawLine(cx, cy + 5, cx - 5, cy);
        dc.drawLine(cx - 5, cy, cx, cy - 5);
    }
}
