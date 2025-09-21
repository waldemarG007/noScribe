# Regeln für die Zusammenarbeit mit dem KI-Agenten
Dieses Dokument definiert die grundlegenden Regeln, Arbeitsweisen und Standards für die Zusammenarbeit mit einem KI-Agenten in diesem Projekt. Es dient als universelle Vorlage für neue Projekte.
## 1. Allgemeine Prinzipien
- **Kritischer Freund:** Der Agent agiert als "kritischer Freund". Er würdigt gute Ideen, zeigt aber auch konstruktiv potenzielle Herausforderungen, technische Auswirkungen und Alternativen auf.
- **Klarheit bei Unsicherheit:** Wenn der Agent sich bei einer Aussage unsicher ist oder keine verlässlichen Informationen hat, kommuniziert er dies klar (z.B. mit "Ich weiß es nicht") und stellt Rückfragen.
- **Sprache:** Die primäre Kommunikationssprache in diesem Projekt ist Deutsch.
## 2. Projektmanagement mit `Plan.md`
Für das Management von Aufgaben wird eine `Plan.md`-Datei im Hauptverzeichnis des Projekts angelegt und verwendet.
- **Struktur:** Die `Plan.md`-Datei sollte eine Tabelle mit den Spalten `Status`, `ID` und `Aufgabe` enthalten.
- **Projekt-Struktur:** Wenn das Projekt mehrere Unterprojekte oder Module enthält, sollte die `Plan.md`-Datei für jedes Unterprojekt oder Modul eine separate ID haben (z.B. `API: 1`, `API: 2`, `Datenbank: 1`, `Datenbank: 2`). Es soll die Projektstruktur erkennbar sein und im Hautpordner sollen dem entsprechende Struktur und Ordner angelegt werden.
- **Plan vor der Tat:** Bevor mit der Implementierung einer neuen Aufgabe begonnen wird, muss die `Plan.md`-Datei aktualisiert werden.
- **Aufgaben nicht löschen:** Bestehende Aufgaben werden nicht umgeschrieben und nicht gelöscht. Ihr Status wird aktualisiert, um den Fortschritt nachvollziehbar zu halten.
- **Neue Aufgaben hinzufügen:** Neue Aufgaben werden immer am Ende der Liste hinzugefügt.
- **Status-Updates:** Der Status einer Aufgabe wird aktualisiert, um den aktuellen Stand widerzuspiegeln (z.B. `🆕 Neu`, `⏳ In Arbeit`, `✅ Erledigt`).
- **Commit vor der Arbeit:** Änderungen an der `Plan.md` werden committet, *bevor* die eigentliche Arbeit an den darin beschriebenen Aufgaben beginnt.
**Beispiel für `Plan.md`:**
```markdown
| Status | ID | Aufgabe |
|------------- |-----|--------------------------|
|✅ Erledigt | 1 | API-Endpunkt für User erstellen |
|⏳ In Arbeit | 2 | Datenbank-Schema anpassen |
|🆕 Neu | 3 | Test-Coverage erhöhen |
```
## 3. Sicherheit
- **Keine sensiblen Daten im Repository:** Es dürfen unter keinen Umständen sensible Daten wie API-Schlüssel, Passwörter oder persönliche Anmeldeinformationen in das Git-Repository committet werden.
- **Konfigurationsdateien nutzen:** Alle sensiblen Daten werden ausschließlich über eine lokale Konfigurationsdatei (z.B. `.env` oder `config.py`) geladen.
- **`.gitignore` verwenden:** Die lokale Konfigurationsdatei muss in der `.gitignore`-Datei aufgeführt sein, um ein versehentliches Committen zu verhindern.
- **Vorlagen-Datei:** Eine Vorlagen-Datei (z.B. `.env.example`) sollte im Repository vorhanden sein, um die benötigten Variablen zu dokumentieren.
## 4. Code-Qualität und Stil
- **Lesbarkeit:** Der Code sollte sauber, gut strukturiert und verständlich sein. Zu jeder angelegten Datei wird oben eine kurze Zusammenfassung hinzugefügt, was die Datei beinhaltet und die Funktionen erklärt. Dieses soll auch aktualisiert werden, wenn sich die Funktionalität ändert.
- **PEP 8:** Für Python-Projekte ist der PEP 8-Styleguide zu befolgen.
- **Sinnvolle Kommentare:** Komplexe Logik, wichtige Design-Entscheidungen oder unoffensichtliche Code-Abschnitte sollten kommentiert werden. Es sollte darauf geachtet werden, dass die Kommentare aktuell und aufführlich gebung sind, damit andere Entwickler den Code verstehen können.
- **Deskriptive Namen:** Variablen, Funktionen und Klassen erhalten klare und aussagekräftige Namen.
- **Keine temporären Dateien:** Temporäre Test- oder Debug-Dateien (z.B. `test.py`, `temp_*.py`) müssen vor einem Commit gelöscht werden.
- **Code-Review:** Jeder Code-Commit wird vom Agenten überprüft, bevor er in das Repository committet wird.
- **Code-Formatierung:** Der Code wird automatisch formatiert, um eine konsistente Darstellung zu gewährleisten.
- **Code-Tests:** Jeder Code-Commit wird mit Tests überprüft, um sicherzustellen, dass keine Regressionen aufgetreten sind.
- **Code-Refactoring:** Der Agent kann Code-Refactoring vornehmen, um den Code zu verbessern und zu optimieren.
- **Code-Optimierung:** Der Agent kann Code optimieren, um die Performance zu verbessern und Ressourcen effizienter zu nutzen.
- **Code-Modularisierung:** Der Agent kann Code in kleinere Module oder Klassen aufteilen, um die Wartbarkeit und Lesbarkeit zu erhöhen.
- **Code-Komplexität:** Der Agent kann Code-Komplexität reduzieren, um die Lesbarkeit und Wartbarkeit zu verbessern.
- **Code-Konsistenz:** Der Agent kann Code-Konsistenz sicherstellen, um eine einheitliche Code-Sprache im Projekt zu gewährleisten.
- **Projekt-Übersichtlichkeit:** Der Agent kann Ordner anlegen und von der Funktion die gleich Datei in einen Ordner verschieben.
## 5. Abhängigkeitsmanagement
- **Anforderungen definieren:** Alle Projekt-Abhängigkeiten müssen in einer Anforderungsdatei (z.B. `requirements.txt` für Python) deklariert sein. Die Anforderungsdatei sollte regelmäßig aktualisiert werden, um sicherzustellen, dass alle Abhängigkeiten aktuell sind.
- **Virtuelle Umgebung:** Die Entwicklung und Ausführung des Projekts sollte innerhalb einer virtuellen Umgebung stattfinden, um Konflikte zu vermeiden.
## 6. Testen
- **Tests ausführen:** Vor dem Einreichen von Änderungen müssen alle vorhandenen Tests ausgeführt werden, um Regressionen zu vermeiden.
- **Neue Tests schreiben:** Für neue Funktionen sollten nach Möglichkeit auch neue Tests erstellt werden, um die Korrektheit zu gewährleisten.
- **Manuelles Testen:** Falls keine automatisierten Tests vorhanden sind, müssen Änderungen manuell durch Ausführen der relevanten Skripte oder der Hauptanwendung überprüft werden.
## 7. Arbeitsweise und Commits
- **Branches:** Änderungen werden in separaten Feature-Branches entwickelt, nicht direkt im `main`-Branch.
- **Eigenständige Commits:** Der Agent darf abgeschlossene Aufgaben eigenständig committen und hochladen, ohne auf eine explizite Aufforderung zu warten.
## 8. Projektspezifische Anweisungen
*Hier können projektspezifische Details ergänzt werden, die von der allgemeinen Vorlage abweichen oder diese ergänzen.*
- **Beispiel 1:** Der Haupteinstiegspunkt der Anwendung ist `main.py`.
- **Beispiel 2:** Alle Datenmodelle befinden sich im Ordner `src/models`.
