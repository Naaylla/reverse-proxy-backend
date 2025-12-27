# Quick Start Script for API Gateway
# Run this after docker-compose up to test the gateway

Write-Host "API Gateway Test Script" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host ""

# Wait for services to be ready
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test health check
Write-Host "`n1. Testing health check..." -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod -Uri "http://localhost/api/health" -Method Get
    Write-Host "✓ Health check passed: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "✗ Health check failed: $_" -ForegroundColor Red
}

# Test economy data (BTC)
Write-Host "`n2. Testing economy data (BTC)..." -ForegroundColor Cyan
try {
    $body = @{
        economy = @{
            asset = "btc"
        }
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost/api/state" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✓ Economy data received:" -ForegroundColor Green
    Write-Host "  BTC Price: $($response.economy.btc_usd) USD" -ForegroundColor White
} catch {
    Write-Host "✗ Economy test failed: $_" -ForegroundColor Red
}

# Test weather data (Algeria)
Write-Host "`n3. Testing weather data (Algeria)..." -ForegroundColor Cyan
try {
    $body = @{
        weather = @{
            country = "algeria"
        }
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost/api/state" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✓ Weather data received:" -ForegroundColor Green
    Write-Host "  Temperature: $($response.weather.temperature)°C" -ForegroundColor White
    Write-Host "  Wind Speed: $($response.weather.wind_speed) km/h" -ForegroundColor White
} catch {
    Write-Host "✗ Weather test failed: $_" -ForegroundColor Red
}

# Test air quality (Algeria)
Write-Host "`n4. Testing air quality data (Algeria)..." -ForegroundColor Cyan
try {
    $body = @{
        air = @{
            country = "algeria"
        }
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost/api/state" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✓ Air quality data received:" -ForegroundColor Green
    Write-Host "  PM10: $($response.air.pm10) µg/m³" -ForegroundColor White
} catch {
    Write-Host "✗ Air quality test failed: $_" -ForegroundColor Red
}

# Test combined request (all data types)
Write-Host "`n5. Testing combined request (all data)..." -ForegroundColor Cyan
try {
    $body = @{
        economy = @{
            asset = "btc"
        }
        weather = @{
            country = "algeria"
        }
        air = @{
            country = "algeria"
        }
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "http://localhost/api/state" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✓ Combined data received:" -ForegroundColor Green
    Write-Host "  BTC Price: $($response.economy.btc_usd) USD" -ForegroundColor White
    Write-Host "  Temperature: $($response.weather.temperature)°C" -ForegroundColor White
    Write-Host "  Wind Speed: $($response.weather.wind_speed) km/h" -ForegroundColor White
    Write-Host "  PM10: $($response.air.pm10) µg/m³" -ForegroundColor White
} catch {
    Write-Host "✗ Combined test failed: $_" -ForegroundColor Red
}

Write-Host "`n========================" -ForegroundColor Green
Write-Host "Testing complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Try it yourself:" -ForegroundColor Yellow
Write-Host "  POST http://localhost/api/state" -ForegroundColor White
Write-Host ""
