import os
import sys
import threading
import subprocess
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


APP_TITLE = "YT to MP3"
WINDOW_SIZE = "720x460"
LINKEDIN_URL = "https://www.linkedin.com/in/andrej-marov%C5%A1ek-78b040206/"


def resource_path(relative_path: str) -> str:
    """
    Works both in development and in PyInstaller builds.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class YTToMP3App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(680, 420)
        self.root.configure(bg="#f5f7fb")

        self.download_folder = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.status_text = tk.StringVar(value="Copy YouTube link, then press the button.")
        self.is_downloading = False
        self.current_process: subprocess.Popen | None = None

        self.setup_styles()
        self.build_ui()

    def setup_styles(self) -> None:
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Main.TFrame",
            background="#f5f7fb"
        )

        style.configure(
            "Card.TFrame",
            background="#ffffff",
            relief="flat"
        )

        style.configure(
            "Title.TLabel",
            background="#ffffff",
            foreground="#111827",
            font=("Segoe UI", 22, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background="#ffffff",
            foreground="#6b7280",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Info.TLabel",
            background="#ffffff",
            foreground="#374151",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Status.TLabel",
            background="#ffffff",
            foreground="#2563eb",
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "Folder.TLabel",
            background="#ffffff",
            foreground="#111827",
            font=("Segoe UI", 10, "bold")
        )

        style.configure(
            "Modern.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 10)
        )

        style.configure(
            "Big.TButton",
            font=("Segoe UI", 14, "bold"),
            padding=(24, 18)
        )

    def build_ui(self) -> None:
        outer = ttk.Frame(self.root, style="Main.TFrame", padding=24)
        outer.pack(fill="both", expand=True)

        card = ttk.Frame(outer, style="Card.TFrame", padding=28)
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.9)

        title = ttk.Label(card, text="YT to MP3", style="Title.TLabel")
        title.pack(pady=(0, 6))

        subtitle = ttk.Label(
            card,
            text="One click. Takes the YouTube link from clipboard and downloads MP3.",
            style="Subtitle.TLabel"
        )
        subtitle.pack(pady=(0, 28))

        self.download_button = ttk.Button(
            card,
            text="Download MP3 from Clipboard",
            style="Big.TButton",
            command=self.on_download_click
        )
        self.download_button.pack(pady=(0, 18), ipadx=6, ipady=2)

        status_label = ttk.Label(
            card,
            textvariable=self.status_text,
            style="Status.TLabel",
            anchor="center",
            justify="center"
        )
        status_label.pack(pady=(0, 18))

        self.progress = ttk.Progressbar(card, mode="indeterminate")
        self.progress.pack(fill="x", pady=(0, 24))

        folder_title = ttk.Label(card, text="Download folder", style="Folder.TLabel")
        folder_title.pack(anchor="w", pady=(0, 8))

        folder_row = ttk.Frame(card, style="Card.TFrame")
        folder_row.pack(fill="x", pady=(0, 10))

        self.folder_entry = tk.Entry(
            folder_row,
            textvariable=self.download_folder,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, ipady=8)

        browse_btn = ttk.Button(
            folder_row,
            text="Browse",
            style="Modern.TButton",
            command=self.choose_folder
        )
        browse_btn.pack(side="left", padx=(10, 0))

        open_btn = ttk.Button(
            card,
            text="Open Folder",
            style="Modern.TButton",
            command=self.open_folder
        )
        open_btn.pack(anchor="w", pady=(0, 20))

        info = ttk.Label(
            card,
            text="Tip: copy the full YouTube link with Ctrl+C before pressing the button.",
            style="Info.TLabel"
        )
        info.pack(pady=(8, 18))

        credit = tk.Label(
            card,
            text="Made by Andrej Marovšek",
            font=("Segoe UI", 9),
            fg="#2563eb",
            bg="#ffffff",
            cursor="hand2"
        )
        credit.pack(side="bottom", pady=(10, 0))
        credit.bind("<Button-1>", lambda e: webbrowser.open(LINKEDIN_URL))

    def choose_folder(self) -> None:
        selected = filedialog.askdirectory(
            title="Choose download folder",
            initialdir=self.download_folder.get() or str(Path.home())
        )
        if selected:
            self.download_folder.set(selected)

    def open_folder(self) -> None:
        folder = self.download_folder.get().strip()
        if not folder:
            messagebox.showwarning(APP_TITLE, "Please choose a folder first.")
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
            messagebox.showerror(APP_TITLE, f"Could not open folder.\n\n{exc}")

    def on_download_click(self) -> None:
        if self.is_downloading:
            return

        try:
            clipboard_text = self.root.clipboard_get().strip()
        except tk.TclError:
            messagebox.showwarning(APP_TITLE, "Clipboard is empty.")
            return

        if not clipboard_text:
            messagebox.showwarning(APP_TITLE, "Clipboard is empty.")
            return

        if "youtube.com/" not in clipboard_text and "youtu.be/" not in clipboard_text:
            messagebox.showwarning(
                APP_TITLE,
                "Clipboard does not seem to contain a valid YouTube link."
            )
            return

        output_folder = self.download_folder.get().strip()
        if not output_folder:
            messagebox.showwarning(APP_TITLE, "Please choose a download folder.")
            return

        os.makedirs(output_folder, exist_ok=True)

        yt_dlp_path = resource_path(os.path.join("bin", "yt-dlp.exe"))
        ffmpeg_path = resource_path(os.path.join("bin", "ffmpeg.exe"))

        if not os.path.exists(yt_dlp_path):
            messagebox.showerror(APP_TITLE, f"Missing file:\n{yt_dlp_path}")
            return

        if not os.path.exists(ffmpeg_path):
            messagebox.showerror(APP_TITLE, f"Missing file:\n{ffmpeg_path}")
            return

        command = [
            yt_dlp_path,
            "--extract-audio",
            "--audio-format", "mp3",
            "--ffmpeg-location", os.path.dirname(ffmpeg_path),
            "-o", os.path.join(output_folder, "%(title)s.%(ext)s"),
            clipboard_text
        ]

        self.start_download(command)

    def start_download(self, command: list[str]) -> None:
        self.is_downloading = True
        self.download_button.state(["disabled"])
        self.progress.start(10)
        self.status_text.set("Downloading MP3...")

        thread = threading.Thread(target=self.run_download, args=(command,), daemon=True)
        thread.start()

    def run_download(self, command: list[str]) -> None:
        try:
            self.current_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

            output_lines = []

            if self.current_process.stdout is not None:
                for line in self.current_process.stdout:
                    clean_line = line.strip()
                    if clean_line:
                        output_lines.append(clean_line)

            return_code = self.current_process.wait()

            if return_code == 0:
                self.root.after(0, self.on_download_success)
            else:
                error_text = "\n".join(output_lines[-12:]) if output_lines else "Unknown error."
                self.root.after(0, lambda: self.on_download_error(error_text))

        except Exception as exc:
            self.root.after(0, lambda: self.on_download_error(str(exc)))
        finally:
            self.current_process = None

    def on_download_success(self) -> None:
        self.is_downloading = False
        self.download_button.state(["!disabled"])
        self.progress.stop()
        self.status_text.set("Done. MP3 downloaded successfully.")
        messagebox.showinfo(APP_TITLE, "MP3 download completed.")

    def on_download_error(self, error_message: str) -> None:
        self.is_downloading = False
        self.download_button.state(["!disabled"])
        self.progress.stop()
        self.status_text.set("Download failed.")
        messagebox.showerror(APP_TITLE, f"Download failed.\n\n{error_message}")


def main() -> None:
    root = tk.Tk()
    app = YTToMP3App(root)
    root.mainloop()


if __name__ == "__main__":
    main()