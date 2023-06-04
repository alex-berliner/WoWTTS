mkdir release
mkdir release\QuestTextSender

@REM build wow screen reader
cd libserpix_rs
cargo build --release --bin wow
IF %ERRORLEVEL% NEQ 0 (
    exit /b %ERRORLEVEL%
)
cd ..

@REM build release package
xcopy /E /H /C /I /Y QuestTextSender release\QuestTextSender
xcopy /E /I /Y LibSerpix\LibSerpix release\QuestTextSender\Libs\LibSerpix
copy libserpix_rs\target\release\wow.exe release\
copy parser.py release\
