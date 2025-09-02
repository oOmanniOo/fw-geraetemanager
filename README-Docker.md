# Docker Setup für FW-Gerätemanager

Diese Anleitung beschreibt, wie Sie den FW-Gerätemanager mit Docker Desktop und WSL2 in einer Testumgebung starten können.

## Voraussetzungen

1. **Docker Desktop** installiert und gestartet
2. **WSL2** aktiviert und konfiguriert
3. **Git** (optional, für Versionskontrolle)

## Schnellstart

### 1. Automatisches Setup (Empfohlen)

#### Für Windows (PowerShell):
```powershell
.\scripts\docker-setup.ps1
```

#### Für Linux/WSL (Bash):
```bash
chmod +x scripts/docker-setup.sh
./scripts/docker-setup.sh
```

### 2. Manuelles Setup

#### Schritt 1: Umgebungsvariablen konfigurieren
```bash
cp env.example .env
```

#### Schritt 2: Docker Container starten
```bash
docker-compose up -d
```

#### Schritt 3: Datenbank-Migrationen ausführen
```bash
docker-compose exec web python manage.py migrate
```

#### Schritt 4: Superuser erstellen (optional)
```bash
docker-compose exec web python manage.py createsuperuser
```

## Zugriff auf die Anwendung

- **Hauptanwendung**: http://localhost:8000
- **Admin-Interface**: http://localhost:8000/admin

## Nützliche Docker-Befehle

### Services verwalten
```bash
# Services starten
docker-compose up -d

# Services stoppen
docker-compose down

# Services neu starten
docker-compose restart

# Logs anzeigen
docker-compose logs -f
```

### Django-Management
```bash
# Django Shell öffnen
docker-compose exec web python manage.py shell

# Migrationen erstellen
docker-compose exec web python manage.py makemigrations

# Migrationen ausführen
docker-compose exec web python manage.py migrate

# Statische Dateien sammeln
docker-compose exec web python manage.py collectstatic
```

### Datenbank-Backup/Restore
```bash
# Backup erstellen
docker-compose exec web python manage.py dumpdata > backup.json

# Backup wiederherstellen
docker-compose exec web python manage.py loaddata backup.json
```

## Entwicklungsumgebung

### Code-Änderungen
Da das Projekt als Volume gemountet ist, werden Code-Änderungen automatisch übernommen. Ein Neustart des Containers ist nur bei Änderungen an `requirements.txt` oder dem `Dockerfile` nötig.

### Debugging
```bash
# Container-Logs anzeigen
docker-compose logs -f web

# In den Container einsteigen
docker-compose exec web bash

# Django-Debug-Server direkt starten
docker-compose exec web python manage.py runserver 0.0.0.0:8000
```

## Produktionsumgebung

Für die Produktion verwenden Sie die Produktions-Konfiguration:

```bash
# Produktions-Build
docker-compose -f docker-compose.prod.yml build

# Produktions-Services starten
docker-compose -f docker-compose.prod.yml up -d
```

### Unterschiede zur Entwicklungsumgebung:
- PostgreSQL statt SQLite
- Gunicorn statt Django-Entwicklungsserver
- Optimierte Docker-Images
- Keine Debug-Ausgaben
- Statische Dateien werden gesammelt

## Troubleshooting

### Häufige Probleme

#### Port 8000 bereits belegt
```bash
# Anderen Port verwenden
docker-compose up -d -p 8001:8000
```

#### WSL2 Performance-Probleme
- Stellen Sie sicher, dass WSL2 aktiviert ist
- Konfigurieren Sie Docker Desktop für WSL2-Backend
- Verwenden Sie das Projekt in einem WSL2-Dateisystem

#### Berechtigungsprobleme
```bash
# Docker-Gruppe prüfen
groups $USER

# Bei Bedarf zur Docker-Gruppe hinzufügen
sudo usermod -aG docker $USER
```

#### Datenbank-Probleme
```bash
# Datenbank zurücksetzen
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Logs analysieren
```bash
# Alle Logs anzeigen
docker-compose logs

# Nur Web-Service Logs
docker-compose logs web

# Logs mit Zeitstempel
docker-compose logs -t web
```

## Konfiguration

### Umgebungsvariablen (.env)
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### Docker Compose Override
Die Datei `docker-compose.override.yml` wird automatisch geladen und überschreibt Einstellungen aus `docker-compose.yml`. Sie können hier lokale Anpassungen vornehmen.

## Backup und Wiederherstellung

### Vollständiges Backup
```bash
# Container stoppen
docker-compose down

# Datenbank-Datei sichern
cp db.sqlite3 backup/db_$(date +%Y%m%d_%H%M%S).sqlite3

# Code sichern (falls nicht in Git)
tar -czf backup/code_$(date +%Y%m%d_%H%M%S).tar.gz . --exclude=backup --exclude=.git
```

### Wiederherstellung
```bash
# Datenbank wiederherstellen
cp backup/db_YYYYMMDD_HHMMSS.sqlite3 db.sqlite3

# Container neu starten
docker-compose up -d
```

## Erweiterte Konfiguration

### Redis für Caching
Die Entwicklungsumgebung enthält bereits Redis. Um es zu nutzen:

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
```

### Nginx Reverse Proxy
Für die Produktion können Sie Nginx als Reverse Proxy hinzufügen:

```yaml
# docker-compose.prod.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web
```

## Support

Bei Problemen:
1. Prüfen Sie die Docker-Logs: `docker-compose logs`
2. Stellen Sie sicher, dass Docker Desktop läuft
3. Überprüfen Sie die WSL2-Konfiguration
4. Konsultieren Sie die Django-Dokumentation für spezifische Fehler

