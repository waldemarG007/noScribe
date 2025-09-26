# noScribe
> ## Spitzentechnologie der KI für die automatische Audiotranskription

## Was ist noScribe?
- Eine KI-basierte Software, die **Interviews** für die qualitative Sozialforschung oder den journalistischen Gebrauch **transkribiert**.
- noScribe ist **kostenlos und Open Source** ([GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html)).
- Es läuft **vollständig lokal** auf Ihrem Computer. Es werden keine Daten ins Internet gesendet. Keine Cloud, keine Sorgen.
- Es kann verschiedene **Sprecher** unterscheiden und versteht etwa 60 Sprachen (mehr oder weniger, siehe unten).
- Es enthält einen **schönen Editor** zum Überprüfen, Verifizieren und Korrigieren des resultierenden Transkripts.
- Es steht auf den Schultern von Giganten: [Whisper von OpenAI](https://github.com/openai/whisper), [faster-whisper von Guillaume Klein](https://github.com/guillaumekln/faster-whisper) und [pyannote von Hervé Bredin](https://github.com/pyannote/pyannote-audio).

</br>

![Main window](img/noScribe_main_window.png)
(Das Transkript stammt aus [diesem Interview](https://www.youtube.com/watch?v=vOwajAbvPzQ&t=2018s), das ich im Mai 2022 mit der russischen Soziologin Natalia Savelyeva geführt habe.)

## Einschränkungen
- noScribe benötigt einen ziemlich aktuellen Computer, sonst dauert die Transkription sehr lange. (Erwägen Sie, es auf einem langsameren Rechner über Nacht laufen zu lassen.)
- Da es anspruchsvolle KI-Modelle verwendet, ist der Download ziemlich groß – etwa 3,7 GB.
- Schlechte Audioqualität führt zu schlechten Transkriptionsergebnissen.
- Keine automatische Transkription ist perfekt, eine manuelle Überarbeitung ist immer notwendig. Nutzen Sie den [enthaltenen Editor](#noscribeedit), um Ihre Transkripte gründlich zu überprüfen. (Siehe auch ["Faktoren, die die Qualität beeinflussen"](#faktoren-die-die-qualit-t-der-transkription-beeinflussen) und ["Bekannte Probleme"](#bekannte-probleme) unten.)
- Wenn Sie mehr wissen möchten und Deutsch verstehen, hat Rebecca Schmidt von der Universität Paderborn eine schöne [Rezension von noScribe](https://sozmethode.hypotheses.org/2315) geschrieben, in der auch die Grenzen diskutiert werden. Auch das deutsche [Computermagazin c't hat noScribe in einer aktuellen Ausgabe empfohlen](https://www.heise.de/select/ct/2025/2/2433207582191637980).

## Warum der Name "noScribe"?
Das [Urban Dictionary](https://www.urbandictionary.com/define.php?term=Scribe) definiert **scribe** als *"eine Person, deren gesamte elende Existenz auf akademischen Schmutz und Schmerz reduziert wurde"*. Ich hoffe, diese Software wird Ihr akademisches Leben ein wenig weniger schmerzhaft und schmutzig machen, daher der Name noScribe :)

## Über mich
**Kai Dröge**, Dr. in Soziologie (mit einem Hintergrund in Informatik), qualitativer Forscher und Dozent, [Hochschule Luzern (Schweiz)](https://www.hslu.ch/de-ch/hochschule-luzern/ueber-uns/personensuche/profile/?pid=823) und [Institut für Sozialforschung, Frankfurt/M. (Deutschland)](https://www.ifs.uni-frankfurt.de/personendetails/kai-droege.html).

## Download und Installation

**Aktuelle Versionsnummer: 0.6.2** (siehe [Änderungsprotokoll](CHANGELOG.md))
> Alle Versionen werden auf SWITCHdrive gehostet, einer sicheren Datenaustauschplattform für Schweizer Hochschulen.

### Windows
- Die **Allzweckversion** für normale PCs ohne NVIDIA-Grafikkarte: [https://drive.switch.ch/index.php/s/HtKDKYRZRNaYBeI?path=%2FWindows%2Fnormal2](https://drive.switch.ch/index.php/s/HtKDKYRZRNaYBeI?path=%2FWindows%2Fnormal2)
- Eine spezielle Version mit **CUDA-Beschleunigung auf NVIDIA-Grafikkarten** mit mindestens 6 GB VRAM: [https://drive.switch.ch/index.php/s/HtKDKYRZRNaYBeI?path=%2FWindows%2Fcuda1](https://drive.switch.ch/index.php/s/HtKDKYRZRNaYBeI?path=%2FWindows%2Fcuda1). Sie müssen auch das [CUDA-Toolkit von hier installieren](https://developer.nvidia.com/cuda-downloads?target_os=Windows) (danach ist ein Neustart erforderlich).
- **Installation**:
    - Starten Sie die heruntergeladene Setupdatei. Dies kann eine Weile dauern, seien Sie geduldig.
    - Wenn Sie eine Warnung erhalten, dass "Windows Ihren PC geschützt hat" und die App von einem "unbekannten Herausgeber" stammt, müssen Sie uns vertrauen und auf "Trotzdem ausführen" klicken.
    - Um eine stille Installation auf einer größeren Gruppe von Computern durchzuführen, starten Sie das Setup mit dem Argument `/S`.

### MacOS
portiert von [gernophil](https://github.com/gernophil) </br>
- **Neuere Macs mit Apple Silicon M1-M4 Prozessoren**
    - Download: [https://drive.switch.ch/index.php/s/HtKDKYRZRNaYBeI?path=%2FmacOS%2Farm64%20(Apple%20Silicon)](https://drive.switch.ch/index.php/s/HtKDKYRZRNaYBeI?path=%2FmacOS%2Farm64%20(Apple%20Silicon))
    - Doppelklicken Sie auf die heruntergeladene DMG-Datei und ziehen Sie dann noScribe und noScribeEdit in den Link zu Ihrem Anwendungsordner (beschriftet mit "drag both here to install").
    - Sie benötigen Apples Rosetta2 Intel-Emulator, da eine Komponente (ffmpeg) noch für Intel-CPUs erstellt wird. Wenn Sie es noch nicht installiert haben, gehen Sie wie folgt vor:
        - Öffnen Sie das Terminal (unter `/Programme/Dienstprogramme/Terminal.app`).
        - Geben Sie `softwareupdate --install-rosetta` oder `softwareupdate --install-rosetta --agree-to-license` ein.
        - Drücken Sie die Eingabetaste und folgen Sie den Anweisungen auf dem Bildschirm.
    - Starten Sie noScribe und/oder noScribeEdit durch einen Doppelklick auf die App in Ihrem Anwendungsordner.
- **Ältere Macs mit Intel-Prozessoren**</br>
   **Hinweis: Version 0.6.2 auf Intel-basierten Macs ist derzeit experimentell und funktioniert möglicherweise nicht vollständig. Bitte helfen Sie uns beim Testen. [Sie können sie hier herunterladen.](https://github.com/kaixxx/noScribe/discussions/143) </br>
    Andernfalls können Sie die stabile Version 0.5 verwenden:**
    - für macOS Sonoma (14) und Sequoia (15): [https://drive.switch.ch/index.php/s/EIVup04qkSHb54j?path=%2FnoScribe%20vers.%200.5%2FmacOS%2Fx86_64%20(Intel)](https://drive.switch.ch/index.php/s/EIVup04qkSHb54j?path=%2FnoScribe%20vers.%200.5%2FmacOS%2Fx86_64%20(Intel))
    - für macOS 11 (Big Sur), 12 (Monterey) und 13 (Ventura): [https://drive.switch.ch/index.php/s/EIVup04qkSHb54j?path=%2FnoScribe%20vers.%200.5%2FmacOS%2Fx86_64_legacy%20(old%20Intel)](https://drive.switch.ch/index.php/s/EIVup04qkSHb54j?path=%2FnoScribe%20vers.%200.5%2FmacOS%2Fx86_64_legacy%20(old%20Intel))
    - Hinweis: Leider können wir das x86_64-Paket derzeit nicht korrekt signieren, sodass Sie eine Warnung erhalten, dass noScribe und noScribeEdit von nicht registrierten Entwicklern stammen. Sie müssen noScribe und noScribeEdit manuell die Ausführung erlauben, wenn Ihr Gatekeeper aktiv ist. Führen Sie die folgenden Schritte aus:
    - Doppelklicken Sie auf die heruntergeladene DMG-Datei.
    - Ziehen Sie noScribe und noScribeEdit in den Link zu Ihrem Anwendungsordner (beschriftet mit "drag both here to install").
    - Starten Sie noScribe durch einen Doppelklick auf die App in Ihrem Anwendungsordner. Sie erhalten eine Fehlermeldung, dass noScribe von einem nicht registrierten Entwickler stammt. Machen Sie dasselbe mit dem noScribe Editor.
    - Gehen Sie zu Einstellungen -> Datenschutz & Sicherheit -> Scrollen Sie nach unten, bis Sie eine Meldung sehen, dass der Start von noScribe verhindert wurde, und klicken Sie auf "Dennoch öffnen". Machen Sie auch hier dasselbe mit dem noScribe Editor.
    - Von nun an sollten beide Programme ohne Probleme starten.

### Linux
portiert von [Eckhard Kadasch](https://github.com/eckhrd) und [Florian Dobener](https://github.com/domna); ausführbare Datei generiert von [gernophil](https://github.com/gernophil).
- **Installation der ausführbaren Datei:**
    - Laden Sie die CUDA- oder CPU-Version von noScribe 0.6.2 für Linux hier herunter: [https://drive.switch.ch/index.php/s/HtKDKYRZRNaYBeI?path=%2FLinux](https://drive.switch.ch/index.php/s/HtKDKYRZRNaYBeI?path=%2FLinux)
    - Entpacken Sie die Datei mit dem Terminalbefehl `tar -xzvf noScribe_0.6.2_cpu_linux_amd64.tar.gz` oder `tar -xzvf noScribe_0.6.2_cuda_linux_amd64.tar.gz`.
    - Führen Sie noScribe über das Terminal aus, indem Sie in den noScribe-Ordner wechseln und `./noScribe` ausführen.
    - Optional: Bearbeiten Sie die Dateien `noScribe.desktop` und `noScribeEdit.desktop` mit einem Texteditor und geben Sie den vollständigen Pfad in den Zeilen ein, die mit `Exce=` und `Icon=` beginnen.

- **Manuelle Installation aus dem Quellcode:**
    Basierend auf [Anweisungen von mael-lenoc](https://github.com/kaixxx/noScribe/discussions/83)
    ```shell
    # Version (muss > 0.6 sein, um die neuesten Korrekturen für Linux zu enthalten!)
    NOS_REL=0.6.1
    wget https://github.com/kaixxx/noScribe/archive/refs/tags/v${NOS_REL}.tar.gz
    tar xvz -f v${NOS_REL}.tar.gz
    cd noScribe-${NOS_REL}/  # von hier an geschieht alles in diesem Verzeichnis

    # Alternative: aktueller main-Branch
    wget -O noScribe-main.zip https://github.com/kaixxx/noScribe/archive/refs/heads/main.zip
    unzip noScribe-main.zip
    cd noScribe-main # von hier an geschieht alles in diesem Verzeichnis

    # noScribeEdit installieren
    rm -rf noScribeEdit/
    git clone https://github.com/kaixxx/noScribeEditor.git noScribeEdit

    # venv
    python3 -m venv .venv
    source .venv/bin/activate  # von hier an geschieht alles im venv

    # Anforderungen
    pip install -r environments/requirements_linux.txt
    pip install -r noScribeEdit/environments/requirements.txt

    # models/precise
    # dies setzt voraus, dass Git Large File Support aktiviert ist: apt install git-lfs
    rm -rf models/precise
    git clone https://huggingface.co/mobiuslabsgmbh/faster-whisper-large-v3-turbo models/precise
    for f in config.json model.bin preprocessor_config.json tokenizer.json vocabulary.json; do wget -O models/fast/$f "https://huggingface.co/mukowaty/faster-whisper-int8/resolve/main/faster-whisper-large-v3-turbo-int8/${f}?download=true"; done

    # ausführen
    python3 ./noScribe.py
    ```

### Alte Versionen:
- [https://drive.switch.ch/index.php/s/EIVup04qkSHb54j](https://drive.switch.ch/index.php/s/EIVup04qkSHb54j)

## Zitation (APA-Stil)
Dröge, K. (2024). noScribe. KI-gestützte Audiotranskription (Version XXX) [Computersoftware]. https://github.com/kaixxx/noScribe

## Verwendung
### Einstellungen
<img align="left" src="img/noScribe_settings.png" width="300">

- **Audiodatei auswählen**: NoScribe unterstützt fast jedes Audio- oder Videoformat.
- **Dateiname für das Transkript auswählen**: Sie können auch den Dateityp wählen: *.html ist der Standard, der auch vom noScribe-Editor unterstützt wird. *.vtt ist ein Video-Untertitelformat und besonders nützlich, wenn Sie Ihr Transkript zur weiteren Annotation in [EXMARaLDA](https://exmaralda.org/) importieren möchten. *.txt exportiert das Transkript als reinen Text.
- **Start** und **Stop** akzeptieren Zeitstempel im Format hh:mm:ss. Verwenden Sie dies, um die Transkription auf einen bestimmten Teil der Aufnahme zu beschränken. Dies ist besonders hilfreich, um Ihre Einstellungen mit einer kleinen Stichprobe zu testen, bevor Sie das gesamte Interview transkribieren, was mehrere Stunden dauern kann. Lassen Sie **Stop** leer, wenn Sie bis zum Ende der Audiodatei transkribieren möchten.
- **Sprache**: Wählen Sie die Sprache Ihres Transkripts, stellen Sie sie auf 'auto' zur automatischen Erkennung ein oder wählen Sie "multilingual", wenn Ihr Audio mehr als eine Sprache enthält (experimentell).
- **Qualität**: 'Precise' (Präzise) ist die empfohlene Einstellung für das genaueste Transkript. Auf langsameren Rechnern können Sie sich für die Option 'fast' (schnell) entscheiden. Dies ist schneller, erfordert aber möglicherweise später mehr manuelle Überarbeitung. Sie können auch [benutzerdefinierte Modelle installieren](https://github.com/kaixxx/noScribe/wiki/Add-custom-Whisper-models-for-transcription), die für bestimmte Sprachen optimiert sind, etc.
- **Pausen markieren**: Wenn aktiviert, werden Teile Ihres Audios ohne Sprachaktivität als Pausen markiert. Pausen werden als runde Klammern mit einem Punkt pro Sekunde darin transkribiert, z. B. '(..)' für eine zweisekündige Pause. Längere Pausen als 10 Sekunden werden als '(XX Sekunden Pause)' oder '(XX Minuten Pause)' ausgeschrieben. Sie haben die Möglichkeit, Pausen von einer Sekunde und mehr ('1sec+'), zwei Sekunden und mehr ('2sec+') oder nur die längeren von drei Sekunden und mehr ('3sec+') zu markieren. Wählen Sie 'none', um diese Funktion vollständig zu deaktivieren.
- **Sprechererkennung**: Diese Funktion verwendet das Pyannote-KI-Modell, um verschiedene Sprecher in Ihrem Audio zu identifizieren und das Transkript entsprechend zu organisieren. Wählen Sie die Anzahl der Sprecher, falls bekannt, oder wählen Sie 'auto'. Die Wahl von 'none' umgeht diesen Schritt vollständig und reduziert die Verarbeitungszeit um etwa die Hälfte. Das resultierende Transkript ist jedoch ein durchgehender Textblock ohne jegliche Hinweise auf Sprecherwechsel.
- **Überlappende Sprache**: Wenn aktiviert, versucht noScribe, Fälle zu markieren, in denen zwei Personen gleichzeitig sprechen. Der überlappende Abschnitt wird mit //doppelten Schrägstrichen// abgegrenzt. (Hinweis: Dies ist eine experimentelle Funktion.)
- **Sprechfehler**: Wenn aktiviert, werden auch häufige Sprechfehler wie Füllwörter ("ähm"), unvollendete Wörter oder Sätze usw. transkribiert.
- **Zeitstempel**: Wenn aktiviert, fügt noScribe Zeitstempel im Format [hh:mm:ss] entweder bei jedem Sprecherwechsel oder alle 60 Sekunden in das Transkript ein. Ich finde diese Zeitstempel etwas ablenkend, daher habe ich sie standardmäßig deaktiviert. Sie können jedoch in bestimmten Kontexten sehr nützlich sein. Auch wenn die Zeitstempel deaktiviert sind, ist es einfach, den Audio-Zeitcode für ein bestimmtes Segment zu bestimmen: Öffnen Sie einfach das Transkript im noScribe Editor, navigieren Sie durch den Text, und der entsprechende Zeitcode wird unten rechts in der App angezeigt.

### Transkriptionsprozess
- Wenn Sie bereit sind, klicken Sie auf die **Start**-Schaltfläche unten links. **Abbrechen** bricht den Vorgang ab.
- Beachten Sie, dass **ein einstündiges Interview bis zu drei Stunden Verarbeitungszeit** in Anspruch nehmen kann und Ihren Rechner stark belastet. Es wird nicht empfohlen, dies im Akkubetrieb zu tun.
- Eine **Fortschrittsanzeige** am unteren Rand der App zeigt an, wie weit Sie im gesamten Prozess sind.
- Das **Hauptfenster** protokolliert Fortschrittsmeldungen und Fehler. Es zeigt auch den Text Ihres Interviews während des letzten Schritts der Transkription an.
- Das Transkript wird alle paar Sekunden unter dem angegebenen Dateinamen automatisch gespeichert.
- Standardmäßig erstellt noScribe eine HTML-Datei. Diese kann in jedem gängigen Texteditor (einschließlich MS Word, LibreOffice) oder QDA-Paket (MAXQDA, ATLAS.ti, QualCoder...) geöffnet werden.
- Bevor Sie jedoch mit dem Transkript arbeiten, sollten Sie es mit dem mitgelieferten Editor überprüfen. Es wird immer einige Fehler geben.

## noScribeEdit
Der mitgelieferte Editor zur Überprüfung des endgültigen Transkripts.

![Das Transkript im noScribe Editor](img/noScribe_Editor.png)

Der noScribe Editor ist eine separate App. Er öffnet sich automatisch, sobald das Transkript fertig ist, kann aber auch unabhängig von noScribe ausgeführt werden. Er enthält einige praktische Funktionen, um Ihr fertiges Transkript auf Fehler zu überprüfen und zu korrigieren:
- Drücken Sie **Strg + Leertaste** (^Leertaste auf dem Mac) oder die **orangefarbene Schaltfläche in der Symbolleiste**, um das Audio zu hören, das Ihrer aktuellen Position im Text entspricht.
- Die **Auswahl des Textes folgt dem Audio, das Sie hören**. Wenn Sie **Änderungen vornehmen** möchten, klicken Sie mit der Maus irgendwo in den Text oder verwenden Sie die Pfeiltasten, um den Cursor zu bewegen. Das Audio stoppt, und Sie können den Text bearbeiten.
- Sie können das **Audio auch anhalten**, indem Sie erneut Strg + Leertaste drücken oder auf die orangefarbene Schaltfläche klicken.
- Wenn Sie das **Audio beschleunigen oder verlangsamen** möchten, ändern Sie das Feld "100%" neben der Schaltfläche "Audio abspielen/pausieren" auf die entsprechende Geschwindigkeit.
- Um die **Sprechernamen zu ändern**, verwenden Sie die Funktion Suchen & Ersetzen, die über das Lupensymbol oder das Menü "Bearbeiten" zugänglich ist.
- Verwenden Sie die Plus- und Minus-Symbole in der Symbolleiste, um **hinein- oder herauszuzoomen**.
- Sie finden die **häufigsten Funktionen eines einfachen Texteditors** sowohl in der Symbolleiste als auch im Menü oben (grundlegende Textformatierung, Ausschneiden, Kopieren & Einfügen, Rückgängig & Wiederholen).
- Ihre typischen **Tastenkombinationen** funktionieren ebenfalls (z. B. Strg+S für Speichern, Strg+F für Suchen & Ersetzen). Sie können alle Tastenkombinationen sehen, wenn Sie das Menü öffnen. Wie bereits erwähnt, ist 'Strg+Leertaste' die Tastenkombination, die Sie am häufigsten verwenden werden, da sie das Audio startet oder pausiert.

Der Quellcode des Editors befindet sich hier: [https://github.com/kaixxx/noScribeEditor](https://github.com/kaixxx/noScribeEditor)

## Faktoren, die die Qualität der Transkription beeinflussen
- Eine **gute Audioaufnahme mit klaren Stimmen und ohne Umgebungsgeräusche** ist entscheidend für eine qualitativ hochwertige Transkription. Ein wenig Mühe in die Qualität der Aufnahme zu investieren, wird Ihnen später viel Zeit bei der manuellen Überarbeitung sparen.
- Whisper (die KI, die noScribe antreibt) versteht etwa 60 verschiedene Sprachen, aber die Qualität der Transkription variiert stark zwischen ihnen. **Spanisch, Italienisch, Englisch, Portugiesisch und Deutsch** werden am besten unterstützt (siehe [hier für weitere Informationen](https://github.com/openai/whisper#available-models-and-languages)).
- Whisper kommt mit **Dialekten** ziemlich gut zurecht (z. B. Schweizerdeutsch), aber das Transkript benötigt möglicherweise mehr manuelle Arbeit bei der Überarbeitung.

## Bekannte Probleme
- Die Whisper-KI kann manchmal in einer **Schleife von sich wiederholendem Text stecken bleiben**, besonders bei längeren Audiodateien. Wenn dies geschieht, versuchen Sie, kürzere Abschnitte zu transkribieren (über die Felder "Start" und "Stop" in noScribe) und sie manuell zusammenzufügen.
- **Mehrsprachiges Audio** wird jetzt unterstützt, ist aber experimentell.
- **Nonverbale Ausdrücke** wie Lachen sind nicht im Transkript enthalten und müssen später im Editor hinzugefügt werden, wenn Sie sie benötigen.
- **Sprecheridentifikation**: Bei einigen Aufnahmen kann die von noScribe verwendete KI die Stimmen bestimmter Sprecher möglicherweise nicht auseinanderhalten, selbst wenn sie für das menschliche Ohr ganz unterschiedlich klingen. Überprüfen Sie die Ergebnisse sorgfältig.
- Die Whisper-KI kann manchmal **halluzinieren**, besonders in stillen Teilen der Aufnahme, wenn sie Hintergrundgeräusche als 'Text' interpretiert (siehe [diese Studie der Cornell University](https://facctconference.org/static/papers24/facct24-111.pdf) für weitere Informationen zu diesem Thema).

## Erweiterte Optionen
- Nachdem die App zum ersten Mal ausgeführt wurde, finden Sie eine Datei namens **config.yml** im Benutzerkonfigurationsverzeichnis (unter Windows: C:\Benutzer\<Benutzername>\AppData\Local\noScribe\noScribe\config.yml; auf dem Mac: "~/Library/Application Support/noscribe/config.yml"). Hier können Sie einige **zusätzliche Einstellungen** ändern, z. B. die Sprache der Benutzeroberfläche.
- Im Benutzerkonfigurationsverzeichnis finden Sie auch einen Ordner namens **log** mit detaillierten Protokolldateien für jedes Transkript (auch für unfertige). Dies kann bei Fehlern hilfreich sein. Beachten Sie jedoch, dass diese Dateien auch den Text Ihrer Transkripte enthalten, der sensible Informationen enthalten könnte.
- Wenn Sie **benutzerdefinierte Whisper-Modelle** mit noScribe verwenden möchten, folgen Sie den [Anweisungen im Wiki](https://github.com/kaixxx/noScribe/wiki/Add-custom-Whisper-models-for-transcription).

## Entwicklung und Beitrag
- Ich habe noScribe in Python 3.12 entwickelt.
- Ich kann die Whisper-Modelle nicht auf GitHub hosten, da sie zu groß sind. Im Ordner `models` befindet sich eine Readme-Datei mit Anweisungen, wie man sie bekommt.
- Ich freue mich über Tests, Fehlerberichte und Pull-Requests (sofern es meine Zeit erlaubt).

### Übersetzungen
- Die Benutzeroberfläche von noScribe wurde bereits in viele Sprachen übersetzt (danke mlynar-czyk).
- Da die meisten Übersetzungen mit ChatGPT erstellt wurden, wird es Probleme geben. Bitte melden Sie alle Fehler, die Sie finden, und machen Sie – wenn möglich – einen Pull-Request mit einer besseren Übersetzung.
- Sie finden die Sprachdateien im Ordner "trans".
- Wenn Sie etwas an den Sprachdateien ändern, achten Sie darauf, die Konventionen der YAML-Sprache zu befolgen.
- Wenn Sie die Sprache der Benutzeroberfläche ändern möchten, müssen Sie den Wert der "locale"-Einstellung in den erweiterten Einstellungen ändern (siehe oben).

## Telegram Bot
Dieses Projekt kann auch als Telegram-Bot zur Transkription von YouTube-Videos betrieben werden. Der Bot wird mit Docker bereitgestellt.

### Den Bot betreiben (Server)
Um den Telegram-Bot auf Ihrem Server zu betreiben, muss Docker installiert sein. Führen Sie dann die folgenden Schritte aus:

1.  **Docker-Image erstellen:**
    Öffnen Sie ein Terminal im Stammverzeichnis des Projekts und führen Sie den folgenden Befehl aus. Dadurch wird das Docker-Image aus `Dockerfile.bot` erstellt und als `noscribe-bot` getaggt.
    ```bash
    docker build -f Dockerfile.bot -t noscribe-bot .
    ```

2.  **Docker-Container ausführen:**
    Sie benötigen einen Bot-Token vom BotFather auf Telegram. Sobald Sie Ihren Token haben, führen Sie den folgenden Befehl aus und ersetzen Sie `"IHR_TELEGRAM_BOT_TOKEN"` durch Ihren tatsächlichen Token.
    ```bash
    docker run -d --name noscribe-bot-container -e TELEGRAM_BOT_TOKEN="IHR_TELEGRAM_BOT_TOKEN" noscribe-bot
    ```
    Dieser Befehl führt den Bot im Hintergrund aus (`-d`). Sie können seine Protokolle jederzeit einsehen, indem Sie `docker logs noscribe-bot-container` ausführen.

Sobald der Container läuft, können Sie mit Ihrem Bot auf Telegram interagieren. Senden Sie ihm einen YouTube-Link, und er wird das Video verarbeiten und Ihnen das Transkript als `.txt`-Datei zurücksenden.

### Bereitstellung mit Portainer
Wenn Sie Portainer auf Ihrem Proxmox-Server verwenden, können Sie den Bot einfach mit der bereitgestellten `docker-compose.yml`-Datei bereitstellen.

1.  **Gehen Sie in Portainer zu "Stacks".**
2.  **Klicken Sie auf "Add stack".**
3.  **Geben Sie dem Stack einen Namen** (z.B. `noscribe-bot`).
4.  **Wählen Sie "Git Repository"** als Build-Methode.
5.  **Geben Sie die URL dieses Repositorys an** und spezifizieren Sie den Branch.
6.  **Setzen Sie den Compose-Pfad** auf `docker-compose.yml`.
7.  **Fügen Sie unter "Environment variables"** eine Variable für Ihren Telegram-Bot-Token hinzu:
    - **Name:** `TELEGRAM_BOT_TOKEN`
    - **Wert:** `ihr-telegram-bot-token-hier-einfügen`
8.  **Klicken Sie auf "Deploy the stack".** Portainer wird nun das Repository abrufen, das Docker-Image erstellen und den Container bereitstellen.

## Andere Software
Wenn Sie an Open-Source-Software für die Analyse qualitativer Daten interessiert sind, schauen Sie sich [QualCoder](https://github.com/ccbogel/QualCoder) und [Taguette](https://www.taguette.org/) an.