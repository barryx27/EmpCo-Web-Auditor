import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin, urlparse
import time
import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import webbrowser

# --- WINDOWS TASKLEISTEN ICON-FIX (ctypes) ---
if sys.platform == "win32":
    import ctypes
    try:
        myappid = 'brdl.empco.webauditor.v1-0-0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

DONT_PATTERNS = {
    "Allgemeine Umweltaussagen": r"\b(umweltfreundlich|ökologisch|gruen|grüne|grünes|grüner)\b",
    "Klimaneutralität": r"\b(klimaneutral|klimaneutrale|klimaneutrales|co2-neutral|emissionsfrei)\b",
    "Nachhaltigkeit (Produktbezug)": r"\b(nachhaltig|nachhaltige|nachhaltiges|nachhaltiger)\b",
    "Verstärkende/Wertende Begriffe": r"\b(wesentlich|deutlich|maßgeblich|signifikant|besonders)\b",
    "Buzzwords (Beispiel)": r"\b(eco|bio|öko)\b"
}

def get_all_links(url, exclusions, base_domain, target_prefix):
    internal_links = set()
    try:
        r = requests.get(url, timeout=10, headers={'User-Agent': 'EmpCo-Auditor/1.0.0'})
        if r.status_code != 200: return internal_links
        soup = BeautifulSoup(r.text, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            full_url = urljoin(url, a_tag['href']).split('#')[0]
            parsed_full = urlparse(full_url)
            
            # 1. Muss auf derselben Domain liegen
            if base_domain in parsed_full.netloc and not full_url.endswith(('.pdf', '.jpg', '.png', '.jpeg', '.zip')):
                # 2. STRICKTE PFAD-RESTRIKTION: Muss mit dem eingegebenen Pfad beginnen
                if full_url.startswith(target_prefix):
                    url_lower = full_url.lower()
                    # 3. DYNAMISCHE AUSSCHLUSS-PRÜFUNG
                    if not any(x in url_lower for x in exclusions if x):
                        internal_links.add(full_url)
    except:
        pass
    return internal_links

def analyze_text(text, url):
    findings = []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for category, pattern in DONT_PATTERNS.items():
        for sentence in sentences:
            sentence_clean = sentence.strip()
            matches = re.findall(pattern, sentence_clean, re.IGNORECASE)
            if matches:
                unique_matches = list(set([m.lower() for m in matches]))
                findings.append({
                    "URL": url,
                    "Kategorie": category,
                    "Gefundener Begriff": ", ".join(unique_matches),
                    "Gefundener Satz (Kontext)": sentence_clean,
                    "To-Do / Empfehlung": "Prüfen: Ist der Begriff belegt? Wenn nein -> anpassen."
                })
    return findings

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EmpCo Web Auditor")
        self.root.geometry("550x660")
        self.root.resizable(False, False)
        
        self.is_cancelled = False
        self.skript_ordner = os.path.dirname(os.path.abspath(__file__))
        
        # --- ICON LADEN ---
        icon_name = "EmpCo_Crawler.ico"
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, icon_name)
        else:
            icon_path = os.path.join(self.skript_ordner, icon_name)
            
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass
        
        # --- BRANDING / LOGO BEREICH (#1E3A8A) ---
        frame_logo = tk.Frame(root, bg="#1E3A8A", height=60) 
        frame_logo.pack(fill="x", side="top")
        frame_logo.pack_propagate(False)
        
        tk.Label(frame_logo, text="EmpCo", font=("Arial", 20, "bold"), fg="white", bg="#1E3A8A").pack(side="left", padx=20, pady=10)
        tk.Label(frame_logo, text="|  Web Auditor", font=("Arial", 12), fg="#FFFFFF", bg="#1E3A8A").pack(side="left", pady=16)
        
        canvas = tk.Canvas(root, height=2, bg="#333333", bd=0, highlightthickness=0)
        canvas.pack(fill="x")
        
        # Inhalt-Frame
        content_frame = tk.Frame(root)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # URL EINGABE
        tk.Label(content_frame, text="Start-URL / Pfad (z.B. https://example.com/subpage):", font=("Arial", 10, "bold")).pack(pady=(5, 2), anchor="w")
        self.entry_url = tk.Entry(content_frame, font=("Arial", 10))
        self.entry_url.insert(0, "https://example.com")
        self.entry_url.pack(fill="x", pady=2)
        
        # Max Pages Eingabe
        frame_pages = tk.Frame(content_frame)
        frame_pages.pack(pady=5, fill="x")
        tk.Label(frame_pages, text="Maximale Anzahl Seiten:", font=("Arial", 10)).pack(side="left")
        self.entry_pages = tk.Entry(frame_pages, width=10)
        self.entry_pages.insert(0, "500")
        self.entry_pages.pack(side="left", padx=10)
        
        # Speicherort wählen
        tk.Label(content_frame, text="Bericht speichern unter:", font=("Arial", 10, "bold")).pack(pady=(10, 2), anchor="w")
        frame_path = tk.Frame(content_frame)
        frame_path.pack(fill="x", pady=2)
        
        self.entry_path = tk.Entry(frame_path, font=("Arial", 9))
        default_excel = os.path.join(self.skript_ordner, "empco_audit_report.xlsx")
        self.entry_path.insert(0, default_excel)
        self.entry_path.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_browse = tk.Button(frame_path, text="Durchsuchen...", command=self.browse_path, font=("Arial", 9))
        self.btn_browse.pack(side="right")
        
        # DYNAMISCHES AUSSCHLUSS-TEXTFELD
        tk.Label(content_frame, text="Pfade/Begriffe ausschließen (mit Komma trennen):", font=("Arial", 10, "bold")).pack(pady=(15, 2), anchor="w")
        self.entry_exclusions = tk.Entry(content_frame, font=("Arial", 10))
        self.entry_exclusions.insert(0, "/news/, /ratgeber/, /shop")
        self.entry_exclusions.pack(fill="x", pady=2)
        
        # Status Textbox
        tk.Label(content_frame, text="Fortschritt / Status:", font=("Arial", 10, "bold")).pack(pady=(15, 2), anchor="w")
        self.txt_status = tk.Text(content_frame, height=7, width=60, font=("Courier", 9))
        self.txt_status.pack(pady=5, fill="x")
        self.log("Bereit für den Start.")
        
        # Buttons Frame
        frame_buttons = tk.Frame(content_frame)
        frame_buttons.pack(pady=10, fill="x")
        
        self.btn_start = tk.Button(frame_buttons, text="Scan starten", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=self.start_scan_thread, height=2, width=22)
        self.btn_start.pack(side="left", padx=5, expand=True, fill="x")
        
        self.btn_cancel = tk.Button(frame_buttons, text="Abbrechen", font=("Arial", 11, "bold"), bg="#f44336", fg="white", command=self.cancel_scan, height=2, width=22, state="disabled")
        self.btn_cancel.pack(side="right", padx=5, expand=True, fill="x")
        
        # --- FOOTER MIT UPDATE-BUTTON ---
        frame_footer = tk.Frame(root, bg="#f4f4f4", height=32)
        frame_footer.pack(fill="x", side="bottom")
        frame_footer.pack_propagate(False)
        
        lbl_copy = tk.Label(frame_footer, text="Entwickelt von Fabian Baradel", font=("Arial", 8), fg="#666666", bg="#f4f4f4")
        lbl_copy.pack(side="left", padx=15, pady=8)
        
        self.btn_update = tk.Button(frame_footer, text="🔄 Auf Updates prüfen", font=("Arial", 8, "bold"), bg="#e0e0e0", fg="#333333", command=self.open_github_releases, relief="groove", bd=1, padx=5)
        self.btn_update.pack(side="right", padx=15, pady=4)

    def log(self, message):
        self.txt_status.insert(tk.END, message + "\n")
        self.txt_status.see(tk.END)

    def open_github_releases(self):
        # WICHTIG: Ersetze 'DEIN_GITHUB_NAME' durch deinen echten GitHub-Nutzernamen nach dem Erstellen!
        webbrowser.open("https://github.com/DEIN_GITHUB_NAME/EmpCo-Web-Auditor/releases")

    def browse_path(self):
        filepath = filedialog.asksaveasfilename(
            initialdir=self.skript_ordner,
            title="Excel-Bericht speichern unter",
            defaultextension=".xlsx",
            filetypes=[("Excel-Dateien", "*.xlsx"), ("Alle Dateien", "*.*")]
        )
        if filepath:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, filepath)

    def cancel_scan(self):
        self.is_cancelled = True
        self.log("\n[!] Abbruch-Signal gesendet. Warte auf aktuelle Seite...")
        self.btn_cancel.config(state="disabled")

    def set_gui_state(self, state):
        self.entry_url.config(state=state)
        self.entry_pages.config(state=state)
        self.entry_path.config(state=state)
        self.entry_exclusions.config(state=state)
        self.btn_browse.config(state=state)
        self.btn_start.config(state=state)
        self.btn_update.config(state=state)

    def start_scan_thread(self):
        self.is_cancelled = False
        threading.Thread(target=self.run_audit, daemon=True).start()

    def run_audit(self):
        start_url = self.entry_url.get().strip()
        excel_filepath = self.entry_path.get().strip()
        
        if not start_url.startswith(("http://", "https://")):
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige URL mit http:// oder https:// ein!")
            return
            
        if not excel_filepath:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen gültigen Speicherort für den Excel-Bericht aus!")
            return

        parsed_start = urlparse(start_url)
        base_domain = parsed_start.netloc.replace("www.", "")
        target_prefix = start_url

        self.set_gui_state("disabled")
        self.btn_cancel.config(state="normal")
        self.txt_status.delete("1.0", tk.END)
        
        self.log(f"Initialisiere Suchlauf für Domain: {base_domain}...")
        self.log(f"Fokus-Präfix: {target_prefix}")
        
        try:
            max_pages = int(self.entry_pages.get())
        except:
            messagebox.showerror("Fehler", "Bitte eine gültige Zahl für die maximalen Seiten eingeben!")
            self.set_gui_state("normal")
            self.btn_cancel.config(state="disabled")
            return
            
        raw_exclusions = self.entry_exclusions.get().split(",")
        exclusions = [x.strip().lower() for x in raw_exclusions if x.strip()]
        
        if exclusions:
            self.log(f"Aktive Ausschlüsse: {', '.join(exclusions)}\n")
        else:
            self.log("Keine Ausschlüsse definiert.\n")
        
        pages_to_visit = {start_url}
        visited_pages = set()
        all_findings = []
        
        while pages_to_visit and len(visited_pages) < max_pages:
            if self.is_cancelled:
                self.log("\n[-] Scan vom Benutzer abgebrochen.")
                break
                
            current_url = pages_to_visit.pop()
            if current_url in visited_pages: continue
            
            self.log(f"Scanne ({len(visited_pages)+1}/{max_pages}): {current_url}")
            visited_pages.add(current_url)
            
            try:
                r = requests.get(current_url, timeout=10, headers={'User-Agent': 'EmpCo-Auditor/1.0.0'})
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    for script in soup(["script", "style"]): 
                        script.decompose()
                    
                    page_findings = analyze_text(soup.get_text(separator=' '), current_url)
                    all_findings.extend(page_findings)
                    
                    new_links = get_all_links(current_url, exclusions, base_domain, target_prefix)
                    pages_to_visit.update(new_links - visited_pages)
                    time.sleep(0.4)
            except:
                self.log(f"Fehler bei Seite: {current_url}")
        
        if all_findings:
            self.log("\nVerarbeite Daten und erstelle Report...")
            df = pd.DataFrame(all_findings)
            try:
                df.to_excel(excel_filepath, index=False)
                self.log(f"\n--- ERFOLG ---")
                self.log(f"Datei gespeichert unter:\n{excel_filepath}")
                status_msg = "Scan abgeschlossen!" if not self.is_cancelled else "Scan abgebrochen!"
                
                messagebox.showinfo("Fertig", f"{status_msg}\n{len(all_findings)} Fundstellen wurden erfolgreich exportiert.\n\nDie Excel-Datei wird nun automatisch geöffnet.")
                
                try:
                    os.startfile(excel_filepath)
                except Exception as e:
                    self.log(f"Hinweis: Datei konnte nicht automatisch geöffnet werden: {e}")
                    
            except Exception as e:
                messagebox.showerror("Fehler", f"Excel konnte nicht gespeichert werden:\n{e}")
        else:
            self.log("\nKeine Treffer erzielt.")
            messagebox.showinfo("Fertig", "Scan beendet. Keine verdächtigen Begriffe gefunden!")
            
        self.set_gui_state("normal")
        self.btn_cancel.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
