@echo off
setlocal EnableDelayedExpansion
rem Pasang semua skill di repo ini secara global untuk Claude Code (level user).
rem Jalankan ulang setiap kali ada skill baru atau repo dipindah. Tidak perlu admin.

set "KIT=%~dp0"
set "KIT=%KIT:~0,-1%"
set "DEST=%USERPROFILE%\.claude\skills"

echo Kit root : %KIT%
echo Tujuan   : %DEST%
echo.

if not exist "%DEST%" mkdir "%DEST%"

for /d %%S in ("%KIT%\.claude\skills\*") do (
    set "NAME=%%~nxS"
    rem Junction lama dari instalasi sebelumnya dihapus dulu (isi repo tidak ikut terhapus).
    dir /AL /B "%DEST%" 2>nul | findstr /X /C:"!NAME!" >nul && rmdir "%DEST%\!NAME!"
    if exist "%DEST%\!NAME!" (
        echo [LEWATI] %DEST%\!NAME! sudah ada sebagai folder biasa. Pindahkan atau hapus dulu, lalu jalankan ulang.
    ) else (
        mklink /J "%DEST%\!NAME!" "%%~fS" >nul && echo [OK] !NAME!
    )
)

setx TRAINING_KIT_HOME "%KIT%" >nul
echo.
echo [OK] TRAINING_KIT_HOME = %KIT%

where npm >nul 2>&1 && (
    echo.
    echo Menjalankan npm install di kit root...
    pushd "%KIT%" && call npm install --silent && popd
)

echo.
echo Selesai. Tutup lalu buka ulang terminal agar TRAINING_KIT_HOME terbaca.
echo Pastikan juga: pip install python-docx openpyxl
endlocal
