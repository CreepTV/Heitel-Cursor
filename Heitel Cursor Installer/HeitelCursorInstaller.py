import os
import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import io
import subprocess

GITHUB_API = "https://api.github.com/repos/CreepTV/Heitel-Cursors/releases"
DEFAULT_INSTALL_DIR = "C:\\Programme"

def get_releases():
    response = requests.get(GITHUB_API)
    response.raise_for_status()
    releases = response.json()
    return [f"{release['tag_name']} - {release['name']}" for release in releases]

def download_file(url, dest):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def install(version, install_dir):
    if version == "Neueste Version":
        response = requests.get(f"{GITHUB_API}/latest")
        response.raise_for_status()
        release = response.json()
    else:
        tag_name = version.split(" - ")[0]
        response = requests.get(f"{GITHUB_API}/tags/{tag_name}")
        response.raise_for_status()
        release = response.json()

    exe_url = next(asset['browser_download_url'] for asset in release['assets'] if asset['name'].endswith('.exe'))
    exe_name = f"HeitelCursor{version}.exe"
    exe_path = os.path.join(install_dir, exe_name)

    download_file(exe_url, exe_path)
    messagebox.showinfo("Installation abgeschlossen", f"Die Anwendung wurde erfolgreich in {install_dir} installiert.")
    
    if messagebox.askyesno("Installation abgeschlossen", "Möchten Sie Heitel Cursor jetzt ausführen?"):
        subprocess.Popen([exe_path])

def select_install_dir():
    def set_install_dir():
        selected_dir = filedialog.askdirectory(initialdir=DEFAULT_INSTALL_DIR)
        if selected_dir:
            install_dir_var.set(selected_dir)

    install_dir_window = tk.Toplevel(root)
    install_dir_window.title("Zielverzeichnis auswählen")
    install_dir_window.geometry("400x200")
    install_dir_window.resizable(False, False)

    ttk.Label(install_dir_window, text="Wählen Sie das Zielverzeichnis für die Installation:", font=("Arial", 12)).pack(pady=20)
    install_dir_var = tk.StringVar(value=DEFAULT_INSTALL_DIR)
    install_dir_combobox = ttk.Combobox(install_dir_window, textvariable=install_dir_var, values=[DEFAULT_INSTALL_DIR], width=50)
    install_dir_combobox.pack(pady=10)
    ttk.Button(install_dir_window, text="Durchsuchen", command=set_install_dir).pack(pady=10)
    ttk.Button(install_dir_window, text="OK", command=install_dir_window.destroy).pack(pady=10)

    install_dir_window.transient(root)
    install_dir_window.grab_set()
    root.wait_window(install_dir_window)

    return install_dir_var.get()

def on_install():
    version = version_combobox.get()
    install_dir = select_install_dir()
    if install_dir:
        if not os.access(install_dir, os.W_OK):
            messagebox.showerror("Fehler", f"Zugriff auf das Verzeichnis {install_dir} verweigert.")
            return
        show_progress()
        root.after(100, lambda: install(version, install_dir))

def show_release_selection():
    start_frame.pack_forget()
    release_frame.pack(pady=20, padx=20, fill="both", expand=True)

def show_start_frame():
    release_frame.pack_forget()
    start_frame.pack(pady=20, padx=20, fill="both", expand=True)

releases = get_releases()

root = tk.Tk()
root.title("Heitel Cursors Installer")
root.geometry("600x400")
root.resizable(False, False)  # Fenstergröße nicht veränderbar

# Startbildschirm
start_frame = ttk.Frame(root)
start_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Bannerbild von einem Link laden
banner_image_url = "https://github.com/CreepTV/Heitel-Cursors/blob/main/Heitel%20Cursor%20Installer/heitelinstallerbanner.jpg?raw=true"  # URL zum Bannerbild
try:
    banner_image_response = requests.get(banner_image_url, stream=True)
    banner_image_response.raise_for_status()
    banner_image_data = banner_image_response.content
    banner_image = Image.open(io.BytesIO(banner_image_data))
    banner_image = banner_image.resize((350, 150))  # Bannerbild verkleinern
    banner_photo = ImageTk.PhotoImage(banner_image)
    banner_label = ttk.Label(start_frame, image=banner_photo)
    banner_label.pack(pady=10)
except Exception as e:
    banner_label = ttk.Label(start_frame, text="Banner Bild nicht gefunden", font=("Arial", 18))
    banner_label.pack(pady=10)

welcome_label = ttk.Label(start_frame, text="Willkommen zum Heitel Cursors Installer", font=("Arial", 18, "bold"))
welcome_label.pack(pady=10)

description_label = ttk.Label(start_frame, text="Dieser Installer hilft Ihnen, die gewünschte Version von Heitel Cursors herunterzuladen und zu installieren.", wraplength=500, font=("Arial", 12))
description_label.pack(pady=10)

# Platzierung des "Weiter"-Buttons am unteren Rand
next_button = ttk.Button(start_frame, text="Weiter", command=show_release_selection)
next_button.pack(side="bottom", pady=10, padx=10)

# Release-Auswahlseite
release_frame = ttk.Frame(root)

ttk.Label(release_frame, text="Wählen Sie die Version, die Sie installieren möchten:", font=("Work-Sans", 14, "bold")).pack(pady=10)
ttk.Label(release_frame, text="Wir empfehlen, immer die neueste Vollversion herunterzuladen.\nBei Beta-Versionen ist die volle Funktionalität nicht gewährleistet.", font=("Arial", 11)).pack(pady=3)

version_combobox = ttk.Combobox(release_frame, values=["Neueste Version"] + releases)
version_combobox.current(0)
version_combobox.pack(pady=10, ipadx=20)  # Dropdown-Menü um 20% breiter machen

install_button = ttk.Button(release_frame, text="Installieren", command=on_install)
install_button.pack(pady=10)

# Hinzufügen des "Zurück"-Buttons
back_button = ttk.Button(release_frame, text="Zurück", command=show_start_frame)
back_button.pack(side="left", pady=10, padx=10)

# Fortschrittsanzeige
progress_frame = ttk.Frame(root)
progress_label = ttk.Label(progress_frame, text="Installation läuft...", font=("Arial", 14, "bold"))
progress_label.pack(pady=10)
progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
progress_bar.pack(pady=10, fill='x', expand=True)

def show_progress():
    release_frame.pack_forget()
    progress_frame.pack(pady=20, padx=20, fill="both", expand=True)
    progress_bar.start()

root.mainloop()