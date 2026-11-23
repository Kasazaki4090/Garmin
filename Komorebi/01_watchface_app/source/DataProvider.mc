import Toybox.Activity;
import Toybox.ActivityMonitor;
import Toybox.Lang;
import Toybox.SensorHistory;
import Toybox.System;
import Toybox.UserProfile;
import Toybox.Weather;

class DataProvider {
    // 电池电量 (0~100)
    public static function getBattery() as Number {
        var stats = System.getSystemStats();
        return stats.battery.toNumber();
    }

    // 实时心率 (BPM)
    public static function getHeartRate() as String {
        var info = Activity.getActivityInfo();
        if (info != null && info.currentHeartRate != null) {
            return info.currentHeartRate.toString();
        }
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
    public static function getBodyBatteryNum() as Number {
        if ((Toybox has :SensorHistory) && (Toybox.SensorHistory has :getBodyBatteryHistory)) {
            var bbIter = SensorHistory.getBodyBatteryHistory({:period => 1, :order => SensorHistory.ORDER_NEWEST_FIRST});
            var sample = bbIter.next();
            if (sample != null && sample.data != null) {
                return sample.data.toNumber();
            }
        }
        return -1;
    }

    public static function getBodyBattery() as String {
        var v = getBodyBatteryNum();
        return v >= 0 ? v.toString() : "--";
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

    // 今日距离 (km / mi)
    public static function getDistanceStr() as String {
        var info = ActivityMonitor.getInfo();
        if (info != null && info.distance != null) {
            var settings = System.getDeviceSettings();
            if (settings.distanceUnits == System.UNIT_STATUTE) {
                var mi = info.distance.toFloat() / 160934.4;
                return mi.format("%.1f") + " mi";
            }
            var km = info.distance.toFloat() / 100000.0;
            return km.format("%.1f") + " km";
        }
        return "--";
    }

    // 海拔 (m / ft)
    public static function getAltitudeStr() as String {
        var altM = null as Float?;
        var act = Activity.getActivityInfo();
        if (act != null && act.altitude != null) {
            altM = act.altitude.toFloat();
        } else if ((Toybox has :SensorHistory) && (Toybox.SensorHistory has :getElevationHistory)) {
            var elIter = SensorHistory.getElevationHistory({:period => 1, :order => SensorHistory.ORDER_NEWEST_FIRST});
            var sample = elIter.next();
            if (sample != null && sample.data != null) {
                altM = sample.data.toFloat();
            }
        }
        if (altM != null) {
            var settings = System.getDeviceSettings();
            if (settings.elevationUnits == System.UNIT_STATUTE) {
                return (altM * 3.28084).toNumber().toString() + " ft";
            }
            return altM.toNumber().toString() + " m";
        }
        return "--";
    }

    // 爬楼层数
    public static function getFloorsStr() as String {
        var info = ActivityMonitor.getInfo();
        if (info != null && (info has :floorsClimbed) && info.floorsClimbed != null) {
            return info.floorsClimbed.toString();
        }
        return "--";
    }

    // 最大摄氧量 (VO2 Max)
    public static function getVo2MaxStr() as String {
        if (Toybox has :UserProfile) {
            var prof = UserProfile.getProfile();
            if (prof != null && (prof has :vo2maxRunning) && prof.vo2maxRunning != null) {
                return prof.vo2maxRunning.toString();
            }
        }
        return "--";
    }

    // 今日高强度活动分钟
    public static function getActiveMinutesNum() as Number {
        var info = ActivityMonitor.getInfo();
        if (info != null && (info has :activeMinutesDay) && info.activeMinutesDay != null) {
            return info.activeMinutesDay.total;
        }
        return -1;
    }

    public static function getActiveMinutesStr() as String {
        var m = getActiveMinutesNum();
        return m >= 0 ? m.toString() + " m" : "--";
    }

    // 消息通知数
    public static function getNotificationsStr() as String {
        var settings = System.getDeviceSettings();
        if (settings has :notificationCount) {
            return settings.notificationCount.toString();
        }
        return "0";
    }

    // 实时气温
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

    // 实时天气状态文本
    public static function getWeatherConditionStr() as String {
        if (Toybox has :Weather) {
            var cond = Weather.getCurrentConditions();
            if (cond != null && cond.condition != null) {
                var c = cond.condition;
                if (c == Weather.CONDITION_RAIN || c == Weather.CONDITION_LIGHT_RAIN ||
                    c == Weather.CONDITION_HEAVY_RAIN || c == Weather.CONDITION_SHOWERS ||
                    c == Weather.CONDITION_DRIZZLE || c == Weather.CONDITION_CHANCE_OF_SHOWERS ||
                    c == Weather.CONDITION_SCATTERED_SHOWERS) {
                    return "RAIN";
                }
                if (c == Weather.CONDITION_THUNDERSTORMS || c == Weather.CONDITION_CHANCE_OF_THUNDERSTORMS) {
                    return "STORM";
                }
                if (c == Weather.CONDITION_SNOW || c == Weather.CONDITION_LIGHT_SNOW ||
                    c == Weather.CONDITION_HEAVY_SNOW || c == Weather.CONDITION_WINTRY_MIX ||
                    c == Weather.CONDITION_RAIN_SNOW || c == Weather.CONDITION_SLEET ||
                    c == Weather.CONDITION_HAIL || c == Weather.CONDITION_CHANCE_OF_SNOW) {
                    return "SNOW";
                }
                if (c == Weather.CONDITION_FOG || c == Weather.CONDITION_HAZY ||
                    c == Weather.CONDITION_MIST || c == Weather.CONDITION_SMOKE) {
                    return "FOG";
                }
                if (c == Weather.CONDITION_CLOUDY || c == Weather.CONDITION_MOSTLY_CLOUDY ||
                    c == Weather.CONDITION_PARTLY_CLOUDY || c == Weather.CONDITION_THIN_CLOUDS) {
                    return "CLOUDY";
                }
                if (c == Weather.CONDITION_WINDY) {
                    return "WINDY";
                }
                return "CLEAR";
            }
        }
        return "--";
    }

    // 弧线进度条百分比 (0~100): 0=关闭, 1=电量, 2=步数目标, 3=身体电量, 4=活动分钟(以30分钟为日标)
    public static function getArcProgress(arcMetric as Number) as Number {
        switch (arcMetric) {
            case 1: return getBattery();
            case 2: return getStepPercent();
            case 3:
                var bb = getBodyBatteryNum();
                return bb >= 0 ? bb : 0;
            case 4:
                var am = getActiveMinutesNum();
                if (am <= 0) { return 0; }
                var pct = (am * 100 / 30).toNumber();
                return pct > 100 ? 100 : pct;
            default:
                return 0;
        }
    }

    // 统一返回 [短标签, 数值文本] 供底部与两翼槽位渲染
    public static function getMetricDisplay(metricId as Number) as Array<String> {
        switch (metricId) {
            case 1:  return ["HR", getHeartRate() + " bpm"];
            case 2:  return ["STEPS", getSteps()];
            case 3:  return ["BODY BAT", getBodyBattery()];
            case 4:  return ["STRESS", getStress()];
            case 5:  return ["", getCalories() + " kcal"];
            case 6:  return ["", getDistanceStr()];
            case 7:  return ["ALT", getAltitudeStr()];
            case 8:  return ["FLOORS", getFloorsStr()];
            case 9:  return ["BAT", getBattery().toString() + "%"];
            case 10: return ["VO2", getVo2MaxStr()];
            case 11: return ["ACTIVE", getActiveMinutesStr()];
            case 12: return ["GOAL", getStepPercent().toString() + "%"];
            case 13: return ["MSG", getNotificationsStr()];
            default: return ["", ""];
        }
    }

    // 两翼大号只取纯数字或精简值，底部取完整带标签值
    public static function getWingValue(metricId as Number) as String {
        switch (metricId) {
            case 1:  return getHeartRate();
            case 2:  return getSteps();
            case 3:  return getBodyBattery();
            case 4:  return getStress();
            case 5:  return getCalories();
            case 6:  return getDistanceStr();
            case 7:  return getAltitudeStr();
            case 8:  return getFloorsStr();
            case 9:  return getBattery().toString() + "%";
            case 10: return getVo2MaxStr();
            case 11: return getActiveMinutesStr();
            case 12: return getStepPercent().toString() + "%";
            case 13: return getNotificationsStr();
            default: return "";
        }
    }

    public static function getWingSubLabel(metricId as Number) as String {
        switch (metricId) {
            case 1:  return "HR BPM";
            case 2:  return getStepPercent().toString() + "%";
            case 3:  return "BODY BAT";
            case 4:  return "STRESS";
            case 5:  return "KCAL";
            case 6:  return "DIST";
            case 7:  return "ALT";
            case 8:  return "FLOORS";
            case 9:  return "BATTERY";
            case 10: return "VO2 MAX";
            case 11: return "ACTIVE";
            case 12: return "STEP GOAL";
            case 13: return "ALERTS";
            default: return "";
        }
    }
}
