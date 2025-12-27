# Pre-Deployment Verification Script
# Run this to verify everything is ready for Render deployment

Write-Host "🔍 Pre-Deployment Verification" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

$errors = 0
$warnings = 0

# Check 1: Required files exist
Write-Host "1. Checking required files..." -ForegroundColor Yellow
$requiredFiles = @(
    "Dockerfile",
    "docker-compose.yml",
    "nginx.conf",
    "supervisord.conf",
    "requirements.txt",
    "render.yaml",
    "app\api\gateway_service.py",
    "app\services\gateway.py",
    "app\models\gateway_schemas.py",
    "app\core\mappings.py"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MISSING!" -ForegroundColor Red
        $errors++
    }
}

# Check 2: Old files removed
Write-Host "`n2. Checking old files removed..." -ForegroundColor Yellow
$oldFiles = @(
    "app\api\assembly_service.py",
    "app\api\design_service.py",
    "app\api\packaging_service.py",
    "app\api\quality_service.py",
    "app\services\assembly.py",
    "app\services\design.py",
    "app\services\packaging.py",
    "app\services\quality.py"
)

$oldFilesFound = $false
foreach ($file in $oldFiles) {
    if (Test-Path $file) {
        Write-Host "  ⚠ $file still exists (should be removed)" -ForegroundColor Yellow
        $warnings++
        $oldFilesFound = $true
    }
}

if (-not $oldFilesFound) {
    Write-Host "  ✓ All old files removed" -ForegroundColor Green
}

# Check 3: Configuration files
Write-Host "`n3. Checking configuration..." -ForegroundColor Yellow

# Check render.yaml
if (Test-Path "render.yaml") {
    $renderContent = Get-Content "render.yaml" -Raw
    if ($renderContent -match "your-frontend.vercel.app") {
        Write-Host "  ⚠ render.yaml still has placeholder URL" -ForegroundColor Yellow
        Write-Host "    Update ALLOWED_ORIGINS with your real frontend URL" -ForegroundColor Yellow
        $warnings++
    } else {
        Write-Host "  ✓ render.yaml configured" -ForegroundColor Green
    }
}

# Check .env.example
if (Test-Path ".env.example") {
    Write-Host "  ✓ .env.example exists" -ForegroundColor Green
} else {
    Write-Host "  ✗ .env.example missing" -ForegroundColor Red
    $errors++
}

# Check 4: Docker configuration
Write-Host "`n4. Checking Docker configuration..." -ForegroundColor Yellow

if (Test-Path "Dockerfile") {
    $dockerContent = Get-Content "Dockerfile" -Raw
    if ($dockerContent -match "python:3.11-slim") {
        Write-Host "  ✓ Dockerfile has correct base image" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Dockerfile may have incorrect base image" -ForegroundColor Yellow
        $warnings++
    }
}

if (Test-Path "docker-compose.yml") {
    $composeContent = Get-Content "docker-compose.yml" -Raw
    if ($composeContent -match "gateway:") {
        Write-Host "  ✓ docker-compose.yml configured for gateway" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ docker-compose.yml may need updates" -ForegroundColor Yellow
        $warnings++
    }
}

# Check 5: Python files syntax (basic check)
Write-Host "`n5. Checking Python files..." -ForegroundColor Yellow

$pythonFiles = Get-ChildItem -Path "app" -Recurse -Filter "*.py"
$syntaxErrors = 0

foreach ($file in $pythonFiles) {
    # Basic check - look for common issues
    $content = Get-Content $file.FullName -Raw
    if ($content -match "from app.api.(assembly_service|design_service|packaging_service|quality_service)") {
        Write-Host "  ⚠ $($file.Name) imports old services" -ForegroundColor Yellow
        $warnings++
    }
}

Write-Host "  ✓ Python files checked" -ForegroundColor Green

# Check 6: Documentation
Write-Host "`n6. Checking documentation..." -ForegroundColor Yellow

$docFiles = @(
    "README.md",
    "GATEWAY_README.md",
    "DEPLOYMENT.md",
    "QUICK_REFERENCE.md"
)

foreach ($file in $docFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ $file missing" -ForegroundColor Yellow
        $warnings++
    }
}

# Check 7: Git status
Write-Host "`n7. Checking Git status..." -ForegroundColor Yellow

try {
    $gitStatus = git status --porcelain 2>&1
    if ($LASTEXITCODE -eq 0) {
        if ([string]::IsNullOrWhiteSpace($gitStatus)) {
            Write-Host "  ✓ All changes committed" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ Uncommitted changes detected:" -ForegroundColor Yellow
            $gitStatus | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
            $warnings++
        }
    } else {
        Write-Host "  ⚠ Not a git repository or git not installed" -ForegroundColor Yellow
        $warnings++
    }
} catch {
    Write-Host "  ⚠ Could not check git status" -ForegroundColor Yellow
    $warnings++
}

# Summary
Write-Host ""
Write-Host "==============================" -ForegroundColor Cyan
Write-Host "Verification Summary" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host ""

if ($errors -eq 0 -and $warnings -eq 0) {
    Write-Host "✅ ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your codebase is ready for deployment!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Update render.yaml with your frontend URL" -ForegroundColor White
    Write-Host "2. Commit and push to GitHub:" -ForegroundColor White
    Write-Host "   git add ." -ForegroundColor Gray
    Write-Host "   git commit -m 'Ready for deployment'" -ForegroundColor Gray
    Write-Host "   git push origin main" -ForegroundColor Gray
    Write-Host "3. Deploy on Render.com" -ForegroundColor White
    Write-Host ""
} elseif ($errors -eq 0) {
    Write-Host "⚠️  $warnings WARNING(S) FOUND" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "The code will work, but consider addressing warnings above." -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "❌ $errors ERROR(S) FOUND" -ForegroundColor Red
    if ($warnings -gt 0) {
        Write-Host "⚠️  $warnings WARNING(S) FOUND" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Please fix errors before deploying!" -ForegroundColor Red
    Write-Host ""
}

Write-Host "For detailed deployment instructions, see DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host ""
