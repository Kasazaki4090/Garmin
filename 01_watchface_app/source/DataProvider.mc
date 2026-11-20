import Toybox.ActivityMonitor;
import Toybox.Lang;
import Toybox.SensorHistory;
import Toybox.System;
import Toybox.Weather;

class DataProvider {
    // 电池电量 (0~100)
    public static function getBattery() as Number {
        var stats = System.getSystemStats();
        return stats.battery.toNumber();
    }

    // 实时心率 (BPM)
    public static function getHeartRate() as String {
        // 尝试从 Activity 获取
        var info = Activity.getActivityInfo();
        if (info != null && info.currentHeartRate != null) {
            return info.currentHeartRate.toString();
        }
        // 尝试从传感器历史获取
        if ((Toybox has :SensorHistory) && (Toybox.SensorHistory has :getHeartRateHistory)) {
            var hrIter = SensorHistory.getHeartRateHistory({:period => 1, :order => SensorHistory.ORDER_NEWEST_FIRST});
            var sample = hrIter.next();
            if (sample != null && sample.data != null) {
                return sample.data.toNumber().toString();
            }
        }
        return "--";
    }

    // 今日步数
    public static function getSteps() as String {
        var info = ActivityMonitor.getInfo();
        if (info != null && info.steps != null) {
            return info.steps.toString();
        }
        return "0";
    }

    // 步数目标达成百分比 (0~100)
    public static function getStepPercent() as Number {
        var info = ActivityMonitor.getInfo();
        if (info != null && info.steps != null && info.stepGoal != null && info.stepGoal > 0) {
            var pct = (info.steps.toFloat() / info.stepGoal.toFloat()) * 100.0;
            return pct > 100.0 ? 100 : pct.toNumber();
        }
        return 0;
    }

    // 卡路里 (Kcal)
    public static function getCalories() as String {
        var info = ActivityMonitor.getInfo();
        if (info != null && info.calories != null) {
            return info.calories.toString();
        }
        return "--";
    }

    // 身体电量 (Body Battery)
    public static function getBodyBattery() as String {
        if ((Toybox has :SensorHistory) && (Toybox.SensorHistory has :getBodyBatteryHistory)) {
            var bbIter = SensorHistory.getBodyBatteryHistory({:period => 1, :order => SensorHistory.ORDER_NEWEST_FIRST});
            var sample = bbIter.next();
            if (sample != null && sample.data != null) {
                return sample.data.toNumber().toString();
            }
        }
        return "--";
    }

    // 压力水平 (Stress)
    public static function getStress() as String {
        if ((Toybox has :SensorHistory) && (Toybox.SensorHistory has :getStressHistory)) {
            var stIter = SensorHistory.getStressHistory({:period => 1, :order => SensorHistory.ORDER_NEWEST_FIRST});
            var sample = stIter.next();
            if (sample != null && sample.data != null) {
                return sample.data.toNumber().toString();
            }
        }
        return "--";
    }

    // 实时气温与天气状态
    public static function getWeatherInfo() as String {
        if (Toybox has :Weather) {
            var cond = Weather.getCurrentConditions();
            if (cond != null && cond.temperature != null) {
                var temp = cond.temperature.toNumber();
                return temp.toString() + "°";
            }
        }
        return "--°";
    }
}
