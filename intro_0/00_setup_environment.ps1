# K-Food App Data Analysis Project Setup - PowerShell Version
# Windows PowerShell 환경용 설정 스크립트

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "K-Food App Data Analysis Project Setup" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# 프로젝트 디렉토리로 이동
$projectPath = "C:\Users\ASUS\Desktop\DATATON\intro"
Set-Location $projectPath
Write-Host "Working directory: $projectPath" -ForegroundColor Green
Write-Host ""

# Python 버전 확인
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    pause
    exit
}
Write-Host ""

# 가상환경 생성
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to recreate it? (y/n)"
    if ($response -eq "y") {
        Remove-Item -Recurse -Force venv
        python -m venv venv
        Write-Host "✓ Virtual environment recreated" -ForegroundColor Green
    }
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# 가상환경 활성화
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "$projectPath\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# pip 업그레이드
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded" -ForegroundColor Green
Write-Host ""

# 필수 라이브러리 설치
Write-Host "Installing required libraries..." -ForegroundColor Yellow
Write-Host ""

$libraries = @(
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "plotly",
    "pytrends",
    "requests",
    "beautifulsoup4",
    "openpyxl",
    "scikit-learn",
    "jupyter",
    "notebook"
)

foreach ($lib in $libraries) {
    Write-Host "  Installing $lib..." -ForegroundColor Cyan
    pip install $lib --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $lib installed successfully" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to install $lib" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installed packages:" -ForegroundColor Yellow
pip list
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Ensure virtual environment is activated" -ForegroundColor White
Write-Host "     Command: .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "  2. Run data collection:" -ForegroundColor White
Write-Host "     Command: python 01_data_collection.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  3. Run visualization:" -ForegroundColor White
Write-Host "     Command: python 02_data_visualization.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  4. Run main analysis:" -ForegroundColor White
Write-Host "     Command: python 03_main_intro_analysis.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# 가상환경이 활성화되어 있는지 확인
if ($env:VIRTUAL_ENV) {
    Write-Host "Virtual environment is active: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "Note: To activate virtual environment manually, run:" -ForegroundColor Yellow
    Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
