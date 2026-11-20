import Toybox.Graphics;
import Toybox.Lang;
import Toybox.Math;

class MinimalBgDrawer {
    // 绘制简笔背景
    public static function draw(dc as Graphics.Dc, width as Number, height as Number, mode as Number, color as Number) as Void {
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.setPenWidth(2);

        switch (mode) {
            case 1:
                drawFujiSun(dc, width, height);
                break;
            case 2:
                drawUkiyoClouds(dc, width, height);
                break;
            case 3:
                drawMistyPeaks(dc, width, height);
                break;
            case 4:
                drawRainRipples(dc, width, height);
                break;
            case 5:
                drawSnowCrest(dc, width, height);
                break;
            case 6:
                drawMoonCat(dc, width, height);
                break;
            default:
                drawFujiSun(dc, width, height);
                break;
        }
    }

    // B1: 晴 · 远山日轮 (富士山折线 + 日轮空心圆 + 横穿云线)
    private static function drawFujiSun(dc as Graphics.Dc, w as Number, h as Number) as Void {
        var baseRatioY = 0.68;
        var baseY = (h * baseRatioY).toNumber();

        // 富士山折线 (左山脚 -> 缓坡 -> 陡坡 -> 平坦火山口 -> 陡坡 -> 缓坡 -> 右山脚)
        var x0 = (w * 0.08).toNumber();
        var x1 = (w * 0.22).toNumber();
        var y1 = baseY - (h * 0.08).toNumber();
        var x2 = (w * 0.38).toNumber();
        var y2 = baseY - (h * 0.22).toNumber();
        var x3 = (w * 0.44).toNumber();
        var y3 = y2;
        var x4 = (w * 0.60).toNumber();
        var y4 = y1;
        var x5 = (w * 0.75).toNumber();

        dc.drawLine(x0, baseY, x1, y1);
        dc.drawLine(x1, y1, x2, y2);
        dc.drawLine(x2, y2, x3, y3); // 火山口平台
        dc.drawLine(x3, y3, x4, y4);
        dc.drawLine(x4, y4, x5, baseY);

        // 右上角空心日轮 (半径约 5% 宽)
        var sunX = (w * 0.78).toNumber();
        var sunY = (h * 0.28).toNumber();
        var sunR = (w * 0.05).toNumber();
        dc.drawCircle(sunX, sunY, sunR);

        // 两条浮云细线
        var cloudY1 = baseY - (h * 0.04).toNumber();
        dc.drawLine((w * 0.25).toNumber(), cloudY1, (w * 0.55).toNumber(), cloudY1);
        var cloudY2 = baseY + (h * 0.02).toNumber();
        dc.drawLine((w * 0.15).toNumber(), cloudY2, (w * 0.40).toNumber(), cloudY2);
    }

    // B2: 云 · 浮世流云 (日式源氏霞云线: 水平圆角带状线条)
    private static function drawUkiyoClouds(dc as Graphics.Dc, w as Number, h as Number) as Void {
        var cy1 = (h * 0.26).toNumber();
        var cy2 = (h * 0.66).toNumber();

        // 上方流云
        dc.drawLine((w * 0.15).toNumber(), cy1, (w * 0.48).toNumber(), cy1);
        dc.drawLine((w * 0.22).toNumber(), cy1 + 6, (w * 0.60).toNumber(), cy1 + 6);

        // 下方流云
        dc.drawLine((w * 0.40).toNumber(), cy2, (w * 0.85).toNumber(), cy2);
        dc.drawLine((w * 0.32).toNumber(), cy2 + 6, (w * 0.72).toNumber(), cy2 + 6);
    }

    // B3: 阴/雾 · 水墨层峦 (前后两重山峦 + 雾线)
    private static function drawMistyPeaks(dc as Graphics.Dc, w as Number, h as Number) as Void {
        var baseY = (h * 0.70).toNumber();

        // 远景山脊 (虚线或浅线)
        dc.drawLine((w * 0.10).toNumber(), baseY, (w * 0.35).toNumber(), baseY - (h * 0.18).toNumber());
        dc.drawLine((w * 0.35).toNumber(), baseY - (h * 0.18).toNumber(), (w * 0.60).toNumber(), baseY);

        // 近景山脊
        dc.drawLine((w * 0.40).toNumber(), baseY, (w * 0.65).toNumber(), baseY - (h * 0.14).toNumber());
        dc.drawLine((w * 0.65).toNumber(), baseY - (h * 0.14).toNumber(), (w * 0.90).toNumber(), baseY);

        // 山脚晨雾水平短线
        dc.drawLine((w * 0.20).toNumber(), baseY + 4, (w * 0.80).toNumber(), baseY + 4);
        dc.drawLine((w * 0.30).toNumber(), baseY + 9, (w * 0.70).toNumber(), baseY + 9);
    }

