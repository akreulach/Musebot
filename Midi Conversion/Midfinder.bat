setlocal enabledelayedexpansion
for /r %%i in (*.mid) do echo %%~ni%%~xi>> midis.txt
endlocal