@echo off
REM Botao de panico: encerra o Annoying Ads mesmo que o ESC falhe.
cd /d "%~dp0"

REM Executavel (nome de imagem exclusivo — seguro matar por nome).
taskkill /F /IM annoying-popups.exe >nul 2>&1

REM Execucao via fonte: mata so o pythonw cuja linha de comando cita o script
REM (evita derrubar outros pythonw nao relacionados).
powershell -NoProfile -Command ^
  "Get-CimInstance Win32_Process -Filter \"Name='pythonw.exe' OR Name='python.exe'\" | Where-Object { $_.CommandLine -like '*annoying_popups*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" >nul 2>&1

echo Pronto: pop-ups encerrados (se algum estava rodando).
