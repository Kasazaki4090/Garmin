import Toybox.Application;
import Toybox.Lang;
import Toybox.WatchUi;

class WatchFaceApp extends Application.AppBase {
    private var mView as WatchFaceView?;

    function initialize() {
        AppBase.initialize();
    }

    function onStart(state as Lang.Dictionary?) as Void {
    }

    function onStop(state as Lang.Dictionary?) as Void {
    }

    function getInitialView() as [WatchUi.Views] or [WatchUi.Views, WatchUi.InputDelegates] {
        mView = new WatchFaceView();
        return [mView];
    }

    // 当用户在手机 Garmin Connect App 修改设置时触发
    function onSettingsChanged() as Void {
        if (mView != null) {
            mView.onSettingsChanged();
        }
    }
}

function getApp() as WatchFaceApp {
    return Application.getApp() as WatchFaceApp;
}
