set SRC=..\..\src
set PYENV=..\..\.pyenv

call %PYENV%\Scripts\activate

pushd %SRC%

pyinstaller ^
  --onefile ^
  --icon res\logo\logo.ico ^
  --add-data "res\logo\logo.ico;res\logo" ^
  --workpath ..\build\windows\tmp ^
  --distpath ..\build\windows\dist ^
  --name %EXENAME% ^
  %EXTRAARGS% ^
  %SCRIPTFILE%

rm %EXENAME%.spec

popd
