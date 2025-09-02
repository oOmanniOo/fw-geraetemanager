# Docker Setup Script für FW-Gerätemanager (PowerShell)
Write-Host "🚀 Starte Docker Setup für FW-Gerätemanager..." -ForegroundColor Green

# Prüfe ob Docker installiert ist
try {
    docker --version | Out-Null
    Write-Host "✅ Docker ist installiert" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker ist nicht installiert. Bitte installieren Sie Docker Desktop." -ForegroundColor Red
    exit 1
}

# Prüfe ob Docker Compose installiert ist
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose ist installiert" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose ist nicht installiert." -ForegroundColor Red
    exit 1
}

# Erstelle .env Datei falls nicht vorhanden
if (-not (Test-Path ".env")) {
    Write-Host "📝 Erstelle .env Datei..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    Write-Host "✅ .env Datei erstellt" -ForegroundColor Green
}

# Baue das Docker Image
Write-Host "🔨 Baue Docker Image..." -ForegroundColor Yellow
docker-compose build

# Starte die Services
Write-Host "🚀 Starte Services..." -ForegroundColor Yellow
docker-compose up -d

# Warte kurz bis der Service läuft
Write-Host "⏳ Warte auf Service..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Führe Migrationen aus
Write-Host "🗄️ Führe Datenbank-Migrationen aus..." -ForegroundColor Yellow
docker-compose exec web python manage.py migrate

# Erstelle Superuser falls gewünscht
$createSuperuser = Read-Host "🤔 Möchten Sie einen Superuser erstellen? (y/n)"
if ($createSuperuser -eq "y" -or $createSuperuser -eq "Y") {
    Write-Host "👤 Erstelle Superuser..." -ForegroundColor Yellow
    docker-compose exec web python manage.py createsuperuser
}

Write-Host "✅ Setup abgeschlossen!" -ForegroundColor Green
Write-Host "🌐 Die Anwendung ist verfügbar unter: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📊 Admin-Interface: http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 Nützliche Befehle:" -ForegroundColor Yellow
Write-Host "  - Services stoppen: docker-compose down" -ForegroundColor White
Write-Host "  - Logs anzeigen: docker-compose logs -f" -ForegroundColor White
Write-Host "  - Shell öffnen: docker-compose exec web python manage.py shell" -ForegroundColor White

