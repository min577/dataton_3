# K-Food App Data Analysis - Run All Scripts
# 모든 분석 스크립트를 순차적으로 실행하는 PowerShell 스크립트

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "K-Food App Market Research - Run All" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

$projectPath = "C:\Users\ASUS\Desktop\DATATON\intro"
Set-Location $projectPath

# 가상환경 활성화 확인
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "$projectPath\venv\Scripts\Activate.ps1"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to activate virtual environment" -ForegroundColor Red
        Write-Host "Please run 00_setup_environment.ps1 first" -ForegroundColor Yellow
        pause
        exit
    }
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
    Write-Host ""
}

# 스크립트 실행 함수
function Run-PythonScript {
    param (
        [string]$scriptName,
        [string]$description
    )
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "Running: $scriptName" -ForegroundColor Yellow
    Write-Host "$description" -ForegroundColor White
    Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    $startTime = Get-Date
    
    python $scriptName
    
    if ($LASTEXITCODE -eq 0) {
        $endTime = Get-Date
        $duration = $endTime - $startTime
        Write-Host ""
        Write-Host "✓ $scriptName completed successfully" -ForegroundColor Green
        Write-Host "  Duration: $($duration.TotalSeconds) seconds" -ForegroundColor Gray
    } else {
        Write-Host ""
        Write-Host "✗ $scriptName failed with error code $LASTEXITCODE" -ForegroundColor Red
        $response = Read-Host "Continue with next script? (y/n)"
        if ($response -ne "y") {
            exit
        }
    }
}

# 1. 데이터 수집
Run-PythonScript "01_data_collection.py" "Collecting and generating dataset CSV files"

# 2. 데이터 시각화
Run-PythonScript "02_data_visualization.py" "Creating visualizations and charts"

# 3. 종합 분석
Run-PythonScript "03_main_intro_analysis.py" "Running comprehensive market analysis"

# 완료 메시지
Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host "ALL SCRIPTS COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

# 생성된 파일 목록
Write-Host "Generated Files:" -ForegroundColor Yellow
Write-Host ""

Write-Host "CSV Data Files:" -ForegroundColor Cyan
$csvFiles = Get-ChildItem -Path . -Filter "data_*.csv" | Select-Object Name, Length, LastWriteTime
if ($csvFiles) {
    $csvFiles | Format-Table -AutoSize
} else {
    Write-Host "  No CSV files found" -ForegroundColor Red
}

Write-Host "Visualization Files:" -ForegroundColor Cyan
$vizFiles = Get-ChildItem -Path . -Filter "viz_*.png" | Select-Object Name, Length, LastWriteTime
if ($vizFiles) {
    $vizFiles | Format-Table -AutoSize
} else {
    Write-Host "  No visualization files found" -ForegroundColor Red
}

Write-Host "Report Files:" -ForegroundColor Cyan
if (Test-Path "MARKET_RESEARCH_SUMMARY.txt") {
    $reportFile = Get-Item "MARKET_RESEARCH_SUMMARY.txt"
    Write-Host "  ✓ $($reportFile.Name) ($($reportFile.Length) bytes)" -ForegroundColor Green
} else {
    Write-Host "  No report file found" -ForegroundColor Red
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Analysis complete! Files are ready for presentation." -ForegroundColor White
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# 선택사항: 파일 탐색기로 폴더 열기
$response = Read-Host "Open project folder in File Explorer? (y/n)"
if ($response -eq "y") {
    Start-Process explorer.exe $projectPath
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
