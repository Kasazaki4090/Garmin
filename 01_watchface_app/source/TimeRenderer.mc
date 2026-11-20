import Toybox.Graphics;
import Toybox.Lang;
import Toybox.System;
import Toybox.Time;
import Toybox.Time.Gregorian;

class TimeRenderer {
    // 渲染时间核心区域 (错落大时间排版)
    public static function drawTime(
        dc as Graphics.Dc, 
        w as Number, 
        h as Number, 
        theme as ThemeManager, 
        is24Hour as Boolean, 
        showSeconds as Boolean
    ) as Void {
        var clockTime = System.getClockTime();
        var hour = clockTime.hour;
        if (!is24Hour) {
            hour = hour % 12;
            if (hour == 0) {
                hour = 12;
            }
        }
        var hourStr = Lang.format("$1$", [hour.format("%02d")]);
        var minStr = Lang.format("$1$", [clockTime.min.format("%02d")]);
        var secStr = Lang.format("$1$", [clockTime.sec.format("%02d")]);

        // 基准坐标 (依据百分比计算，适配 260x260 与 454x454)
        // 小时：居左偏中，超大字体
        var hourX = (w * 0.44).toNumber();
        var hourY = (h * 0.42).toNumber();

        // 分钟：紧邻小时右侧，稍小字号，贴合圆形边缘
        var minX = (w * 0.52).toNumber();
        var minY = (h * 0.32).toNumber();

        // 秒钟：置于分钟下方，补齐右侧高度落差
        var secX = (w * 0.65).toNumber();
        var secY = (h * 0.53).toNumber();

        // 1. 绘制小时 (大字号)
        dc.setColor(theme.colorHour, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            hourX,
            hourY,
            Graphics.FONT_NUMBER_HOT,
            hourStr,
            Graphics.TEXT_JUSTIFY_RIGHT | Graphics.TEXT_JUSTIFY_VCENTER
        );

        // 2. 绘制分钟 (中大字号)
        dc.setColor(theme.colorMin, Graphics.COLOR_TRANSPARENT);
        dc.drawText(
            minX,
            minY,
            Graphics.FONT_NUMBER_MEDIUM,
            minStr,
            Graphics.TEXT_JUSTIFY_LEFT | Graphics.TEXT_JUSTIFY_VCENTER
        );

        // 3. 绘制秒钟 (小字号，AOD息屏模式下隐藏)
        if (showSeconds) {
            dc.setColor(theme.colorSec, Graphics.COLOR_TRANSPARENT);
            dc.drawText(
                secX,
                secY,
                Graphics.FONT_SYSTEM_SMALL,
                secStr,
                Graphics.TEXT_JUSTIFY_LEFT | Graphics.TEXT_JUSTIFY_VCENTER
            );
        }
    }
}
