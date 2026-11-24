@echo off
set SDK=C:\Users\SHIZUKI\AppData\Roaming\Garmin\ConnectIQ\Sdks\connectiq-sdk-win-9.3.0-2026-10-20-95888f262
set PRG=d:\Garmin\Komorebi\01_watchface_app\bin\Komorebi_fr965.prg

echo Starting Connect IQ Simulator...
call "%SDK%\bin\connectiq.bat"
timeout /t 4 /nobreak >nul
echo Loading Komorebi_fr965.prg...
copy /Y "d:\Garmin\Komorebi\01_watchface_app\bin\Komorebi_fr965-settings.json" "%TEMP%\com.garmin.connectiq\GARMIN\Settings\KOMOREBI_FR965-settings.json" >nul
copy /Y "d:\Garmin\Komorebi\01_watchface_app\bin\Komorebi_fr965-settings.json" "%TEMP%\com.garmin.connectiq\GARMIN\APPS\SETTINGS\KOMOREBI_FR965-settings.json" >nul
call "%SDK%\bin\monkeydo.bat" "%PRG%" fr965
