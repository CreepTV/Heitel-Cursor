# Heitel Cursors Anwendung

## Beschreibung

Die Heitel Cursors Anwendung ist ein Python-basiertes Programm, das es Benutzern ermöglicht, benutzerdefinierte Cursor und Soundeinstellungen auf ihrem Windows-System zu verwalten. Die Anwendung bietet eine grafische Benutzeroberfläche (GUI) mit verschiedenen Funktionen, darunter das Setzen eines benutzerdefinierten Cursors, das Zurücksetzen auf den Standard-Cursor und das Anpassen der Lautstärke für Soundeffekte.

## Hauptfunktionen

### Benutzerdefinierter Cursor

- Die Anwendung lädt einen benutzerdefinierten Cursor von einer angegebenen URL herunter und ermöglicht es dem Benutzer, diesen Cursor auf seinem System zu setzen.
- Der Benutzer kann den benutzerdefinierten Cursor mit einem Klick auf die Schaltfläche "Heitel Cursor setzen" aktivieren.
- Eine Benachrichtigung wird angezeigt, um den Benutzer über den Erfolg oder Misserfolg des Vorgangs zu informieren.

### Standard-Cursor wiederherstellen

- Der Benutzer kann den Standard-Cursor seines Systems wiederherstellen, indem er auf die Schaltfläche "Standard-Cursor wiederherstellen" klickt.
- Eine Benachrichtigung wird angezeigt, um den Benutzer über den Erfolg des Vorgangs zu informieren.

### Soundeinstellungen

- Die Anwendung bietet eine Lautstärkeregelung für Soundeffekte, die bei bestimmten Aktionen abgespielt werden.
- Der Benutzer kann die Lautstärke über einen Schieberegler anpassen, und die aktuelle Lautstärke wird in Prozent angezeigt.

### Benachrichtigungen

- Die Anwendung zeigt Benachrichtigungen an, um den Benutzer über verschiedene Aktionen und deren Ergebnisse zu informieren.
- Benachrichtigungen enthalten ein Bild und Text und werden für eine kurze Zeit angezeigt, bevor sie automatisch entfernt werden.

## Technische Details

- **Programmiersprache:** Python
- **Bibliotheken:**
    - `ctypes`, `win32gui`, `win32con`: Für die Verwaltung von Cursors und Systemparametern.
    - `os`, `urllib.request`: Für Dateiverwaltung und Herunterladen von Dateien.
    - `customtkinter`: Für die Erstellung der grafischen Benutzeroberfläche.
    - `PIL (Pillow)`: Für die Bildverarbeitung.
    - `pygame`: Für das Abspielen von Soundeffekten.

## Dateien und URLs

- **Zielpfad für Downloads:** `Documents/HerrHeitel`
- **Heruntergeladene Dateien:**
    - `HeitelCursorNormal.cur`: Benutzerdefinierter Cursor
    - `HeitelCursorsLogo.png`: Logo-Bild
    - `HeitelCursorsWindowIcon.ico`: Fenster-Icon
    - `HeitelHardwareSounde.mp3`: Sounddatei

## Installation und Ausführung

1. Stellen Sie sicher, dass Python und die erforderlichen Bibliotheken installiert sind.
2. Laden Sie die Anwendung herunter und führen Sie das Skript `HeitelCursorV2.py` aus.
3. Die Anwendung lädt die erforderlichen Dateien herunter und startet die grafische Benutzeroberfläche.

**Hinweis:** Diese Anwendung ist für Windows-Systeme konzipiert und nutzt spezifische Windows-APIs, um Cursors und Systemparameter zu verwalten.

## Download

Eine ausführbare Datei (EXE) der Anwendung kann von der [GitHub Releases-Seite](https://github.com/HeitelCursor/Heitel-Cursor-Projekt/releases) heruntergeladen werden.