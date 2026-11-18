@echo off
rem Buat folder project baru selevel dengan repo skill.
rem Pemakaian: new_project.bat Nama_Project

if "%~1"=="" (
    echo Pemakaian: new_project.bat Nama_Project
    echo Contoh   : new_project.bat Onboarding_MLE_Dify
    exit /b 1
)

set "KIT=%~dp0"
set "KIT=%KIT:~0,-1%"
for %%P in ("%KIT%\..") do set "PARENT=%%~fP"
set "PROJ=%PARENT%\%~1"

if exist "%PROJ%" (
    echo Folder %PROJ% sudah ada. Tidak ada yang diubah.
    exit /b 1
)

mkdir "%PROJ%\briefs" "%PROJ%\materi_rujukan" "%PROJ%\output"
copy "%KIT%\project-template\CLAUDE.md" "%PROJ%\CLAUDE.md" >nul
copy "%KIT%\project-template\README.md" "%PROJ%\README.md" >nul
copy "%KIT%\project-template\.gitignore" "%PROJ%\.gitignore" >nul

echo Project dibuat: %PROJ%
echo.
echo Langkah berikutnya:
echo   1. Simpan Brief ke %PROJ%\briefs\
echo   2. Simpan materi lama yang dipakai ulang ke %PROJ%\materi_rujukan\
echo   3. cd "%PROJ%" lalu jalankan: claude
