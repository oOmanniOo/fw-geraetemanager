# FW-Gerätemanager

Ein modernes Django-basiertes Webanwendungssystem zur Verwaltung von Feuerwehrgeräten, Fahrzeugen und deren Prüfungen.

## 🚒 Projektübersicht

Der FW-Gerätemanager ist eine professionelle Lösung für Feuerwehren und Rettungsdienste, um ihre Ausrüstung, Fahrzeuge und regelmäßigen Prüfungen effizient zu verwalten. Das System bietet eine intuitive Benutzeroberfläche und umfassende Funktionalitäten für die tägliche Arbeit.

## ✨ Hauptfunktionen

### 🔧 Geräteverwaltung
- **Gerätekategorien**: Strukturierte Einordnung von Ausrüstung
- **Statusverfolgung**: Überwachung des aktuellen Zustands jedes Geräts
- **Identifikation**: Eindeutige Kennzeichnung durch Seriennummern und Barcodes
- **Bemerkungen**: Detaillierte Notizen zu jedem Gerät

### 🚗 Fahrzeugverwaltung
- **Fahrzeugdaten**: Kennzeichen, Funkrufname, Standort
- **Geräteräume**: Logische Gruppierung von Ausrüstung pro Fahrzeug
- **Aktivitätsstatus**: Überwachung der Einsatzbereitschaft

### 📋 Prüfungssystem
- **Checklisten**: Strukturierte Prüfungsabläufe
- **Prüfungsarten**: Verschiedene Kategorien von Inspektionen
- **Ergebnisprotokollierung**: Dokumentation von Prüfungsergebnissen
- **PDF-Export**: Professionelle Berichte zum Ausdrucken
- **Bemerkungen**: Detaillierte Notizen zu Prüfungsergebnissen

## 🛠️ Technische Details

### Technologie-Stack
- **Backend**: Django 5.2.5 (Python)
- **Datenbank**: SQLite3 (entwicklungsfreundlich)
- **Frontend**: Bootstrap 5, moderne CSS-Grid-Layouts
- **PDF-Generierung**: WeasyPrint für professionelle Ausgabe
- **Deployment**: Django-environ für Umgebungsvariablen

### Projektstruktur
```
fw-geraetemanager/
├── fwmanager/          # Hauptprojekt-Konfiguration
├── geraete/            # Geräteverwaltung App
├── fahrzeuge/          # Fahrzeugverwaltung App
├── pruefungen/         # Prüfungssystem App
├── static/             # CSS, JavaScript, Bilder
├── templates/          # Basis-Templates
├── manage.py           # Django-Management
└── requirements.txt    # Python-Abhängigkeiten
```

## 🚀 Installation

### Voraussetzungen
- Python 3.8+
- pip (Python Package Manager)
- Git

### Schritt-für-Schritt Anleitung

1. **Repository klonen**
   ```bash
   git clone https://github.com/yourusername/fw-geraetemanager.git
   cd fw-geraetemanager
   ```

2. **Virtuelle Umgebung erstellen**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **Umgebungsvariablen konfigurieren**
   ```bash
   # .env Datei erstellen
   cp .env.example .env
   
   # Folgende Variablen anpassen:
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Datenbank initialisieren**
   ```bash
   python manage.py migrate
   ```

6. **Superuser erstellen**
   ```bash
   python manage.py createsuperuser
   ```

7. **Entwicklungsserver starten**
   ```bash
   python manage.py runserver
   ```

8. **Anwendung öffnen**
   Öffne deinen Browser und gehe zu: http://127.0.0.1:8000

## 📖 Verwendung

### Erste Schritte
1. **Admin-Bereich**: http://127.0.0.1:8000/admin/
2. **Gerätekategorien** und **Status** anlegen
3. **Fahrzeuge** mit Geräteräumen erstellen
4. **Geräte** den entsprechenden Räumen zuordnen
5. **Prüfungsarten** und **Checklisten** definieren

### Workflow-Beispiel
1. Neues Gerät in der Geräteverwaltung anlegen
2. Gerät einem Geräteraum in einem Fahrzeug zuordnen
3. Prüfung für das Gerät starten
4. Checkliste durchgehen und Ergebnisse dokumentieren
5. Prüfungsbericht als PDF exportieren

## 🔧 Konfiguration

### Umgebungsvariablen (.env)
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Produktions-Einstellungen
- `DEBUG=False` setzen
- Sichere `SECRET_KEY` verwenden
- `ALLOWED_HOSTS` auf tatsächliche Domains beschränken
- Datenbank auf PostgreSQL oder MySQL umstellen

## 📊 Datenbank-Schema

### Hauptmodelle
- **Gerät**: Zentrale Einheit mit Kategorie, Status und Zuordnung
- **Fahrzeug**: Träger für Geräteräume
- **Geräteraum**: Logische Gruppierung von Geräten
- **Prüfung**: Dokumentation von Inspektionen
- **Checklistenpunkt**: Einzelne Prüfungsaspekte
- **Antwort**: Ergebnis eines Prüfungspunkts


### Produktions-Setup
1. **Webserver**: Nginx oder Apache
2. **WSGI**: Gunicorn oder uWSGI
3. **Datenbank**: PostgreSQL (empfohlen)
4. **Statische Dateien**: CDN oder lokaler Server
5. **SSL**: Let's Encrypt Zertifikat


## 🤝 Beitragen

Wir freuen uns über Beiträge! So kannst du helfen:

1. **Fork** das Repository
2. **Feature Branch** erstellen (`git checkout -b feature/AmazingFeature`)
3. **Änderungen committen** (`git commit -m 'Add some AmazingFeature'`)
4. **Branch pushen** (`git push origin feature/AmazingFeature`)
5. **Pull Request** erstellen

### Coding Standards
- PEP 8 für Python-Code
- Django Best Practices
- Aussagekräftige Commit-Messages
- Tests für neue Features

## 📝 Changelog

### Version 1.0.0
- Grundlegende Geräteverwaltung
- Fahrzeugverwaltung mit Geräteräumen
- Prüfungssystem mit Checklisten
- PDF-Export-Funktionalität
- Moderne Bootstrap-UI

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.


## 📞 Support

Bei Fragen oder Problemen:

- **Issues**: [GitHub Issues](https://github.com/yourusername/fw-geraetemanager/issues)

## 🙏 Danksagungen

- Django Community für das großartige Framework
- Bootstrap Team für die UI-Komponenten
- WeasyPrint für die PDF-Generierung
- Alle Mitwirkenden und Tester

---

**Entwickelt mit ❤️ für die Feuerwehr-Community**

*Letzte Aktualisierung: August 2025*
