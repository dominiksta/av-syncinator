if (Test-Path -Path "tmp\ffmpeg.exe") {
    Write-Output "Found ffmpeg"
} else {
    Write-Output "Die not find ffmpeg, downloading now..."
    Invoke-WebRequest -OutFile tmp\ffmpeg.zip `
    https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    Expand-Archive -Force tmp\ffmpeg.zip tmp\ffmpeg
    Copy-Item (Get-ChildItem -Path .\tmp\ffmpeg\ -Recurse ffmpeg.exe).fullname `
    tmp\ffmpeg.exe
}
