set BASE=..\..\

call powershell -File get-ffmpeg.ps1
call %BASE%\.pyenv\Scripts\activate

pushd %BASE%

pyinstaller ^
  --onefile ^
  --icon avsyncinator\res\logo\logo.ico ^
  --add-data "avsyncinator\res\logo\logo.ico;res\logo" ^
  --add-data "build\windows\tmp\ffmpeg.exe;." ^
  --workpath build\windows\tmp ^
  --distpath build\windows\dist ^
  --name %EXENAME% ^
  %EXTRAARGS% ^
  %SCRIPTFILE%

rm %EXENAME%.spec

popd
