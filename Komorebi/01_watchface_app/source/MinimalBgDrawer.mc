import Toybox.Graphics;
import Toybox.Lang;
import Toybox.Math;

// 极简日系背景：圆相（禅圈）框住时间 + 地平线 + 右上角按模式点缀符号
class MinimalBgDrawer {
    public static function draw(dc as Graphics.Dc, width as Number, height as Number, mode as Number, color as Number) as Void {
        var w = width;
        var h = height;
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.setPenWidth(2);

        // 1. 圆相（Ensō）：一个大圆环，左下留缺口，框住中央时间
        drawEnso(dc, w, h);

        // 2. 地平线：底部一条淡墨横线
        var hy = (h * 0.80).toNumber();
        dc.drawLine((w * 0.16).toNumber(), hy, (w * 0.84).toNumber(), hy);

        // 3. 右上角模式符号（克制，单一元素）
        switch (mode) {
            case 1: drawSun(dc, w, h); break;       // 晴 · 日轮
            case 2: drawClouds(dc, w, h); break;    // 云 · 流云
            case 3: drawMist(dc, w, h); break;      // 雾 · 远山
            case 4: drawRain(dc, w, h); break;      // 雨 · 雨丝
            case 5: drawSnow(dc, w, h); break;      // 雪 · 雪花
            case 6: drawMoon(dc, w, h); break;      // 夜 · 弦月
            default: drawSun(dc, w, h); break;
        }
    }

    // 圆相：约 86% 直径的圆环，左下留一段缺口（手绘禅意）
    private static function drawEnso(dc as Graphics.Dc, w as Number, h as Number) as Void {
        var cx = (w / 2).toNumber();
        var cy = (h / 2).toNumber();
        var side = w < h ? w : h;
        var r = ((side / 2) * 0.86).toNumber();
        dc.setPenWidth(3);
        // 从 130° 顺时针画到 95°（即左下留约 35° 缺口）
        dc.drawArc(cx, cy, r, Graphics.ARC_CLOCKWISE, 130, 95);
        dc.setPenWidth(2);
    }

    // 日轮：实心小圆点（朱印感）
    private static function drawSun(dc as Graphics.Dc, w as Number, h as Number) as Void {
        var sx = (w * 0.74).toNumber();
        var sy = (h * 0.20).toNumber();
        var r = (w * 0.035).toNumber();
        dc.drawCircle(sx, sy, r);
    }

    // 流云：两条长短错落的水平线
    private static function drawClouds(dc as Graphics.Dc, w as Number, h as Number) as Void {
        var y = (h * 0.20).toNumber();
        dc.drawLine((w * 0.66).toNumber(), y, (w * 0.84).toNumber(), y);
        dc.drawLine((w * 0.72).toNumber(), (y + 7).toNumber(), (w * 0.82).toNumber(), (y + 7).toNumber());
    }

    // 远山：一个简洁折线山脊
    private static function drawMist(dc as Graphics.Dc, w as Number, h as Number) as Void {
        var y = (h * 0.22).toNumber();
        dc.drawLine((w * 0.66).toNumber(), y, (w * 0.74).toNumber(), (y - 12).toNumber());
        dc.drawLine((w * 0.74).toNumber(), (y - 12).toNumber(), (w * 0.84).toNumber(), y);
    }

    // 雨丝：三条短斜线
    private static function drawRain(dc as Graphics.Dc, w as Number, h as Number) as Void {
        var x = (w * 0.72).toNumber();
        var y = (h * 0.18).toNumber();
        for (var i = 0; i < 3; i++) {
            var px = (x + i * 8).toNumber();
            dc.drawLine(px, y, (px - 4).toNumber(), (y + 12).toNumber());
        }
    }

    // 雪花：单枚米字星
    private static function drawSnow(dc as Graphics.Dc, w as Number, h as Number) as Void {
        var x = (w * 0.74).toNumber();
        var y = (h * 0.20).toNumber();
        var r = (w * 0.03).toNumber();
        dc.drawLine(x, (y - r).toNumber(), x, (y + r).toNumber());
        dc.drawLine((x - r).toNumber(), y, (x + r).toNumber(), y);
        var d = (r * 0.7).toNumber();
        dc.drawLine((x - d).toNumber(), (y - d).toNumber(), (x + d).toNumber(), (y + d).toNumber());
        dc.drawLine((x - d).toNumber(), (y + d).toNumber(), (x + d).toNumber(), (y - d).toNumber());
    }

    // 弦月：两圆相切形成的弯月
    private static function drawMoon(dc as Graphics.Dc, w as Number, h as Number) as Void {
        var mx = (w * 0.74).toNumber();
        var my = (h * 0.20).toNumber();
        var r = (w * 0.04).toNumber();
        dc.drawCircle(mx, my, r);
    }
}
