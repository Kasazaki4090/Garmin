import Toybox.Application;
import Toybox.Graphics;
import Toybox.Lang;
import Toybox.System;
import Toybox.WatchUi;

class WatchFaceView extends WatchUi.WatchFace {
    private var mTheme as ThemeManager;
    private var mIsSleeping as Boolean = false;

    function initialize() {
        WatchFace.initialize();
        mTheme = new ThemeManager();
    }

    function onLayout(dc as Graphics.Dc) as Void {
        // 自定义布局直接通过 Dc 动态计算
    }

    function onShow() as Void {
    }

    function onUpdate(dc as Graphics.Dc) as Void {
        var w = dc.getWidth();
        var h = dc.getHeight();

        // 1. 绘制表盘底色 (清屏)
        dc.setColor(mTheme.colorBg, mTheme.colorBg);
        dc.clear();

        // 2. 绘制极简几何日系简笔画背景 (息屏时不绘制简笔背景，节省 AMOLED 烧屏风险和 MIP 功耗)
        if (!mIsSleeping) {
            MinimalBgDrawer.draw(dc, w, h, mTheme.bgMode, mTheme.colorBgLines);
        }

        // 3. 绘制核心错落大时间
        var is24Hour = System.getDeviceSettings().is24Hour;
        TimeRenderer.drawTime(dc, w, h, mTheme, is24Hour, !mIsSleeping);

        // 4. 绘制顶部状态 (电量/天气/日期)
        DataFieldsDrawer.drawTopZone(dc, w, h, mTheme);

        // 5. 绘制底部身体数据矩阵 (心率/压力/身体电量/步数)
        DataFieldsDrawer.drawBottomZone(dc, w, h, mTheme);

        // 6. 绘制左右边缘弧线 (如果启用)
        DataFieldsDrawer.drawArcs(dc, w, h, mTheme);
    }

    function onHide() as Void {
    }

    // 进入低功耗休眠 (关闭每秒秒针刷新，关闭重度背景)
    function onEnterSleep() as Void {
        mIsSleeping = true;
        WatchUi.requestUpdate();
    }

    // 唤醒表盘 (抬腕/轻触)
    function onExitSleep() as Void {
        mIsSleeping = false;
        WatchUi.requestUpdate();
    }

    // 设置项发生变更时由 App 调用
    public function onSettingsChanged() as Void {
        mTheme.reloadTheme();
        WatchUi.requestUpdate();
    }
}
