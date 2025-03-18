import os
import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import io

GITHUB_API = "https://api.github.com/repos/CreepTV/Heitel-Cursors/releases"

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

def select_install_dir():
    return filedialog.askdirectory()

def on_install():
    version = version_combobox.get()
    install_dir = select_install_dir()
    if install_dir:
        install(version, install_dir)

def show_release_selection():
    start_frame.pack_forget()
    release_frame.pack(pady=20, padx=20, fill="both", expand=True)

releases = get_releases()

root = tk.Tk()
root.title("Heitel Cursors Installer")
root.geometry("600x400")

# Startbildschirm
start_frame = ttk.Frame(root)
start_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Bannerbild von einem Link laden
banner_image_url = "https://example.com/path/to/banner/image.png"  # URL zum Bannerbild
try:
    banner_image_response = requests.get(banner_image_url, stream=True)
    banner_image_response.raise_for_status()
    banner_image_data = banner_image_response.content
    banner_image = Image.open(io.BytesIO(banner_image_data))
    banner_photo = ImageTk.PhotoImage(banner_image)
    banner_label = ttk.Label(start_frame, image=banner_photo)
    banner_label.pack(pady=10)
except Exception as e:
    banner_label = ttk.Label(start_frame, text="Banner Bild nicht gefunden", font=("Arial", 18))
    banner_label.pack(pady=10)

welcome_label = ttk.Label(start_frame, text="Willkommen zum Heitel Cursors Installer", font=("Arial", 18))
welcome_label.pack(pady=10)

description_label = ttk.Label(start_frame, text="Dieser Installer hilft Ihnen, die gewünschte Version von Heitel Cursors herunterzuladen und zu installieren.", wraplength=500)
description_label.pack(pady=10)

next_button = ttk.Button(start_frame, text="Weiter", command=show_release_selection)
next_button.pack(pady=10)

# Release-Auswahlseite
release_frame = ttk.Frame(root)

ttk.Label(release_frame, text="Wählen Sie die Version, die Sie installieren möchten:", font=("Arial", 14)).pack(pady=10)

version_combobox = ttk.Combobox(release_frame, values=["Neueste Version"] + releases)
version_combobox.current(0)
version_combobox.pack(pady=10)

install_button = ttk.Button(release_frame, text="Installieren", command=on_install)
install_button.pack(pady=10)

root.mainloop()