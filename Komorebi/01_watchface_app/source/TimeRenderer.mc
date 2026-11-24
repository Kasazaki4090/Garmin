import Toybox.Graphics;
import Toybox.Lang;

// 时间渲染分发层：
//   F1 = iPhone 裂开 Mono 字库
//   F2 = 衬线 / 宋朝体 字库
//   其余 / 字库加载失败 → SegmentClock（严格等宽 Mono 矢量段码）
class TimeRenderer {
    public static function draw(dc as Graphics.Dc, w as Number, h as Number, theme as ThemeManager, is24Hour as Boolean, showSeconds as Boolean) as Void {
        if (theme.fontId == 1 || theme.fontId == 2 || theme.fontId == 4 || theme.fontId == 5 || theme.fontId == 6) {
            if (SerifClock.draw(dc, w, h, theme, is24Hour, showSeconds)) {
                return;
            }
        }
        SegmentClock.draw(dc, w, h, theme, is24Hour, showSeconds);
    }
}
