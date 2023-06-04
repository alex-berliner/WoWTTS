mkdir release\bin
mkdir release\QuestTextSender

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
copy dist\wowtts.exe release\wowtts.exe
xcopy /E /H /C /I /Y QuestTextSender release\QuestTextSender
xcopy /E /I /Y LibSerpix\LibSerpix release\QuestTextSender\Libs\LibSerpix
copy libserpix_rs\target\release\wow.exe release\bin\parser.exe
@REM copy parser.py release\
