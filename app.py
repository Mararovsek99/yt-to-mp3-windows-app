import os
import re
import sys
import json
import queue
import threading
import subprocess
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


APP_TITLE = "YT to MP3"
WINDOW_SIZE = "760x560"
LINKEDIN_URL = "https://www.linkedin.com/in/andrej-marov%C5%A1ek-78b040206/"


LANGUAGES = {
    "English": {
        "window_title": "YT to MP3",
        "title": "YT to MP3",
        "subtitle": "One click. Takes the YouTube link from clipboard and downloads MP3.",
        "download_button": "Download MP3 from Clipboard",
        "folder_label": "Download folder",
        "browse_button": "Browse",
        "open_button": "Open Folder",
        "language_label": "Language",
        "playlist_label": "Allow playlist download",
        "status_ready": "Copy a YouTube link and press the button.",
        "status_downloading": "Downloading...",
        "status_done": "Done. MP3 downloaded successfully.",
        "status_failed": "Download failed.",
        "status_stopped": "Download stopped.",
        "status_preparing": "Preparing download...",
        "tip": "Tip: copy the full YouTube link with Ctrl+C before pressing the button.",
        "credit": "Made by Andrej Marovšek",
        "warn_clipboard_empty": "Clipboard is empty.",
        "warn_invalid_url": "Clipboard does not seem to contain a valid YouTube link.",
        "warn_no_folder": "Please choose a download folder.",
        "err_missing_ytdlp": "Missing file:\n{path}",
        "err_missing_ffmpeg": "Missing file:\n{path}",
        "err_open_folder": "Could not open folder.\n\n{error}",
        "download_finished": "MP3 download completed.",
        "download_failed": "Download failed.\n\n{error}",
        "download_stopped": "The download was stopped.",
        "stop_button": "Stop",
    },
    "Slovenian": {
        "window_title": "YT v MP3",
        "title": "YT v MP3",
        "subtitle": "En klik. Vzame YouTube povezavo iz odložišča in prenese MP3.",
        "download_button": "Prenesi MP3 iz odložišča",
        "folder_label": "Mapa za prenos",
        "browse_button": "Izberi",
        "open_button": "Odpri mapo",
        "language_label": "Jezik",
        "playlist_label": "Dovoli prenos playliste",
        "status_ready": "Kopiraj YouTube povezavo in pritisni gumb.",
        "status_downloading": "Prenašam...",
        "status_done": "Končano. MP3 je uspešno prenesen.",
        "status_failed": "Prenos ni uspel.",
        "status_stopped": "Prenos ustavljen.",
        "status_preparing": "Pripravljam prenos...",
        "tip": "Namig: pred pritiskom na gumb kopiraj celoten YouTube link s Ctrl+C.",
        "credit": "Made by Andrej Marovšek",
        "warn_clipboard_empty": "Odložišče je prazno.",
        "warn_invalid_url": "V odložišču ni veljavne YouTube povezave.",
        "warn_no_folder": "Izberi mapo za prenos.",
        "err_missing_ytdlp": "Manjka datoteka:\n{path}",
        "err_missing_ffmpeg": "Manjka datoteka:\n{path}",
        "err_open_folder": "Mape ni bilo mogoče odpreti.\n\n{error}",
        "download_finished": "Prenos MP3 je končan.",
        "download_failed": "Prenos ni uspel.\n\n{error}",
        "download_stopped": "Prenos je bil ustavljen.",
        "stop_button": "Ustavi",
    },
    "German": {
        "window_title": "YT zu MP3",
        "title": "YT zu MP3",
        "subtitle": "Ein Klick. Nimmt den YouTube-Link aus der Zwischenablage und lädt MP3 herunter.",
        "download_button": "MP3 aus Zwischenablage laden",
        "folder_label": "Download-Ordner",
        "browse_button": "Durchsuchen",
        "open_button": "Ordner öffnen",
        "language_label": "Sprache",
        "playlist_label": "Playlist-Download erlauben",
        "status_ready": "Kopiere einen YouTube-Link und drücke die Taste.",
        "status_downloading": "Download läuft...",
        "status_done": "Fertig. MP3 erfolgreich heruntergeladen.",
        "status_failed": "Download fehlgeschlagen.",
        "status_stopped": "Download gestoppt.",
        "status_preparing": "Download wird vorbereitet...",
        "tip": "Tipp: Kopiere den vollständigen YouTube-Link mit Ctrl+C vor dem Klick.",
        "credit": "Made by Andrej Marovšek",
        "warn_clipboard_empty": "Zwischenablage ist leer.",
        "warn_invalid_url": "Die Zwischenablage enthält keinen gültigen YouTube-Link.",
        "warn_no_folder": "Bitte einen Download-Ordner wählen.",
        "err_missing_ytdlp": "Datei fehlt:\n{path}",
        "err_missing_ffmpeg": "Datei fehlt:\n{path}",
        "err_open_folder": "Ordner konnte nicht geöffnet werden.\n\n{error}",
        "download_finished": "MP3-Download abgeschlossen.",
        "download_failed": "Download fehlgeschlagen.\n\n{error}",
        "download_stopped": "Der Download wurde gestoppt.",
        "stop_button": "Stoppen",
    },
    "Italian": {
        "window_title": "YT in MP3",
        "title": "YT in MP3",
        "subtitle": "Un clic. Prende il link YouTube dagli appunti e scarica l'MP3.",
        "download_button": "Scarica MP3 dagli appunti",
        "folder_label": "Cartella download",
        "browse_button": "Sfoglia",
        "open_button": "Apri cartella",
        "language_label": "Lingua",
        "playlist_label": "Consenti download playlist",
        "status_ready": "Copia un link YouTube e premi il pulsante.",
        "status_downloading": "Download in corso...",
        "status_done": "Fatto. MP3 scaricato con successo.",
        "status_failed": "Download non riuscito.",
        "status_stopped": "Download interrotto.",
        "status_preparing": "Preparazione download...",
        "tip": "Suggerimento: copia il link YouTube completo con Ctrl+C prima di cliccare.",
        "credit": "Made by Andrej Marovšek",
        "warn_clipboard_empty": "Gli appunti sono vuoti.",
        "warn_invalid_url": "Gli appunti non contengono un link YouTube valido.",
        "warn_no_folder": "Scegli una cartella di download.",
        "err_missing_ytdlp": "File mancante:\n{path}",
        "err_missing_ffmpeg": "File mancante:\n{path}",
        "err_open_folder": "Impossibile aprire la cartella.\n\n{error}",
        "download_finished": "Download MP3 completato.",
        "download_failed": "Download non riuscito.\n\n{error}",
        "download_stopped": "Il download è stato interrotto.",
        "stop_button": "Ferma",
    },
    "Spanish": {
        "window_title": "YT a MP3",
        "title": "YT a MP3",
        "subtitle": "Un clic. Toma el enlace de YouTube del portapapeles y descarga MP3.",
        "download_button": "Descargar MP3 del portapapeles",
        "folder_label": "Carpeta de descarga",
        "browse_button": "Elegir",
        "open_button": "Abrir carpeta",
        "language_label": "Idioma",
        "playlist_label": "Permitir descarga de playlist",
        "status_ready": "Copia un enlace de YouTube y pulsa el botón.",
        "status_downloading": "Descargando...",
        "status_done": "Hecho. MP3 descargado correctamente.",
        "status_failed": "La descarga falló.",
        "status_stopped": "Descarga detenida.",
        "status_preparing": "Preparando descarga...",
        "tip": "Consejo: copia el enlace completo de YouTube con Ctrl+C antes de pulsar.",
        "credit": "Made by Andrej Marovšek",
        "warn_clipboard_empty": "El portapapeles está vacío.",
        "warn_invalid_url": "El portapapeles no contiene un enlace válido de YouTube.",
        "warn_no_folder": "Elige una carpeta de descarga.",
        "err_missing_ytdlp": "Falta el archivo:\n{path}",
        "err_missing_ffmpeg": "Falta el archivo:\n{path}",
        "err_open_folder": "No se pudo abrir la carpeta.\n\n{error}",
        "download_finished": "Descarga MP3 completada.",
        "download_failed": "La descarga falló.\n\n{error}",
        "download_stopped": "La descarga fue detenida.",
        "stop_button": "Detener",
    },
    "French": {
        "window_title": "YT en MP3",
        "title": "YT en MP3",
        "subtitle": "Un clic. Prend le lien YouTube du presse-papiers et télécharge le MP3.",
        "download_button": "Télécharger MP3 du presse-papiers",
        "folder_label": "Dossier de téléchargement",
        "browse_button": "Choisir",
        "open_button": "Ouvrir le dossier",
        "language_label": "Langue",
        "playlist_label": "Autoriser le téléchargement de playlist",
        "status_ready": "Copiez un lien YouTube et appuyez sur le bouton.",
        "status_downloading": "Téléchargement...",
        "status_done": "Terminé. MP3 téléchargé avec succès.",
        "status_failed": "Échec du téléchargement.",
        "status_stopped": "Téléchargement arrêté.",
        "status_preparing": "Préparation du téléchargement...",
        "tip": "Astuce : copiez le lien YouTube complet avec Ctrl+C avant de cliquer.",
        "credit": "Made by Andrej Marovšek",
        "warn_clipboard_empty": "Le presse-papiers est vide.",
        "warn_invalid_url": "Le presse-papiers ne contient pas de lien YouTube valide.",
        "warn_no_folder": "Veuillez choisir un dossier de téléchargement.",
        "err_missing_ytdlp": "Fichier manquant :\n{path}",
        "err_missing_ffmpeg": "Fichier manquant :\n{path}",
        "err_open_folder": "Impossible d'ouvrir le dossier.\n\n{error}",
        "download_finished": "Téléchargement MP3 terminé.",
        "download_failed": "Échec du téléchargement.\n\n{error}",
        "download_stopped": "Le téléchargement a été arrêté.",
        "stop_button": "Arrêter",
    },
    "Portuguese": {
        "window_title": "YT para MP3",
        "title": "YT para MP3",
        "subtitle": "Um clique. Pega o link do YouTube da área de transferência e baixa MP3.",
        "download_button": "Baixar MP3 da área de transferência",
        "folder_label": "Pasta de download",
        "browse_button": "Procurar",
        "open_button": "Abrir pasta",
        "language_label": "Idioma",
        "playlist_label": "Permitir download de playlist",
        "status_ready": "Copie um link do YouTube e pressione o botão.",
        "status_downloading": "Baixando...",
        "status_done": "Concluído. MP3 baixado com sucesso.",
        "status_failed": "Falha no download.",
        "status_stopped": "Download parado.",
        "status_preparing": "Preparando download...",
        "tip": "Dica: copie o link completo do YouTube com Ctrl+C antes de clicar.",
        "credit": "Made by Andrej Marovšek",
        "warn_clipboard_empty": "A área de transferência está vazia.",
        "warn_invalid_url": "A área de transferência não contém um link válido do YouTube.",
        "warn_no_folder": "Escolha uma pasta de download.",
        "err_missing_ytdlp": "Arquivo ausente:\n{path}",
        "err_missing_ffmpeg": "Arquivo ausente:\n{path}",
        "err_open_folder": "Não foi possível abrir a pasta.\n\n{error}",
        "download_finished": "Download MP3 concluído.",
        "download_failed": "Falha no download.\n\n{error}",
        "download_stopped": "O download foi parado.",
        "stop_button": "Parar",
    },
    "Dutch": {
        "window_title": "YT naar MP3",
        "title": "YT naar MP3",
        "subtitle": "Eén klik. Pakt de YouTube-link uit het klembord en downloadt MP3.",
        "download_button": "Download MP3 uit klembord",
        "folder_label": "Downloadmap",
        "browse_button": "Bladeren",
        "open_button": "Map openen",
        "language_label": "Taal",
        "playlist_label": "Playlist-download toestaan",
        "status_ready": "Kopieer een YouTube-link en druk op de knop.",
        "status_downloading": "Downloaden...",
        "status_done": "Klaar. MP3 succesvol gedownload.",
        "status_failed": "Download mislukt.",
        "status_stopped": "Download gestopt.",
        "status_preparing": "Download voorbereiden...",
        "tip": "Tip: kopieer de volledige YouTube-link met Ctrl+C voordat je klikt.",
        "credit": "Made by Andrej Marovšek",
        "warn_clipboard_empty": "Klembord is leeg.",
        "warn_invalid_url": "Het klembord bevat geen geldige YouTube-link.",
        "warn_no_folder": "Kies een downloadmap.",
        "err_missing_ytdlp": "Bestand ontbreekt:\n{path}",
        "err_missing_ffmpeg": "Bestand ontbreekt:\n{path}",
        "err_open_folder": "Kon map niet openen.\n\n{error}",
        "download_finished": "MP3-download voltooid.",
        "download_failed": "Download mislukt.\n\n{error}",
        "download_stopped": "De download is gestopt.",
        "stop_button": "Stop",
    },
    "Croatian": {
        "window_title": "YT u MP3",
        "title": "YT u MP3",
        "subtitle": "Jedan klik. Uzima YouTube link iz međuspremnika i preuzima MP3.",
        "download_button": "Preuzmi MP3 iz međuspremnika",
        "folder_label": "Mapa za preuzimanje",
        "browse_button": "Odaberi",
        "open_button": "Otvori mapu",
        "language_label": "Jezik",
        "playlist_label": "Dopusti preuzimanje playliste",
        "status_ready": "Kopiraj YouTube link i pritisni gumb.",
        "status_downloading": "Preuzimanje...",
        "status_done": "Gotovo. MP3 je uspješno preuzet.",
        "status_failed": "Preuzimanje nije uspjelo.",
        "status_stopped": "Preuzimanje zaustavljeno.",
        "status_preparing": "Priprema preuzimanja...",
        "tip": "Savjet: kopiraj cijeli YouTube link s Ctrl+C prije klika.",
        "credit": "Made by Andrej Marovšek",
        "warn_clipboard_empty": "Međuspremnik je prazan.",
        "warn_invalid_url": "U međuspremniku nije valjan YouTube link.",
        "warn_no_folder": "Odaberi mapu za preuzimanje.",
        "err_missing_ytdlp": "Nedostaje datoteka:\n{path}",
        "err_missing_ffmpeg": "Nedostaje datoteka:\n{path}",
        "err_open_folder": "Mapu nije moguće otvoriti.\n\n{error}",
        "download_finished": "MP3 preuzimanje je završeno.",
        "download_failed": "Preuzimanje nije uspjelo.\n\n{error}",
        "download_stopped": "Preuzimanje je zaustavljeno.",
        "stop_button": "Zaustavi",
    },
    "Serbian": {
        "window_title": "YT u MP3",
        "title": "YT u MP3",
        "subtitle": "Jedan klik. Uzima YouTube link iz klipborda i preuzima MP3.",
        "download_button": "Preuzmi MP3 iz klipborda",
        "folder_label": "Folder za preuzimanje",
        "browse_button": "Izaberi",
        "open_button": "Otvori folder",
        "language_label": "Jezik",
        "playlist_label": "Dozvoli preuzimanje playliste",
        "status_ready": "Kopiraj YouTube link i pritisni dugme.",
        "status_downloading": "Preuzimanje...",
        "status_done": "Gotovo. MP3 je uspešno preuzet.",
        "status_failed": "Preuzimanje nije uspelo.",
        "status_stopped": "Preuzimanje zaustavljeno.",
        "status_preparing": "Priprema preuzimanja...",
        "tip": "Savet: kopiraj ceo YouTube link sa Ctrl+C pre klika.",
        "credit": "Made by Andrej Marovšek",
        "warn_clipboard_empty": "Klipbord je prazan.",
        "warn_invalid_url": "U klipbordu nije ispravan YouTube link.",
        "warn_no_folder": "Izaberi folder za preuzimanje.",
        "err_missing_ytdlp": "Nedostaje fajl:\n{path}",
        "err_missing_ffmpeg": "Nedostaje fajl:\n{path}",
        "err_open_folder": "Folder nije moguće otvoriti.\n\n{error}",
        "download_finished": "MP3 preuzimanje je završeno.",
        "download_failed": "Preuzimanje nije uspelo.\n\n{error}",
        "download_stopped": "Preuzimanje je zaustavljeno.",
        "stop_button": "Zaustavi",
    },
}


