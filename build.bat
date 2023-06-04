@REM archive name
FOR /F "tokens=*" %%g IN ('python3 -c "import version; print(version.VERSION.strip())"') do (SET VAR=%%g)
set rel_dir="wow_tts"
set "zipFile=wowtts_%VAR%.zip"
rmdir /s /q "%rel_dir%"
del %zipFile%

mkdir %rel_dir%\bin
mkdir %rel_dir%\WoWTTS

@REM build screen reader wrapper
PyInstaller -F wowtts.py
IF %ERRORLEVEL% NEQ 0 (
    exit /b %ERRORLEVEL%
)

@REM build wow screen reader
cd libserpix_rs
cargo build --release --bin wow
IF %ERRORLEVEL% NEQ 0 (
    exit /b %ERRORLEVEL%
)
cd ..

@REM build release package
copy dist\wowtts.exe %rel_dir%\wowtts.exe
xcopy /E /H /C /I /Y WoWTTS %rel_dir%\WoWTTS
xcopy /E /I /Y LibSerpix\LibSerpix %rel_dir%\WoWTTS\Libs\LibSerpix
copy libserpix_rs\target\release\wow.exe %rel_dir%\bin\parser.exe

powershell -Command "Add-Type -A 'System.IO.Compression.FileSystem'; [System.IO.Compression.ZipFile]::CreateFromDirectory('%rel_dir%', '%zipFile%')"
