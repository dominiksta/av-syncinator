set SRC=..\..\src
set PYENV=..\..\.pyenv

call powershell -File get-ffmpeg.ps1
call %PYENV%\Scripts\activate

pushd %SRC%

pyinstaller ^
  --onefile ^
  --icon res\logo\logo.ico ^
  --add-data "res\logo\logo.ico;res\logo" ^
  --add-data "..\build\windows\tmp\ffmpeg.exe;." ^
  --workpath ..\build\windows\tmp ^
  --distpath ..\build\windows\dist ^
  --name %EXENAME% ^
  %EXTRAARGS% ^
  %SCRIPTFILE%

rm %EXENAME%.spec

popd
