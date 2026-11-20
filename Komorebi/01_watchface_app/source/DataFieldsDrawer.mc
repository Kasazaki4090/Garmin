import Toybox.Graphics;
import Toybox.Lang;
import Toybox.Time;
import Toybox.Time.Gregorian;

class DataFieldsDrawer {
    // 渲染顶部数据 (电池 + 天气 + 简短日期)
    public static function drawTopZone(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager) as Void {
        var topY = (h * 0.12).toNumber();

        // 1. 日期与星期 (居中)
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

        // 2. 电池百分比 (居左)
        var batt = DataProvider.getBattery();
        var battStr = Lang.format("$1$%", [batt]);
        dc.setColor(batt <= 20 ? theme.colorAccent : theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            (w * 0.28).toNumber(),
            topY,
            Graphics.FONT_XTINY,
            battStr,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );

        // 3. 气温 (居右)
        var weatherStr = DataProvider.getWeatherInfo();
        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            (w * 0.72).toNumber(),
            topY,
            Graphics.FONT_XTINY,
            weatherStr,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );
    }

    // 渲染底部数据矩阵 (心率 / 身体电量 / 步数 / 卡路里)
    public static function drawBottomZone(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager) as Void {
        var row1Y = (h * 0.76).toNumber();
        var row2Y = (h * 0.86).toNumber();

        // 第一排：心率 (左) 与 身体电量 (右)
        var hr = DataProvider.getHeartRate();
        var hrStr = "HR " + hr;
        dc.setColor(theme.colorAccent, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            (w * 0.35).toNumber(),
            row1Y,
            Graphics.FONT_XTINY,
            hrStr,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );

        var bb = DataProvider.getBodyBattery();
        var bbStr = "BB " + bb;
        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            (w * 0.65).toNumber(),
            row1Y,
            Graphics.FONT_XTINY,
            bbStr,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );

        // 第二排：步数 (居中偏左) 与 压力 (居中偏右)
        var steps = DataProvider.getSteps();
        var stepStr = "ST " + steps;
        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            (w * 0.35).toNumber(),
            row2Y,
            Graphics.FONT_XTINY,
            stepStr,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );

        var stress = DataProvider.getStress();
        var stressStr = "STRESS " + stress;
        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            (w * 0.65).toNumber(),
            row2Y,
            Graphics.FONT_XTINY,
            stressStr,
            Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER
        );
    }

    // 绘制左右边缘进度弧
    public static function drawArcs(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager) as Void {
        if (theme.arcMode == 0) {
            return; // 关闭弧线
        }

        var cx = (w / 2).toNumber();
        var cy = (h / 2).toNumber();
        var r = ((w / 2) - 4).toNumber();

        dc.setPenWidth(theme.arcMode == 1 ? 2 : 4);

        // 左弧：电池电量进度 (140° 到 220°)
        var batt = DataProvider.getBattery();
        var battAngle = 140 + ((batt / 100.0) * 80.0);
        dc.setColor(theme.colorAccent, Graphics.COLOR_TRANSPARENT);
        dc.drawArc(cx, cy, r, Graphics.ARC_COUNTER_CLOCKWISE, 140, battAngle.toNumber());

        // 右弧：步数达成率进度 (40° 到 320° 倒转)
        var stepPct = DataProvider.getStepPercent();
        var stepAngle = 40 - ((stepPct / 100.0) * 80.0);
        if (stepAngle < 0) {
            stepAngle += 360;
        }
        dc.setColor(theme.colorData, Graphics.COLOR_TRANSPARENT);
        dc.drawArc(cx, cy, r, Graphics.ARC_CLOCKWISE, 40, stepAngle.toNumber());
    }
}