def resource_path(relative_path: str) -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class YTToMP3App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.current_language = "English"
        self.texts = LANGUAGES[self.current_language]

        self.root.title(self.texts["window_title"])
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(720, 520)
        self.root.configure(bg="#f5f7fb")

        self.download_folder = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.status_text = tk.StringVar(value=self.texts["status_ready"])
        self.language_var = tk.StringVar(value=self.current_language)
        self.allow_playlist_var = tk.BooleanVar(value=False)
        self.progress_var = tk.DoubleVar(value=0.0)

        self.is_downloading = False
        self.stop_requested = False
        self.current_process: subprocess.Popen | None = None
        self.ui_queue: queue.Queue[tuple[str, str]] = queue.Queue()

        self.setup_styles()
        self.build_ui()
        self.root.after(100, self.process_ui_queue)

    def setup_styles(self) -> None:
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Main.TFrame", background="#f5f7fb")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure(
            "Title.TLabel",
            background="#ffffff",
            foreground="#111827",
            font=("Segoe UI", 22, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#ffffff",
            foreground="#6b7280",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Info.TLabel",
            background="#ffffff",
            foreground="#374151",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Status.TLabel",
            background="#ffffff",
            foreground="#2563eb",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "Section.TLabel",
            background="#ffffff",
            foreground="#111827",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure("Modern.TButton", font=("Segoe UI", 10, "bold"), padding=(16, 10))
        style.configure("Big.TButton", font=("Segoe UI", 14, "bold"), padding=(24, 18))
        style.configure(
            "Switch.TCheckbutton",
            background="#ffffff",
            foreground="#111827",
            font=("Segoe UI", 10),
        )

    def build_ui(self) -> None:
        outer = ttk.Frame(self.root, style="Main.TFrame", padding=24)
        outer.pack(fill="both", expand=True)

        card = ttk.Frame(outer, style="Card.TFrame", padding=28)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.93, relheight=0.92)

        top_row = ttk.Frame(card, style="Card.TFrame")
        top_row.pack(fill="x", pady=(0, 12))

        self.language_label = ttk.Label(top_row, text=self.texts["language_label"], style="Section.TLabel")
        self.language_label.pack(side="left")

        self.language_combo = ttk.Combobox(
            top_row,
            values=list(LANGUAGES.keys()),
            textvariable=self.language_var,
            state="readonly",
            width=16,
        )
        self.language_combo.pack(side="right")
        self.language_combo.bind("<<ComboboxSelected>>", self.on_language_change)

        self.title_label = ttk.Label(card, text=self.texts["title"], style="Title.TLabel")
        self.title_label.pack(pady=(0, 6))

        self.subtitle_label = ttk.Label(card, text=self.texts["subtitle"], style="Subtitle.TLabel")
        self.subtitle_label.pack(pady=(0, 22))

        self.download_button = ttk.Button(
            card,
            text=self.texts["download_button"],
            style="Big.TButton",
            command=self.on_download_click,
        )
        self.download_button.pack(pady=(0, 14), ipadx=6, ipady=2)

        self.stop_button = ttk.Button(
            card,
            text=self.texts["stop_button"],
            style="Modern.TButton",
            command=self.stop_download,
        )
        self.stop_button.pack(pady=(0, 14))
        self.stop_button.state(["disabled"])

        self.playlist_check = ttk.Checkbutton(
            card,
            text=self.texts["playlist_label"],
            variable=self.allow_playlist_var,
            style="Switch.TCheckbutton",
        )
        self.playlist_check.pack(pady=(0, 14))

        self.status_label = ttk.Label(
            card,
            textvariable=self.status_text,
            style="Status.TLabel",
            anchor="center",
            justify="center",
        )
        self.status_label.pack(pady=(0, 10))

        self.progress = ttk.Progressbar(
            card,
            mode="determinate",
            maximum=100,
            variable=self.progress_var,
        )
        self.progress.pack(fill="x", pady=(0, 6))

        self.progress_percent_label = ttk.Label(card, text="0%", style="Info.TLabel")
        self.progress_percent_label.pack(pady=(0, 18))

        self.folder_title_label = ttk.Label(card, text=self.texts["folder_label"], style="Section.TLabel")
        self.folder_title_label.pack(anchor="w", pady=(0, 8))

        folder_row = ttk.Frame(card, style="Card.TFrame")
        folder_row.pack(fill="x", pady=(0, 10))

        self.folder_entry = tk.Entry(
            folder_row,
            textvariable=self.download_folder,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, ipady=8)

        self.browse_button = ttk.Button(
            folder_row,
            text=self.texts["browse_button"],
            style="Modern.TButton",
            command=self.choose_folder,
        )
        self.browse_button.pack(side="left", padx=(10, 0))

        self.open_button = ttk.Button(
            card,
            text=self.texts["open_button"],
            style="Modern.TButton",
            command=self.open_folder,
        )
        self.open_button.pack(anchor="w", pady=(0, 18))

        self.tip_label = ttk.Label(card, text=self.texts["tip"], style="Info.TLabel")
        self.tip_label.pack(pady=(8, 18))

        self.credit_label = tk.Label(
            card,
            text=self.texts["credit"],
            font=("Segoe UI", 9),
            fg="#2563eb",
            bg="#ffffff",
            cursor="hand2",
        )
        self.credit_label.pack(side="bottom", pady=(10, 0))
        self.credit_label.bind("<Button-1>", lambda e: webbrowser.open(LINKEDIN_URL))

    def on_language_change(self, _event=None) -> None:
        self.current_language = self.language_var.get()
        self.texts = LANGUAGES[self.current_language]
        self.apply_language()

    def apply_language(self) -> None:
        self.root.title(self.texts["window_title"])
        self.title_label.config(text=self.texts["title"])
        self.subtitle_label.config(text=self.texts["subtitle"])
        self.download_button.config(text=self.texts["download_button"])
        self.stop_button.config(text=self.texts["stop_button"])
        self.playlist_check.config(text=self.texts["playlist_label"])
        self.folder_title_label.config(text=self.texts["folder_label"])
        self.browse_button.config(text=self.texts["browse_button"])
        self.open_button.config(text=self.texts["open_button"])
        self.tip_label.config(text=self.texts["tip"])
        self.credit_label.config(text=self.texts["credit"])
        self.language_label.config(text=self.texts["language_label"])

        if not self.is_downloading:
            if self.progress_var.get() >= 100:
                self.status_text.set(self.texts["status_done"])
            elif self.progress_var.get() > 0:
                self.status_text.set(self.texts["status_ready"])
            else:
                self.status_text.set(self.texts["status_ready"])

    def choose_folder(self) -> None:
        selected = filedialog.askdirectory(
            title=self.texts["folder_label"],
            initialdir=self.download_folder.get() or str(Path.home()),
        )
        if selected:
            self.download_folder.set(selected)

    def open_folder(self) -> None:
        folder = self.download_folder.get().strip()
        if not folder:
            messagebox.showwarning(APP_TITLE, self.texts["warn_no_folder"])
            return

        os.makedirs(folder, exist_ok=True)

        try:
            if sys.platform.startswith("win"):
                os.startfile(folder)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
        except Exception as exc:
            messagebox.showerror(APP_TITLE, self.texts["err_open_folder"].format(error=exc))

    def on_download_click(self) -> None:
        if self.is_downloading:
            return

        try:
            clipboard_text = self.root.clipboard_get().strip()
        except tk.TclError:
            messagebox.showwarning(APP_TITLE, self.texts["warn_clipboard_empty"])
            return

        if not clipboard_text:
            messagebox.showwarning(APP_TITLE, self.texts["warn_clipboard_empty"])
            return

        if "youtube.com/" not in clipboard_text and "youtu.be/" not in clipboard_text:
            messagebox.showwarning(APP_TITLE, self.texts["warn_invalid_url"])
            return

        output_folder = self.download_folder.get().strip()
        if not output_folder:
            messagebox.showwarning(APP_TITLE, self.texts["warn_no_folder"])
            return

        os.makedirs(output_folder, exist_ok=True)

        yt_dlp_path = resource_path(os.path.join("bin", "yt-dlp.exe"))
        ffmpeg_path = resource_path(os.path.join("bin", "ffmpeg.exe"))

        if not os.path.exists(yt_dlp_path):
            messagebox.showerror(APP_TITLE, self.texts["err_missing_ytdlp"].format(path=yt_dlp_path))
            return

        if not os.path.exists(ffmpeg_path):
            messagebox.showerror(APP_TITLE, self.texts["err_missing_ffmpeg"].format(path=ffmpeg_path))
            return

        command = [
            yt_dlp_path,
            "--newline",
            "--progress",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--ffmpeg-location",
            os.path.dirname(ffmpeg_path),
            "-o",
            os.path.join(output_folder, "%(title)s.%(ext)s"),
            "--print",
            "after_move:DOWNLOAD_PATH=%(filepath)s",
        ]

        if self.allow_playlist_var.get():
            command.append("--yes-playlist")
        else:
            command.append("--no-playlist")

        command.append(clipboard_text)
        self.start_download(command)

    def start_download(self, command: list[str]) -> None:
        self.is_downloading = True
        self.stop_requested = False
        self.progress_var.set(0)
        self.progress_percent_label.config(text="0%")
        self.status_text.set(self.texts["status_preparing"])
        self.download_button.state(["disabled"])
        self.stop_button.state(["!disabled"])

        thread = threading.Thread(target=self.run_download, args=(command,), daemon=True)
        thread.start()

    def stop_download(self) -> None:
        if not self.is_downloading:
            return

        self.stop_requested = True
        self.status_text.set(self.texts["status_stopped"])

        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
            except Exception:
                pass

    def process_ui_queue(self) -> None:
        while not self.ui_queue.empty():
            action, value = self.ui_queue.get_nowait()

            if action == "progress":
                try:
                    number = float(value)
                except ValueError:
                    number = 0.0
                self.progress_var.set(max(0.0, min(100.0, number)))
                self.progress_percent_label.config(text=f"{int(number)}%")
                if self.is_downloading:
                    self.status_text.set(f'{self.texts["status_downloading"]} {int(number)}%')

            elif action == "status":
                self.status_text.set(value)

            elif action == "done":
                self.finish_success(value)

            elif action == "error":
                self.finish_error(value)

            elif action == "stopped":
                self.finish_stopped()

        self.root.after(100, self.process_ui_queue)

    def parse_progress(self, line: str) -> float | None:
        match = re.search(r"\[download\]\s+(\d+(?:\.\d+)?)%", line)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    def run_download(self, command: list[str]) -> None:
        try:
            self.current_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform.startswith("win") else 0,
            )

            output_lines: list[str] = []
            final_download_path = ""

            if self.current_process.stdout is not None:
                for raw_line in self.current_process.stdout:
                    line = raw_line.strip()
                    if not line:
                        continue

                    output_lines.append(line)

                    if line.startswith("DOWNLOAD_PATH="):
                        final_download_path = line.replace("DOWNLOAD_PATH=", "", 1).strip()
                        continue

                    progress_value = self.parse_progress(line)
                    if progress_value is not None:
                        self.ui_queue.put(("progress", str(progress_value)))
                        continue

                    if "[ExtractAudio]" in line or "[VideoRemuxer]" in line or "[ffmpeg]" in line:
                        self.ui_queue.put(("status", self.texts["status_downloading"]))

            return_code = self.current_process.wait()

            if self.stop_requested:
                self.ui_queue.put(("stopped", ""))
                return

            if return_code == 0:
                self.ui_queue.put(("progress", "100"))
                self.ui_queue.put(("done", final_download_path))
            else:
                error_text = "\n".join(output_lines[-12:]) if output_lines else "Unknown error."
                self.ui_queue.put(("error", error_text))

        except Exception as exc:
            self.ui_queue.put(("error", str(exc)))
        finally:
            self.current_process = None

    def finish_success(self, download_path: str) -> None:
        self.is_downloading = False
        self.download_button.state(["!disabled"])
        self.stop_button.state(["disabled"])
        self.progress_var.set(100)
        self.progress_percent_label.config(text="100%")
        self.status_text.set(self.texts["status_done"])

        if download_path:
            messagebox.showinfo(APP_TITLE, f'{self.texts["download_finished"]}\n\n{download_path}')
        else:
            messagebox.showinfo(APP_TITLE, self.texts["download_finished"])

    def finish_error(self, error_message: str) -> None:
        self.is_downloading = False
        self.download_button.state(["!disabled"])
        self.stop_button.state(["disabled"])
        self.status_text.set(self.texts["status_failed"])
        messagebox.showerror(APP_TITLE, self.texts["download_failed"].format(error=error_message))

    def finish_stopped(self) -> None:
        self.is_downloading = False
        self.download_button.state(["!disabled"])
        self.stop_button.state(["disabled"])
        self.status_text.set(self.texts["status_stopped"])
        messagebox.showinfo(APP_TITLE, self.texts["download_stopped"])


def main() -> None:
    root = tk.Tk()
    app = YTToMP3App(root)
    root.mainloop()


if __name__ == "__main__":
    main()