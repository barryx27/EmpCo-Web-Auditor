# EmpCo Web Auditor (v1.0.0) 🚀

Der **EmpCo Web Auditor** ist ein universelles, Open-Source Desktop-Tool zur automatisierten Überprüfung von Website-Inhalten auf Konformität mit modernen Green-Claims- und Umwelt-Richtlinien (Empirical Content / Greenwashing-Prävention). Der Crawler durchsucht jede beliebige, vom Nutzer definierte Domain nach sensiblen, unüberprüften oder potenziell wettbewerbswidrigen Phrasen.

---

## 📦 Schnelleinstieg für Anwender (Download & Start)

Für die Nutzung des Tools müssen Sie **keine** Programmierumgebungen installiert haben. Es steht eine fertige Windows-Anwendung zur Verfügung.

1. Klicken Sie oben rechts auf dieser GitHub-Seite auf den Reiter **"Releases"** (oder nutzen Sie den Direktlink `/releases`).
2. Laden Sie sich unter dem neuesten Release im Bereich *Assets* die Datei **`EmpCo_Web_Auditor.exe`** herunter.
3. Starten Sie das Programm per **Doppelklick**.

> 💡 **Hinweis zum ersten Start (Windows SmartScreen):**
> Da es sich um eine unabhängig kompilierte und selbstsignierte Open-Source-Anwendung handelt, zeigt Windows beim allerersten Start eventuell einen blauen Warnbildschirm (*"Der Computer wurde durch Windows geschützt"*). Klicken Sie einfach auf **„Weitere Informationen“** und im Anschluss auf **„Trotzdem ausführen“**. Bei allen zukünftigen Starts öffnet sich die App sofort.

---

## 🎯 Funktionen & Bedienungsanleitung

1. **Zu scannende Start-URL:** Tragen Sie hier die vollständige Webadresse ein. Sie können entweder eine Hauptdomain (z. B. `https://example.com`) oder einen spezifischen Unterpfad eingeben (z. B. `https://example.com/subpage`). Wenn ein Unterpfad angegeben wird, beschränkt sich der Crawler strikt auf diese Struktur und alles, was tiefenmäßig darunter liegt.
2. **Maximale Anzahl Seiten:** Begrenzt die Crawl-Tiefe (Standard: 500 Seiten).
3. **Flexible Pfad-Filter:** Nutzen Sie das freie Textfeld, um unerwünschte Verzeichnisstrukturen oder Begriffe vom Scan auszuschließen. Trennen Sie mehrere Begriffe einfach durch ein Komma (z. B. `/news/, /produktdatenbank, /shop, .pdf`). Sobald einer dieser Begriffe in einer gefundenen URL auftaucht, wird diese komplett übersprungen.
4. **Automatischer Excel-Bericht:** Nach Abschluss generiert das Tool eine saubere Analyse-Tabelle mit der URL, der Kategorie, dem exakt gefundenen Begriff sowie dem vollständigen Satzkontext zur schnellen redaktionellen Verifizierung.

---

## 🤖 Transparenz-Hinweis (Vibe-Coding)

Dieses Tool wurde vollständig mittels **Vibe-Coding** (KI-gestützte Entwicklung unter Einsatz moderner Large Language Models wie Gemini/ChatGPT) erstellt. Struktur, UI-Design und die Algorithmen zur Pfadanalyse wurden durch iterative KI-Prompts generiert und verfeinert.

---

## ⚖️ Rechtlicher Ausschluss & Haftungsbegrenzung (Disclaimer)

**WICHTIGER HINWEIS FÜR DIE NUTZUNG:**

* **Keine Rechtsberatung:** Dieses Tool dient ausschließlich der redaktionellen Unterstützung und Orientierung bei der Überprüfung von Website-Inhalten. Die Nutzung dieser Anwendung stellt zu keinem Zeitpunkt eine Rechtsberatung dar und ersetzt keine rechtliche Prüfung durch qualifizierte Juristen oder Fachanwälte.
* **Technisches Fehlerrisiko:** Ein automatisiertes Web-Crawling ist technisch bedingt niemals zu 100 % fehlerfrei oder lückenlos. Seitenaufrufe können durch Server-Timeouts, Bot-Schutz-Mechanismen, JavaScript-Inhalte (AJAX) oder temporäre Netzwerkprobleme unvollständig sein. Es besteht **keine Garantie auf Vollständigkeit** der Berichte (*False Negatives* sind möglich).
* **Haftungsausschluss:** Der Entwickler (Fabian Baradel) übernimmt keinerlei Haftung für die Richtigkeit, Aktualität und Vollständigkeit der durch das Tool ermittelten Daten. Jegliche Haftung für Schäden, Bußgelder, wettbewerbsrechtliche Abmahnungen oder finanzielle Nachteile, die direkt oder indirekt aus der Nutzung des Tools oder dem Vertrauen auf die generierten Berichte entstehen, ist vollständig ausgeschlossen. Die Nutzung erfolgt auf eigene Gefahr.

---
*Entwickelt von Fabian Baradel — 2026*
