# Feuerwehr Gerätemanager

Ein Django-basiertes Webanwendungssystem zur Verwaltung von Feuerwehrgeräten, Fahrzeugen und deren Prüfungen.

## 🚒 Projektübersicht

Der Feuerwehr Gerätemanager ist eine Lösung für Feuerwehren, um ihre Ausrüstung, Fahrzeuge und regelmäßigen Prüfungen effizient zu verwalten. Das System bietet eine intuitive Benutzeroberfläche und umfassende Funktionalitäten, um den Überblick über den Zustand und den Standort von Geräten zu behalten und die Prüfungsdokumentation zu vereinfachen.

## ✨ Hauptfunktionen

-   **Geräteverwaltung**: Erfassen, Bearbeiten und Filtern von Geräten. Jedes Gerät hat eine Kategorie, einen Status, einen Lagerort (Fahrzeug und Geräteraum) und eine eindeutige Kennzeichnung.
-   **Fahrzeugverwaltung**: Anlegen und Verwalten von Fahrzeugen und deren Geräteräumen.
-   **Prüfungssystem**:
    -   Verwaltung von anstehenden und durchgeführten Prüfungen.
    -   Dynamische Checklisten basierend auf der Gerätekategorie.
    -   Verfolgung des Prüfungsstatus (bestanden/nicht bestanden).
    -   Export von Prüfprotokollen als PDF.

## 🛠️ Technologie-Stack


-   **Backend**: Django
-   **Datenbank**: PostgreSQL (für Produktion) und SQLite (für lokale Entwicklung)
-   **Frontend**: Bootstrap
-   **PDF-Generierung**: WeasyPrint
-   **Deployment**: Docker, Gunicorn

## 🚀 Installation

Es gibt zwei empfohlene Wege, die Anwendung zu installieren:

### 1. Lokale Entwicklung

Dieser Weg ist ideal für Entwickler, die am Code arbeiten möchten.

**Voraussetzungen:**
- Python 3.8+
- `pip` (Python Package Manager)

**Anleitung:**

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/your-username/fw-geraetemanager.git
    cd fw-geraetemanager
    ```

2.  **Virtuelle Umgebung erstellen und aktivieren:**
    ```bash
    # Erstellen
    python -m venv .venv

    # Windows
    .venv\Scripts\activate

    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Datenbank migrieren:**
    ```bash
    python manage.py migrate
    ```

5.  **Superuser anlegen (für den Admin-Zugang):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Entwicklungsserver starten:**
    ```bash
    python manage.py runserver
    ```
    Die Anwendung ist jetzt unter `http://127.0.0.1:8000` erreichbar.

### 2. Produktion (mit Docker)

Dieser Weg ist für die einfache Bereitstellung einer lauffähigen Anwendung gedacht.

**Voraussetzungen:**
- Docker
- Docker Compose

**Anleitung:**

1.  **`.env`-Datei erstellen:**
    -   Kopieren Sie die `env.example` zu einer neuen Datei namens `.env`.
    -   Passen Sie die Variablen in der `.env`-Datei an, insbesondere `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` und `SECRET_KEY`.

2.  **Anwendung bauen und starten:**
    ```bash
    docker-compose up --build
    ```
    Die Anwendung wird gestartet und ist über den in Ihrer Docker-Konfiguration festgelegten Port erreichbar (standardmäßig Port 80).

## 📁 Projektstruktur

```
fw-geraetemanager/
├── fahrzeuge/          # App für die Fahrzeugverwaltung
├── geraete/            # App für die Geräteverwaltung
├── pruefungen/         # App für das Prüfungssystem
├── fwmanager/          # Django-Projektkonfiguration
├── static/             # Statische Dateien (CSS, JS)
├── templates/          # Globale Templates (z.B. base.html)
├── docker-compose.yml  # Docker-Konfiguration
├── Dockerfile          # Docker-Image für die Anwendung
├── manage.py           # Django-Management-Skript
└── requirements.txt    # Python-Abhängigkeiten
```