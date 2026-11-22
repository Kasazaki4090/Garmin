import Toybox.Application;
import Toybox.Graphics;
import Toybox.Lang;
import Toybox.System;
import Toybox.Weather;
import Toybox.WatchUi;

// 全屏圆表盘水彩背景绘制器 (454x454 满屏绘制，带自动白天/夜间/天气切换)
class MinimalBgDrawer {
    private static var mCachedMode as Number = -1;
    private static var mCachedBitmap as WatchUi.BitmapResource? = null;

    public static function draw(dc as Graphics.Dc, width as Number, height as Number, mode as Number, lineColor as Number) as Void {
        var activeMode = resolveMode(mode);

        if (activeMode != mCachedMode || mCachedBitmap == null) {
            mCachedMode = activeMode;
            mCachedBitmap = loadSceneBitmap(activeMode);
        }

        if (mCachedBitmap != null) {
            var bmp = mCachedBitmap as WatchUi.BitmapResource;
            var bw = bmp.getWidth();
            var bh = bmp.getHeight();
            var bx = ((width - bw) / 2).toNumber();
            var by = ((height - bh) / 2).toNumber();
            dc.drawBitmap(bx, by, bmp);
        }
    }

    private static function resolveMode(mode as Number) as Number {
        if (mode >= 1 && mode <= 6) {
            return mode;
        }
        var clock = System.getClockTime();
        if (clock.hour >= 19 || clock.hour < 6) {
            return 6;
        }
        if (Toybox has :Weather) {
            var cond = Weather.getCurrentConditions();
            if (cond != null && cond.condition != null) {
                var c = cond.condition;
                // 4. 雨 / 雷暴 / 台风 / 热带风暴
                if (c == Weather.CONDITION_RAIN || c == Weather.CONDITION_LIGHT_RAIN ||
                    c == Weather.CONDITION_HEAVY_RAIN || c == Weather.CONDITION_SHOWERS ||
                    c == Weather.CONDITION_THUNDERSTORMS || c == Weather.CONDITION_CHANCE_OF_SHOWERS ||
                    c == Weather.CONDITION_SCATTERED_SHOWERS || c == Weather.CONDITION_DRIZZLE ||
                    c == Weather.CONDITION_CHANCE_OF_THUNDERSTORMS || c == Weather.CONDITION_HURRICANE ||
                    c == Weather.CONDITION_TROPICAL_STORM || c == Weather.CONDITION_SQUALL) {
                    return 4;
                }
                // 5. 雪 / 雨夹雪 / 冻雨 / 冰雹
                if (c == Weather.CONDITION_SNOW || c == Weather.CONDITION_LIGHT_SNOW ||
                    c == Weather.CONDITION_HEAVY_SNOW || c == Weather.CONDITION_WINTRY_MIX ||
                    c == Weather.CONDITION_RAIN_SNOW || c == Weather.CONDITION_SLEET ||
                    c == Weather.CONDITION_HAIL || c == Weather.CONDITION_CHANCE_OF_SNOW ||
                    c == Weather.CONDITION_FREEZING_RAIN || c == Weather.CONDITION_ICE) {
                    return 5;
                }
                // 3. 雾 / 阴天 / 霾 / 沙尘
                if (c == Weather.CONDITION_FOG || c == Weather.CONDITION_HAZY ||
                    c == Weather.CONDITION_MIST || c == Weather.CONDITION_SMOKE ||
                    c == Weather.CONDITION_CLOUDY || c == Weather.CONDITION_MOSTLY_CLOUDY ||
                    c == Weather.CONDITION_DUST || c == Weather.CONDITION_SAND ||
                    c == Weather.CONDITION_SANDSTORM) {
                    return 3;
                }
                // 2. 多云 / 少云 / 微风
                if (c == Weather.CONDITION_PARTLY_CLOUDY || c == Weather.CONDITION_MOSTLY_CLEAR ||
                    c == Weather.CONDITION_PARTLY_CLEAR || c == Weather.CONDITION_THIN_CLOUDS ||
                    c == Weather.CONDITION_WINDY) {
                    return 2;
                }
            }
        }
        return 1;
    }

    private static function loadSceneBitmap(mode as Number) as WatchUi.BitmapResource? {
        try {
            switch (mode) {
                case 1: return Application.loadResource(Rez.Drawables.BgScene1) as WatchUi.BitmapResource;
                case 2: return Application.loadResource(Rez.Drawables.BgScene2) as WatchUi.BitmapResource;
                case 3: return Application.loadResource(Rez.Drawables.BgScene3) as WatchUi.BitmapResource;
                case 4: return Application.loadResource(Rez.Drawables.BgScene4) as WatchUi.BitmapResource;
                case 5: return Application.loadResource(Rez.Drawables.BgScene5) as WatchUi.BitmapResource;
                case 6: return Application.loadResource(Rez.Drawables.BgScene6) as WatchUi.BitmapResource;
                default: return Application.loadResource(Rez.Drawables.BgScene1) as WatchUi.BitmapResource;
            }
        } catch (ex) {
            return null;
        }
    }
}
