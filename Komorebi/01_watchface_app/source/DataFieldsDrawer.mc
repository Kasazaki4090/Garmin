import Toybox.Graphics;
import Toybox.Lang;
import Toybox.Time;
import Toybox.Time.Gregorian;

class DataFieldsDrawer {
    // 渲染顶部状态栏 (左: 电池图标+百分比 | 中: 日期 | 右: 气温)
    public static function drawTopZone(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager) as Void {
        var topY = (h * 0.135).toNumber();

        // 1. 电池 (居左：微型电池框 + 百分比，左移到 0.19 * w 避免撞到中间日期)
        var batt = DataProvider.getBattery();
        var battColor = batt <= 20 ? theme.colorAccent : theme.colorData;
        var bx = (w * 0.19).toNumber();
        var bw = (w * 0.042).toNumber();
        var bh = (h * 0.022).toNumber();
        if (bw < 12) { bw = 12; }
        if (bh < 7) { bh = 7; }
        var by = (topY - bh / 2).toNumber();

        dc.setColor(battColor, Graphics.COLOR_TRANSPARENT);
        dc.setPenWidth(1);
        dc.drawRectangle(bx, by, bw, bh);
        // 电池右侧极耳
        var nubH = (bh * 0.5).toNumber();
        dc.fillRectangle(bx + bw, (topY - nubH / 2).toNumber(), 2, nubH);
        // 内部电量填充块
        var innerW = (((bw - 4) * batt) / 100.0).toNumber();
        if (innerW > 0) {
            dc.fillRectangle(bx + 2, by + 2, innerW, bh - 4);
        }
        var battStr = Lang.format("$1$%", [batt]);
        dc.drawText(
            bx + bw + 5,
            topY,
            Graphics.FONT_XTINY,
            battStr,
            Graphics.TEXT_JUSTIFY_LEFT | Graphics.TEXT_JUSTIFY_VCENTER
        );

        // 2. 日期 (居中)
        var now = Time.now();
        var info = Gregorian.info(now, Time.FORMAT_SHORT);
        var dateStr = Lang.format("$1$/$2$", [info.month.format("%02d"), info.day.format("%02d")]);
        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            (w * 0.50).toNumber(),
            topY,
            Graphics.FONT_XTINY,
            dateStr,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );

        // 3. 气温 (居右)
        var weatherStr = DataProvider.getWeatherInfo() + "C";
        dc.drawText(
            (w * 0.72).toNumber(),
            topY,
            Graphics.FONT_XTINY,
            weatherStr,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );
    }

    // 渲染底部身体数据矩阵 (2x2 微型矢量图标 + 数值，无横线干扰)
    public static function drawBottomZone(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager) as Void {
        var row1Y = (h * 0.785).toNumber();
        var row2Y = (h * 0.870).toNumber();
        var iconOff = (w * 0.025).toNumber();
        if (iconOff < 8) { iconOff = 8; }

        // 第一排左：心率 (茜红小爱心 + BPM)
        var hrX = (w * 0.32).toNumber();
        drawHeartIcon(dc, hrX, row1Y, theme.colorAccent);
        dc.setColor(theme.colorAccent, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            hrX + iconOff,
            row1Y,
            Graphics.FONT_XTINY,
            DataProvider.getHeartRate(),
            Graphics.TEXT_JUSTIFY_LEFT | Graphics.TEXT_JUSTIFY_VCENTER
        );

        // 第一排右：身体电量 (小闪电 + 数值)
        var bbX = (w * 0.60).toNumber();
        drawBoltIcon(dc, bbX, row1Y, theme.colorMin);
        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            bbX + iconOff,
            row1Y,
            Graphics.FONT_XTINY,
            DataProvider.getBodyBattery(),
            Graphics.TEXT_JUSTIFY_LEFT | Graphics.TEXT_JUSTIFY_VCENTER
        );

        // 第二排左：步数 (双脚印 + 步数)
        var stX = (w * 0.34).toNumber();
        drawFootIcon(dc, stX, row2Y, theme.colorData);
        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            stX + iconOff,
            row2Y,
            Graphics.FONT_XTINY,
            DataProvider.getSteps(),
            Graphics.TEXT_JUSTIFY_LEFT | Graphics.TEXT_JUSTIFY_VCENTER
        );

        // 第二排右：压力 (空心菱形 + 压力值)
        var strX = (w * 0.58).toNumber();
        drawDiamondIcon(dc, strX, row2Y, theme.colorData);
        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            strX + iconOff,
            row2Y,
            Graphics.FONT_XTINY,
            DataProvider.getStress(),
            Graphics.TEXT_JUSTIFY_LEFT | Graphics.TEXT_JUSTIFY_VCENTER
        );
        dc.setPenWidth(1);
    }

    // 绘制左右边缘进度弧 (采用严格 Garmin 逆时针角度系 + 0% 防满圆特判)
    public static function drawArcs(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager) as Void {
        if (theme.arcMode == 0) {
            return;
        }
        var cx = (w / 2).toNumber();
        var cy = (h / 2).toNumber();
        var r = ((w / 2) - 5).toNumber();
        dc.setPenWidth(theme.arcMode == 1 ? 3 : 5);

        // 左弧：电池电量 (由下往上：220° 顺时针扫向 140°)
        var batt = DataProvider.getBattery();
        if (batt > 1) {
            var battEnd = (220 - ((batt / 100.0) * 80.0)).toNumber();
            dc.setColor(theme.colorAccent, Graphics.COLOR_TRANSPARENT);
            dc.drawArc(cx, cy, r, Graphics.ARC_CLOCKWISE, 220, battEnd);
        }

        // 右弧：步数达成率 (由下往上：320° 逆时针扫向 40°)
        var stepPct = DataProvider.getStepPercent();
        if (stepPct > 1) {
            var stepEnd = ((320 + ((stepPct / 100.0) * 80.0)).toNumber()) % 360;
            dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
            dc.drawArc(cx, cy, r, Graphics.ARC_COUNTER_CLOCKWISE, 320, stepEnd);
        }
        dc.setPenWidth(1);
    }

    // --- 微型矢量图标库 (零位图、抗锯齿实心多边形) ---
    private static function drawHeartIcon(dc as Graphics.Dc, cx as Number, cy as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.fillCircle(cx - 3, cy - 2, 3);
        dc.fillCircle(cx + 3, cy - 2, 3);
        dc.fillPolygon([[cx - 6, cy - 1], [cx + 6, cy - 1], [cx, cy + 6]]);
    }

    private static function drawBoltIcon(dc as Graphics.Dc, cx as Number, cy as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.fillPolygon([
            [cx + 2, cy - 7],
            [cx - 4, cy + 1],
            [cx,     cy + 1],
            [cx - 2, cy + 7],
            [cx + 4, cy - 1],
            [cx,     cy - 1]
        ]);
    }

    private static function drawFootIcon(dc as Graphics.Dc, cx as Number, cy as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.fillCircle(cx - 2, cy - 3, 2);
        dc.fillCircle(cx + 2, cy + 2, 2);
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
