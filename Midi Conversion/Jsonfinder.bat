setlocal enabledelayedexpansion
for /r %%i in (*.json) do echo %%~ni%%~xi>> Jsons.txt
endlocal