    // B4: 雨 · 细雨涟漪 (右上微云 + 倾斜雨丝 + 水波椭圆)
    private static function drawRainRipples(dc as Graphics.Dc, w as Number, h as Number) as Void {
        // 斜细雨丝 (60度)
        var dx = 6;
        var dy = 14;
        var rainPositions = [
            [(w * 0.25).toNumber(), (h * 0.28).toNumber()],
            [(w * 0.45).toNumber(), (h * 0.32).toNumber()],
            [(w * 0.65).toNumber(), (h * 0.25).toNumber()],
            [(w * 0.35).toNumber(), (h * 0.58).toNumber()],
            [(w * 0.72).toNumber(), (h * 0.60).toNumber()]
        ];

        for (var i = 0; i < rainPositions.size(); i++) {
            var pt = rainPositions[i];
            dc.drawLine(pt[0], pt[1], pt[0] - dx, pt[1] + dy);
        }

        // 水波涟漪 (底部扁平椭圆)
        var rx = (w * 0.50).toNumber();
        var ry = (h * 0.70).toNumber();
        dc.drawEllipse(rx, ry, (w * 0.18).toNumber(), (h * 0.03).toNumber());
        dc.drawEllipse(rx + 10, ry + 6, (w * 0.10).toNumber(), (h * 0.02).toNumber());
    }

    // B5: 雪 · 雪峰寒星 (带雪冠折线峰 + 米字雪花)
    private static function drawSnowCrest(dc as Graphics.Dc, w as Number, h as Number) as Void {
        var baseY = (h * 0.70).toNumber();
        var peakX = (w * 0.40).toNumber();
        var peakY = baseY - (h * 0.20).toNumber();

        // 山峰
        dc.drawLine((w * 0.15).toNumber(), baseY, peakX, peakY);
        dc.drawLine(peakX, peakY, (w * 0.70).toNumber(), baseY);

        // 雪冠折线 (Z 字型雪线)
        var sy = peakY + (h * 0.06).toNumber();
        dc.drawLine(peakX - 10, sy, peakX - 2, sy + 4);
        dc.drawLine(peakX - 2, sy + 4, peakX + 5, sy - 2);
        dc.drawLine(peakX + 5, sy - 2, peakX + 12, sy + 5);

        // 散落极简几何雪花 (3线交叉成星)
        drawSnowflake(dc, (w * 0.75).toNumber(), (h * 0.25).toNumber(), 4);
        drawSnowflake(dc, (w * 0.25).toNumber(), (h * 0.35).toNumber(), 3);
        drawSnowflake(dc, (w * 0.82).toNumber(), (h * 0.52).toNumber(), 3);
    }

    private static function drawSnowflake(dc as Graphics.Dc, x as Number, y as Number, r as Number) as Void {
        dc.drawLine(x, y - r, x, y + r);
        dc.drawLine(x - r, y, x + r, y);
        dc.drawLine(x - (r * 0.7).toNumber(), y - (r * 0.7).toNumber(), x + (r * 0.7).toNumber(), y + (r * 0.7).toNumber());
    }

    // B6: 夜 · 弦月眠猫 (右上细弯月 + 小星点 + 趴卧小猫剪影线)
    private static function drawMoonCat(dc as Graphics.Dc, w as Number, h as Number) as Void {
        // 右上角弯月 (两圆相切差弧)
        var mx = (w * 0.76).toNumber();
        var my = (h * 0.24).toNumber();
        var mr = (w * 0.07).toNumber();
        dc.drawCircle(mx, my, mr);

        // 星辰小十字
        var sx = (w * 0.65).toNumber();
        var sy = (h * 0.32).toNumber();
        dc.drawLine(sx - 3, sy, sx + 3, sy);
        dc.drawLine(sx, sy - 3, sx, sy + 3);

        // 简笔小猫弧线 (趴在时间分界线上)
        var cx = (w * 0.45).toNumber();
        var cy = (h * 0.68).toNumber();
        // 猫背弧线
        dc.drawArc(cx, cy + 10, 16, Graphics.ARC_CLOCKWISE, 140, 20);
        // 猫耳折线
        dc.drawLine(cx + 8, cy - 3, cx + 12, cy - 10);
        dc.drawLine(cx + 12, cy - 10, cx + 15, cy - 4);
        dc.drawLine(cx + 15, cy - 4, cx + 18, cy - 8);
        dc.drawLine(cx + 18, cy - 8, cx + 21, cy - 2);
    }
}
