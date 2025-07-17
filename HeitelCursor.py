import ctypes
import win32gui
import win32con
import os
import urllib.request
import customtkinter as ctk
from tkinter import Toplevel, Label, Scale, HORIZONTAL
from customtkinter import CTkImage, CTkSlider, CTkProgressBar  # CTkSlider und CTkProgressBar importieren
from PIL import Image, ImageTk, UnidentifiedImageError
import pygame  # Sound-Abspielfunktion importieren
import threading
import tkinter as tk  # Importiere tkinter explizit
from pynput import mouse  # Import the pynput library for global mouse hooks
import webbrowser  # Für das Öffnen von URLs im Browser
import requests  # Für HTTP-Requests zu myinstants.com
import json  # Für JSON-Parsing
import re  # Für Regex-Operationen
from tkinter import filedialog  # Für Dateidialog

# Zielpfad für den Download
cursor_dir = os.path.join(os.path.expandvars("%USERPROFILE%"), "Documents", "HerrHeitel")
os.makedirs(cursor_dir, exist_ok=True)
cursor_file = os.path.join(cursor_dir, "HeitelCursorNormal.cur")
link_cursor_file = os.path.join(cursor_dir, "HeitelCursorLink.cur")
text_cursor_file = os.path.join(cursor_dir, "HeitelCursorText.cur")
wait_cursor_file = os.path.join(cursor_dir, "HeitelCursorWait.ani")
progress_cursor_file = os.path.join(cursor_dir, "HeitelCursorProgress.ani")
image_file = os.path.join(cursor_dir, "HeitelCursorsLogo.png")
icon_file = os.path.join(cursor_dir, "HeitelCursorLogoNew.ico")  # Icon-Datei-Pfad hinzufügen
sound_file = os.path.join(cursor_dir, "HeitelHardwareSounde.mp3")
window_file = os.path.join(cursor_dir, "window_icon.png")
sound_icon_file = os.path.join(cursor_dir, "sound_icon.png")
cursor_icon_file = os.path.join(cursor_dir, "cursor_icon.png")
window_icon_file = os.path.join(cursor_dir, "windowsymbol_icon.png")
creep_media_logo_file = os.path.join(cursor_dir, "Creep MediaLogo.png")
dxra_logo_file = os.path.join(cursor_dir, "DXRA_Logo.png")

# URLs der Dateien
cursor_url = "https://cloud.dxra.de/s/728PKXwP8rkxEj3/download/HeitelCursorNormal.cur"
link_cursor_url = "https://cloud.dxra.de/s/NkF2ndtCjJXTXZC/download/Heitel-CursorLink.cur"  # Neue URL für Link-Cursor
text_cursor_url = "https://cloud.dxra.de/s/4PHzdYoRn9pM2Jj/download/Heitelcaretfinal.cur"  # URL für Text-Cursor
wait_cursor_url = "https://cloud.dxra.de/s/7oRegG452G88TcX/download/HeitelCursorLoadingCircle.ani"  # URL für Wait-Cursor
progress_cursor_url = "https://cloud.dxra.de/s/WDkS6kceLkK8gkE/download/HeitelCursorProgress.ani"  # URL für Progress-Cursor
image_url = "https://cloud.dxra.de/s/N4AnLELBgi3Jci9/download/HeitelCursorLogo.png"
icon_url = "https://raw.githubusercontent.com/CreepTV/Heitel-Cursor/refs/heads/main/recources/HeitelCursorLogoNew.ico"
sound_url = "https://cloud.dxra.de/s/ieX32WHSHYjrBYy/download/HeitelHardwareSounde.mp3"
window_url = "https://github.com/CreepTV/Heitel-Cursor/blob/main/recources/window_icon.png"
sound_icon_url = "https://cloud.dxra.de/s/tkLdMagazPr7LJS/download/sound_icon.png"
cursor_icon_url = "https://cloud.dxra.de/s/fSBCty8DwH9tSdq/download/cursor_icon.png"
window_icon_url = "https://cloud.dxra.de/s/QzN3pR5L4qbdxHC/download/windowsymbol_icon.png"
creep_media_logo_url = "https://raw.githubusercontent.com/CreepTV/Heitel-Cursor/main/Heitel%20Cursor%20Site/data/Creep%20MediaLogo.png"
dxra_logo_url = "https://raw.githubusercontent.com/CreepTV/Heitel-Cursor/main/Heitel%20Cursor%20Site/data/DXRA_Logo.png"

# Globales Variablen für das Bild
global img
global image_label

# Dateien herunterladen
def download_files(progress_bar, loading_label):
    files_to_download = {
        cursor_file: cursor_url,
        link_cursor_file: link_cursor_url,
        text_cursor_file: text_cursor_url,
        wait_cursor_file: wait_cursor_url,
        progress_cursor_file: progress_cursor_url,
        image_file: image_url,
        icon_file: icon_url,
        sound_file: sound_url,
        window_file: window_url,
        sound_icon_file: sound_icon_url,
        cursor_icon_file: cursor_icon_url,
        window_icon_file: window_icon_url,
        creep_media_logo_file: creep_media_logo_url,
        dxra_logo_file: dxra_logo_url
    }

    total_files = len(files_to_download)
    files_downloaded = 0
    files_already_present = True

    for file_path, file_url in files_to_download.items():
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            files_already_present = False
            try:
                urllib.request.urlretrieve(file_url, file_path)
                print(f"{os.path.basename(file_path)} heruntergeladen nach: {file_path}")
            except Exception as e:
                print(f"Fehler beim Herunterladen von {os.path.basename(file_path)}: {e}")
        else:
            print(f"{os.path.basename(file_path)} ist bereits vorhanden.")
        
        files_downloaded += 1
        progress = files_downloaded / total_files
        
        # GUI-Aktualisierungen müssen im Haupt-Thread erfolgen
        root.after(0, lambda: update_progress(progress_bar, loading_label, progress, files_already_present))

    root.after(0, lambda: finish_download(loading_label))  # Haupt-Thread verwenden

def update_progress(progress_bar, loading_label, progress, files_already_present):
    progress_bar.set(progress)
    if files_already_present:
        loading_label.configure(text=f"Lade Dateien... ({int(progress * 100)}%)")
    else:
        loading_label.configure(text=f"Lade Dateien herunter... ({int(progress * 100)}%)")

def finish_download(loading_label):
    loading_label.configure(text="Dateien geladen!")
    root.after(1000, show_main_page)  # 1 Sekunde warten, dann zur Hauptseite wechseln

notification_list = []  # Liste, um aktive Benachrichtigungen zu verfolgen

# Initialisiere Pygame-Mixer
pygame.mixer.init()

# Lautstärkeregler Wert
volume_value = 0.5

# Variable to store the click sound file path
click_sound_file = sound_file  # Default to HeitelHardwareSounde.mp3

# Lautstärke einstellen
def set_volume(value):
    global volume_value
    volume_value = float(value) / 100
    pygame.mixer.music.set_volume(volume_value)
    volume_percentage_label.configure(text=f"{int(value)}%")  # Aktualisiere die Prozentanzeige

# Sound abspielen
def play_sound():
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# Function to play the click sound
def play_click_sound():
    if click_sound_enabled.get() and os.path.exists(click_sound_file):
        try:
            sound = pygame.mixer.Sound(click_sound_file)
            sound.set_volume(volume_value)  # Set volume for the click sound
            sound.play()
        except Exception as e:
            print(f"Fehler beim Abspielen des Klicksounds: {e}")

# Function to upload a custom click sound
def upload_click_sound():
    global click_sound_file
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if file_path:
        click_sound_file = file_path
        show_notification("Klicksound erfolgreich geändert!")
        update_click_sound_label()

# Function to reset the click sound to the default
def reset_click_sound():
    global click_sound_file
    click_sound_file = sound_file  # Reset to default sound
    show_notification("Klicksound auf Standard zurückgesetzt!")
    update_click_sound_label()

# Function to update the label showing the current sound file
def update_click_sound_label():
    current_sound_label.configure(text=f"Aktuell: {os.path.basename(click_sound_file)}")

# MyInstants.com Integration
def search_myinstants_sounds(query):
    """
    Sucht nach Sounds auf myinstants.com über die REST API
    """
    try:
        api_url = f"https://myinstants-api.vercel.app/search?q={query}"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        sounds = []
        
        # API gibt ein Objekt mit "data" Array zurück
        if isinstance(data, dict) and 'data' in data:
            sound_data = data['data']
            for sound in sound_data[:10]:
                if sound.get('title') and sound.get('mp3'):
                    sounds.append({
                        'name': sound['title'],
                        'url': sound['mp3'],
                        'id': sound.get('id', ''),
                        'description': sound.get('description', ''),
                        'tags': sound.get('tags', []),
                        'favorites': sound.get('favorites', 0),
                        'views': sound.get('views', 0),
                        'uploader': sound.get('uploader', {})
                    })
        return sounds
    except Exception as e:
        print(f"Fehler bei MyInstants API Suche: {e}")
        return []

def get_popular_sounds():
    """
    Gibt eine Liste beliebter Sounds über die MyInstants API zurück
    """
    try:
        api_url = "https://myinstants-api.vercel.app/best"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        popular_sounds = []
        
        # API gibt ein Objekt mit "data" Array zurück
        if isinstance(data, dict) and 'data' in data:
            sound_data = data['data']
            for sound in sound_data[:8]:
                if sound.get('title'):
                    popular_sounds.append(sound['title'])
        
        if not popular_sounds:
            popular_sounds = [
                "bruh", "oof", "wow", "no", "yes", "nope", "ohh", "ah", "error", "beep",
                "click", "pop", "ding", "bell", "notification", "success", "fail", "tada",
                "whoosh", "swoosh", "thud", "bonk", "boing", "splash", "crash", "boom",
                "laugh", "scream", "sigh", "yawn", "sneeze", "cough", "whistle", "applause"
            ]
        return popular_sounds
    except Exception as e:
        print(f"Fehler bei MyInstants API Best: {e}")
        return [
            "bruh", "oof", "wow", "no", "yes", "nope", "ohh", "ah", "error", "beep",
            "click", "pop", "ding", "bell", "notification", "success", "fail", "tada",
            "whoosh", "swoosh", "thud", "bonk", "boing", "splash", "crash", "boom",
            "laugh", "scream", "sigh", "yawn", "sneeze", "cough", "whistle", "applause"
        ]

def download_myinstants_sound(audio_url, sound_name):
    """
    Lädt einen Sound von MyInstants herunter
    """
    try:
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', sound_name)
        file_extension = '.mp3' if audio_url.endswith('.mp3') else '.wav'
        filename = f"{safe_name}{file_extension}"
        sound_path = os.path.join(cursor_dir, "myinstants_sounds")
        os.makedirs(sound_path, exist_ok=True)
        file_path = os.path.join(sound_path, filename)
        response = requests.get(audio_url, timeout=30)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path
    except Exception as e:
        print(f"Fehler beim Herunterladen des Sounds: {e}")
        return None

def play_myinstants_sound(file_path):
    """
    Spielt einen MyInstants-Sound ab
    """
    try:
        if os.path.exists(file_path):
            sound = pygame.mixer.Sound(file_path)
            sound.set_volume(volume_value)
            sound.play()
            return True
    except Exception as e:
        print(f"Fehler beim Abspielen des Sounds: {e}")
    return False

def set_myinstants_as_click_sound(file_path):
    """
    Setzt einen MyInstants-Sound als Klicksound
    """
    global click_sound_file
    if os.path.exists(file_path):
        click_sound_file = file_path
        show_notification("MyInstants Sound als Klicksound gesetzt!")
        update_click_sound_label()
        return True
    return False

def open_myinstants_browser():
    """
    Öffnet ein Fenster zum Durchsuchen und Auswählen von MyInstants-Sounds
    """
    # Neues Fenster erstellen
    myinstants_window = Toplevel(root)
    myinstants_window.title("MyInstants Sound Browser")
    myinstants_window.geometry("600x500")
    myinstants_window.resizable(True, True)
    
    # Icon setzen falls vorhanden
    if os.path.exists(icon_file):
        myinstants_window.iconbitmap(icon_file)
    
    # Hauptframe
    main_frame = ctk.CTkFrame(myinstants_window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Such-Bereich
    search_frame = ctk.CTkFrame(main_frame)
    search_frame.pack(fill="x", padx=10, pady=10)
    
    search_label = ctk.CTkLabel(search_frame, text="Suche nach Sounds:", font=("Arial", 14))
    search_label.pack(pady=(10, 5), anchor="w", padx=10)
    
    # Eingabefeld und Button nebeneinander
    search_input_frame = ctk.CTkFrame(search_frame)
    search_input_frame.pack(fill="x", padx=10, pady=5)
    
    search_entry = ctk.CTkEntry(search_input_frame, placeholder_text="z.B. 'bruh', 'oof', 'wow'...")
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    search_button = ctk.CTkButton(search_input_frame, text="Suchen", width=100)
    search_button.pack(side="right")
    
    # Ergebnis-Bereich
    results_frame = ctk.CTkFrame(main_frame)
    results_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    results_label = ctk.CTkLabel(results_frame, text="Suchergebnisse:", font=("Arial", 14))
    results_label.pack(pady=(10, 5), anchor="w", padx=10)
    
    # Scrollable Frame für Ergebnisse
    scrollable_frame = ctk.CTkScrollableFrame(results_frame)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Status Label
    status_label = ctk.CTkLabel(results_frame, text="Geben Sie einen Suchbegriff ein und klicken Sie auf 'Suchen'", font=("Arial", 11))
    status_label.pack(pady=5)
    
    # Aktuelle Suche Variable
    current_search_results = []
    
    def search_sounds():
        query = search_entry.get().strip()
        if not query:
            status_label.configure(text="Bitte geben Sie einen Suchbegriff ein")
            return
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        status_label.configure(text="Suche läuft...")
        search_button.configure(text="Suche...", state="disabled")
        def search_thread():
            try:
                sounds = search_myinstants_sounds(query)
                def update_results():
                    nonlocal current_search_results
                    current_search_results = sounds
                    if not sounds:
                        status_label.configure(text="Keine Sounds gefunden. Versuchen Sie einen anderen Suchbegriff.")
                        no_results_label = ctk.CTkLabel(scrollable_frame, text="Keine Ergebnisse gefunden", font=("Arial", 12))
                        no_results_label.pack(pady=20)
                    else:
                        status_label.configure(text=f"{len(sounds)} Sounds gefunden")
                        for i, sound in enumerate(sounds):
                            create_sound_item(scrollable_frame, sound, i)
                    search_button.configure(text="Suchen", state="normal")
                myinstants_window.after(0, update_results)
            except Exception as e:
                def show_error():
                    status_label.configure(text=f"Fehler bei der Suche: {str(e)}")
                    search_button.configure(text="Suchen", state="normal")
                myinstants_window.after(0, show_error)
        threading.Thread(target=search_thread, daemon=True).start()
    
    def create_sound_item(parent, sound, index):
        """
        Erstellt ein GUI-Element für einen Sound
        """
        item_frame = ctk.CTkFrame(parent)
        item_frame.pack(fill="x", padx=5, pady=5)
        
        # Sound-Name
        name_label = ctk.CTkLabel(item_frame, text=sound['name'], font=("Arial", 12, "bold"))
        name_label.pack(pady=(10, 5), anchor="w", padx=10)
        
        # Zusätzliche Informationen anzeigen (Views, Favorites)
        if sound.get('views', 0) > 0 or sound.get('favorites', 0) > 0:
            info_text = f"👁 {sound.get('views', 0)} Aufrufe • ⭐ {sound.get('favorites', 0)} Favoriten"
            info_label = ctk.CTkLabel(item_frame, text=info_text, font=("Arial", 10), text_color="gray")
            info_label.pack(pady=(0, 5), anchor="w", padx=10)
        
        # Description anzeigen falls vorhanden
        if sound.get('description'):
            desc_text = sound['description'][:100] + "..." if len(sound['description']) > 100 else sound['description']
            desc_label = ctk.CTkLabel(item_frame, text=desc_text, font=("Arial", 9), text_color="gray", wraplength=500)
            desc_label.pack(pady=(0, 5), anchor="w", padx=10)
        
        # Button-Frame
        button_frame = ctk.CTkFrame(item_frame)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Anhören Button
        play_button = ctk.CTkButton(button_frame, text="▶ Anhören", width=100, fg_color="#1f6aa5", hover_color="#1e5a96")
        play_button.pack(side="left", padx=(0, 10))
        
        # Auswählen Button
        select_button = ctk.CTkButton(button_frame, text="✓ Auswählen", width=100, fg_color="#2b8a3e", hover_color="#2a7737")
        select_button.pack(side="left")
        
        # Status Label für diesen Sound
        item_status_label = ctk.CTkLabel(item_frame, text="", font=("Arial", 10))
        item_status_label.pack(pady=(0, 5), anchor="w", padx=10)
        
        def play_sound():
            play_button.configure(text="Laden...", state="disabled")
            item_status_label.configure(text="Lade Sound...")
            
            def play_thread():
                try:
                    # Verwende die direkte Audio-URL
                    audio_url = sound['url']
                    
                    # Lade Sound temporär herunter
                    temp_file = download_myinstants_sound(audio_url, f"temp_{sound['name']}")
                    if temp_file:
                        # Spiele Sound ab
                        if play_myinstants_sound(temp_file):
                            def show_success():
                                item_status_label.configure(text="Sound wird abgespielt")
                                play_button.configure(text="▶ Anhören", state="normal")
                            myinstants_window.after(0, show_success)
                        else:
                            def show_error():
                                item_status_label.configure(text="Fehler beim Abspielen")
                                play_button.configure(text="▶ Anhören", state="normal")
                            myinstants_window.after(0, show_error)
                    else:
                        def show_error():
                            item_status_label.configure(text="Fehler beim Laden")
                            play_button.configure(text="▶ Anhören", state="normal")
                        myinstants_window.after(0, show_error)
                        
                except Exception as e:
                    def show_error():
                        item_status_label.configure(text=f"Fehler: {str(e)}")
                        play_button.configure(text="▶ Anhören", state="normal")
                    myinstants_window.after(0, show_error)
            
            threading.Thread(target=play_thread, daemon=True).start()
        
        def select_sound():
            select_button.configure(text="Laden...", state="disabled")
            item_status_label.configure(text="Lade Sound herunter...")
            
            def select_thread():
                try:
                    # Verwende die direkte Audio-URL
                    audio_url = sound['url']
                    
                    # Lade Sound dauerhaft herunter
                    downloaded_file = download_myinstants_sound(audio_url, sound['name'])
                    if downloaded_file:
                        # Setze als Klicksound
                        if set_myinstants_as_click_sound(downloaded_file):
                            def show_success():
                                item_status_label.configure(text="✓ Als Klicksound gesetzt!")
                                select_button.configure(text="✓ Ausgewählt", state="disabled", fg_color="green")
                                # Schließe das Fenster nach kurzer Verzögerung
                                myinstants_window.after(2000, myinstants_window.destroy)
                            myinstants_window.after(0, show_success)
                        else:
                            def show_error():
                                item_status_label.configure(text="Fehler beim Setzen als Klicksound")
                                select_button.configure(text="✓ Auswählen", state="normal")
                            myinstants_window.after(0, show_error)
                    else:
                        def show_error():
                            item_status_label.configure(text="Fehler beim Download")
                            select_button.configure(text="✓ Auswählen", state="normal")
                        myinstants_window.after(0, show_error)
                        
                except Exception as e:
                    def show_error():
                        item_status_label.configure(text=f"Fehler: {str(e)}")
                        select_button.configure(text="✓ Auswählen", state="normal")
                    myinstants_window.after(0, show_error)
            
            threading.Thread(target=select_thread, daemon=True).start()
        
        # Button-Events verbinden
        play_button.configure(command=play_sound)
        select_button.configure(command=select_sound)
    
    # Such-Events
    search_button.configure(command=search_sounds)
    search_entry.bind("<Return>", lambda e: search_sounds())
    
    # Schließen Button
    close_button = ctk.CTkButton(main_frame, text="Schließen", command=myinstants_window.destroy, fg_color="red", hover_color="darkred")
    close_button.pack(pady=10)

# Function to open URL in default browser
def open_url(url):
    try:
        webbrowser.open(url)
        show_notification(f"Öffne {url} im Browser...")
    except Exception as e:
        show_notification(f"Fehler beim Öffnen der URL: {e}")

# Funktion zum Setzen des Text-Cursors (Caret)
def set_text_cursor_color(color_hex):
    """
    Setzt den Text-Cursor (Caret) mit einer eigenen Cursor-Datei
    color_hex: Hex-Farbcode (z.B. "#F2C4B0") - wird als Fallback verwendet
    """
    try:
        # Verwende eigene Text-Cursor-Datei falls vorhanden
        if os.path.exists(text_cursor_file):
            # Caret-Größe auf 50% der Standard-Größe reduzieren (ca. 42px bei 85px Standard)
            caret_size = int(85 * 0.5)  # 50% kleiner als Standard
            text_cursor = ctypes.windll.user32.LoadImageW(0, text_cursor_file, win32con.IMAGE_CURSOR, caret_size, caret_size, win32con.LR_LOADFROMFILE)
            if text_cursor:
                ctypes.windll.user32.SetSystemCursor(text_cursor, 32513)  # IDC_IBEAM (Text Select)
                return True
        
        # Fallback: Setze Registry-Einstellungen für Caret-Farbe
        color_hex = color_hex.lstrip('#')
        r = int(color_hex[0:2], 16)
        g = int(color_hex[2:4], 16)
        b = int(color_hex[4:6], 16)
        
        # Windows RGB-Wert
        color_rgb = (r << 16) | (g << 8) | b
        
        import winreg
        try:
            # Personalization Registry Key für Akzentfarbe
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 
                                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "ColorPrevalence", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "AccentColor", 0, winreg.REG_DWORD, color_rgb)
            winreg.CloseKey(key)
            
            # Desktop Registry für Caret-Breite
            key2 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Control Panel\Desktop", 
                                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key2, "CaretWidth", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key2)
            
            # Aktualisiere Systemeinstellungen
            ctypes.windll.user32.SystemParametersInfoW(0x0015, 0, None, 0x0001)
            
            return True
        except Exception as reg_error:
            print(f"Registry-Fehler: {reg_error}")
            return False
            
    except Exception as e:
        print(f"Fehler beim Setzen des Text-Cursors: {e}")
        return False

# Lade eine benutzerdefinierte Cursor-Datei
def set_custom_cursor():
    cursor = ctypes.windll.user32.LoadImageW(0, cursor_file, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
    if cursor:
        ctypes.windll.user32.SetSystemCursor(cursor, 32512)  # IDC_ARROW (Normal Select)
        
        # Verwende separaten Link-Cursor falls vorhanden, sonst den normalen Cursor
        if os.path.exists(link_cursor_file):
            link_cursor = ctypes.windll.user32.LoadImageW(0, link_cursor_file, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
            if link_cursor:
                ctypes.windll.user32.SetSystemCursor(link_cursor, 32649)  # IDC_HAND (Link Select)
            else:
                ctypes.windll.user32.SetSystemCursor(cursor, 32649)  # Fallback auf normalen Cursor
        else:
            ctypes.windll.user32.SetSystemCursor(cursor, 32649)  # Fallback auf normalen Cursor
        
        # Verwende separaten Wait-Cursor falls vorhanden, sonst den normalen Cursor
        if os.path.exists(wait_cursor_file):
            wait_cursor = ctypes.windll.user32.LoadImageW(0, wait_cursor_file, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
            if wait_cursor:
                ctypes.windll.user32.SetSystemCursor(wait_cursor, 32514)  # IDC_WAIT (Wait/Busy)
            else:
                ctypes.windll.user32.SetSystemCursor(cursor, 32514)  # Fallback auf normalen Cursor
        else:
            ctypes.windll.user32.SetSystemCursor(cursor, 32514)  # Fallback auf normalen Cursor
        
        # Verwende separaten Progress-Cursor falls vorhanden, sonst den normalen Cursor
        if os.path.exists(progress_cursor_file):
            progress_cursor = ctypes.windll.user32.LoadImageW(0, progress_cursor_file, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
            if progress_cursor:
                ctypes.windll.user32.SetSystemCursor(progress_cursor, 32650)  # IDC_APPSTARTING (Working In Background)
            else:
                ctypes.windll.user32.SetSystemCursor(cursor, 32650)  # Fallback auf normalen Cursor
        else:
            ctypes.windll.user32.SetSystemCursor(cursor, 32650)  # Fallback auf normalen Cursor
        
        # Setze den Text-Cursor (Caret)
        set_text_cursor_color("#F2C4B0")
            
        show_notification("MuhammedCursor wurde gesetzt!")
        play_sound()
    else:
        show_notification("Fehler beim Laden des Cursors")
        play_sound()

# Lade eine benutzerdefinierte Cursor-Datei mit angepasster Größe
def set_custom_cursor_with_size(size):
    cursor = ctypes.windll.user32.LoadImageW(0, cursor_file, win32con.IMAGE_CURSOR, size, size, win32con.LR_LOADFROMFILE)
    if cursor:
        ctypes.windll.user32.SetSystemCursor(cursor, 32512)  # IDC_ARROW (Normal Select)
        
        # Verwende separaten Link-Cursor falls vorhanden, sonst den normalen Cursor
        if os.path.exists(link_cursor_file):
            link_cursor = ctypes.windll.user32.LoadImageW(0, link_cursor_file, win32con.IMAGE_CURSOR, size, size, win32con.LR_LOADFROMFILE)
            if link_cursor:
                ctypes.windll.user32.SetSystemCursor(link_cursor, 32649)  # IDC_HAND (Link Select)
            else:
                ctypes.windll.user32.SetSystemCursor(cursor, 32649)  # Fallback auf normalen Cursor
        else:
            ctypes.windll.user32.SetSystemCursor(cursor, 32649)  # Fallback auf normalen Cursor
        
        # Verwende separaten Wait-Cursor falls vorhanden, sonst den normalen Cursor
        if os.path.exists(wait_cursor_file):
            wait_cursor = ctypes.windll.user32.LoadImageW(0, wait_cursor_file, win32con.IMAGE_CURSOR, size, size, win32con.LR_LOADFROMFILE)
            if wait_cursor:
                ctypes.windll.user32.SetSystemCursor(wait_cursor, 32514)  # IDC_WAIT (Wait/Busy)
            else:
                ctypes.windll.user32.SetSystemCursor(cursor, 32514)  # Fallback auf normalen Cursor
        else:
            ctypes.windll.user32.SetSystemCursor(cursor, 32514)  # Fallback auf normalen Cursor
        
        # Verwende separaten Progress-Cursor falls vorhanden, sonst den normalen Cursor
        if os.path.exists(progress_cursor_file):
            progress_cursor = ctypes.windll.user32.LoadImageW(0, progress_cursor_file, win32con.IMAGE_CURSOR, size, size, win32con.LR_LOADFROMFILE)
            if progress_cursor:
                ctypes.windll.user32.SetSystemCursor(progress_cursor, 32650)  # IDC_APPSTARTING (Working In Background)
            else:
                ctypes.windll.user32.SetSystemCursor(cursor, 32650)  # Fallback auf normalen Cursor
        else:
            ctypes.windll.user32.SetSystemCursor(cursor, 32650)  # Fallback auf normalen Cursor
        
        # Setze den Text-Cursor (Caret) mit angepasster Größe
        if os.path.exists(text_cursor_file):
            # Caret-Größe auf 50% der normalen Cursor-Größe reduzieren
            caret_size = int(size * 0.6)
            text_cursor = ctypes.windll.user32.LoadImageW(0, text_cursor_file, win32con.IMAGE_CURSOR, caret_size, caret_size, win32con.LR_LOADFROMFILE)
            if text_cursor:
                ctypes.windll.user32.SetSystemCursor(text_cursor, 32513)  # IDC_IBEAM (Text Select)
            else:
                set_text_cursor_color("#F2C4B0")  # Fallback
        else:
            set_text_cursor_color("#F2C4B0")  # Fallback
            
        play_sound()
    else:
        show_notification("Fehler beim Laden des Cursors")
        play_sound()

# Setzt den Standard-Cursor zurück
def reset_cursor():
    ctypes.windll.user32.SystemParametersInfoW(87, 0, None, 0)
    show_notification("Standard-Cursor wiederhergestellt!")
    play_click_sound()

# Beendet das Programm
def exit_program():
    play_sound()
    root.quit()

# Benachrichtigung anzeigen
def show_notification(message):
    notification = Toplevel()
    notification.overrideredirect(True)
    notification.configure(bg='black')  # Hintergrund schwarz setzen
    notification.attributes("-topmost", True)
    
    # Container für Bild und Text
    content_frame = Label(notification, bg='black')
    content_frame.pack()

    # Bild hinzufügen
    try:
        if os.path.exists(image_file):
            img = Image.open(image_file)
            img = img.resize((32, 32))  # Größe des Bildes anpassen
            photo = ImageTk.PhotoImage(img)
            image_label = Label(content_frame, image=photo, bg='black')
            image_label.image = photo  # Referenz speichern
            image_label.pack(side='left', padx=5)
    except (FileNotFoundError, UnidentifiedImageError) as e:
        print(f"Fehler beim Laden des Bildes: {e}")

    label = Label(content_frame, text=message, bg="black", fg="white", padx=10, pady=5, font=("Arial", 12))
    label.pack(side='left')

    # Dynamisch die Größe der Benachrichtigungsbox anpassen
    notification.update_idletasks()
    notification_width = content_frame.winfo_reqwidth() + 20
    notification_height = content_frame.winfo_reqheight() + 10
    screen_width = notification.winfo_screenwidth()
    screen_height = notification.winfo_screenheight()

    # Position der neuen Benachrichtigung berechnen
    padding = 10  # Abstand zwischen den Benachrichtigungen
    y_position = screen_height - notification_height - 100 - (len(notification_list) * (notification_height + padding))
    x_position = screen_width - notification_width - 20
    notification.geometry(f"{notification_width}x{notification_height}+{x_position}+{y_position}")
    
    notification_list.append((notification, notification_height))

    # Entferne Benachrichtigung nach 2 Sekunden
    def remove_notification():
        notification.destroy()
        notification_list.remove((notification, notification_height))
        for i, (noti, height) in enumerate(notification_list):
            new_y_position = screen_height - height - 100 - (i * (height + padding))
            noti.geometry(f"{notification_width}x{height}+{x_position}+{new_y_position}")

    notification.after(2000, remove_notification)

def set_appearance_mode(mode):
    ctk.set_appearance_mode(mode)
    update_appearance_buttons(mode)

def update_appearance_buttons(active_mode):
    modes = ["Dark", "Light", "System"]
    buttons = [dark_mode_button, light_mode_button, system_mode_button]
    for mode, button in zip(modes, buttons):
        if mode == active_mode:
            if mode == "Dark":
                button.configure(fg_color="gray")
            elif mode == "Light":
                button.configure(fg_color="gray")
            elif mode == "System":
                button.configure(fg_color="lightgray")
        else:
            if mode == "Dark":
                button.configure(fg_color="darkgray")
            elif mode == "Light":
                button.configure(fg_color="white")
            elif mode == "System":
                button.configure(fg_color="gray")

# GUI erstellen
def create_gui():
    ctk.set_appearance_mode("System")  # "Dark", "Light", or "System"
    ctk.set_default_color_theme("blue")
    
    global frame
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Header-Frame für das Logo
    header_frame = ctk.CTkFrame(frame, height=100, corner_radius=10)
    header_frame.pack(fill="x", padx=10, pady=(10, 0))
    header_frame.pack_propagate(False)  # Verhindert, dass der Frame seine Größe ändert

    # Bild einfügen
    global img, image_label
    try:
        if os.path.exists(image_file):
            img = CTkImage(Image.open(image_file), size=(84, 84))
            image_label = ctk.CTkLabel(header_frame, image=img, text="")
            image_label.pack(anchor="ne", padx=10, pady=8)
            print(f"Logo erfolgreich geladen: {image_file}")  # Debug-Ausgabe
        else:
            print(f"Logo-Datei nicht gefunden: {image_file}")  # Debug-Ausgabe
    except (FileNotFoundError, UnidentifiedImageError) as e:
        print(f"Fehler beim Laden des Bildes: {e}")
    
    # Tab-Steuerung hinzufügen
    tab_control = ctk.CTkTabview(frame)
    tab_control.pack(pady=10, padx=0, fill="both", expand=True)  # Tabs weiter nach links verschieben
    
    # Tab für Cursor-Einstellungen
    tab_cursor = tab_control.add("Cursor")
    
    cursor_frame = ctk.CTkFrame(tab_cursor, corner_radius=10)
    cursor_frame.pack(pady=10, padx=10, fill="x", anchor="w")
    
    label = ctk.CTkLabel(cursor_frame, text="Wähle einen Cursor:", font=("Arial", 16))
    label.pack(pady=10, anchor="w", padx=10)  # Linken Abstand hinzufügen
    
    button_set = ctk.CTkButton(cursor_frame, text="MuhammedCursor setzen", command=lambda: set_custom_cursor_with_size(int(cursor_size_slider.get())), fg_color="#cc7000", hover_color="#994c00")
    button_set.pack(pady=5, anchor="w", padx=10)  # Linken Abstand hinzufügen
    
    button_reset = ctk.CTkButton(cursor_frame, text="Standard-Cursor wiederherstellen", command=reset_cursor)
    button_reset.pack(pady=5, anchor="w", padx=10)  # Linken Abstand hinzufügen
    
    # Tab für Einstellungen
    tab_settings = tab_control.add("Settings")

    # Vertikale Leiste für Sound und Cursors mit Symbolen
    settings_frame = ctk.CTkFrame(tab_settings)
    settings_frame.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

    sidebar_frame = ctk.CTkFrame(settings_frame, width=40, corner_radius=0)  # Dünnere Leiste
    sidebar_frame.pack(side="left", fill="y")
    sidebar_frame.pack_propagate(False)

    # Symbole laden
    try:
        sound_image = CTkImage(Image.open(sound_icon_file), size=(20, 20))
        cursor_image = CTkImage(Image.open(cursor_icon_file), size=(20, 20))
        window_image = CTkImage(Image.open(window_icon_file), size=(20, 20))
        # Für Credits verwenden wir das HeitelCursor Logo
        credits_image = CTkImage(Image.open(image_file), size=(20, 20))
    except (FileNotFoundError, UnidentifiedImageError) as e:
        print(f"Fehler beim Laden der Symbole: {e}")
        sound_image = None
        cursor_image = None
        window_image = None
        credits_image = None

    sound_button = ctk.CTkButton(sidebar_frame, image=sound_image, text="", width=30, height=30,  # Größe anpassen
                                   command=lambda: show_settings_tab("Sound", sound_frame, cursor_frame, window_frame, credits_frame))
    sound_button.pack(pady=(20, 0), padx=5)  # Padding anpassen

    cursor_button = ctk.CTkButton(sidebar_frame, image=cursor_image, text="", width=30, height=30,  # Größe anpassen
                                    command=lambda: show_settings_tab("Cursors", sound_frame, cursor_frame, window_frame, credits_frame))
    cursor_button.pack(pady=(20, 0), padx=5)  # Padding anpassen

    window_button = ctk.CTkButton(sidebar_frame, image=window_image, text="", width=30, height=30,  # Größe anpassen
                                    command=lambda: show_settings_tab("Window", sound_frame, cursor_frame, window_frame, credits_frame))
    window_button.pack(pady=(20, 0), padx=5)  # Padding anpassen

    credits_button = ctk.CTkButton(sidebar_frame, image=credits_image, text="", width=30, height=30,  # Größe anpassen
                                     command=lambda: show_settings_tab("Credits", sound_frame, cursor_frame, window_frame, credits_frame))
    credits_button.pack(pady=(20, 0), padx=5)  # Padding anpassen

    # Frames für Sound-, Cursor-, Fenster- und Credits-Einstellungen
    sound_frame = ctk.CTkFrame(settings_frame, corner_radius=0)
    cursor_frame = ctk.CTkFrame(settings_frame, corner_radius=0)
    window_frame = ctk.CTkFrame(settings_frame, corner_radius=0)
    credits_frame = ctk.CTkFrame(settings_frame, corner_radius=0)

    def show_settings_tab(value, sound_frame, cursor_frame, window_frame, credits_frame):
        if value == "Sound":
            sound_frame.pack(side="right", fill="both", expand=True)
            cursor_frame.pack_forget()
            window_frame.pack_forget()
            credits_frame.pack_forget()
        elif value == "Cursors":
            cursor_frame.pack(side="right", fill="both", expand=True)
            sound_frame.pack_forget()
            window_frame.pack_forget()
            credits_frame.pack_forget()
        elif value == "Window":
            window_frame.pack(side="right", fill="both", expand=True)
            sound_frame.pack_forget()
            cursor_frame.pack_forget()
            credits_frame.pack_forget()
        elif value == "Credits":
            credits_frame.pack(side="right", fill="both", expand=True)
            sound_frame.pack_forget()
            cursor_frame.pack_forget()
            window_frame.pack_forget()

    # Sound Einstellungen
    volume_label = ctk.CTkLabel(sound_frame, text="Lautstärke", font=("Arial", 16))
    volume_label.pack(pady=5, anchor="w", padx=10)

    # Lautstärkeregler und Prozentanzeige hinzufügen
    volume_frame = ctk.CTkFrame(sound_frame, corner_radius=10)
    volume_frame.pack(pady=5, padx=10, fill="x", anchor="w")

    volume_slider = CTkSlider(volume_frame, from_=0, to=100, command=set_volume)
    volume_slider.set(volume_value * 100)  # Setze die anfängliche Lautstärke auf 50%
    volume_slider.pack(side="left", fill="x", expand=True, padx=(0, 5))

    # Prozentanzeige hinzufügen
    global volume_percentage_label
    volume_percentage_label = ctk.CTkLabel(volume_frame, text=f"{int(volume_value * 100)}%", font=("Arial", 12))
    volume_percentage_label.pack(side="left", padx=(5, 10))

    # Add click sound settings to the sound frame
    click_sound_label = ctk.CTkLabel(sound_frame, text="Klicksound", font=("Arial", 16))
    click_sound_label.pack(pady=5, anchor="w", padx=10)

    click_sound_frame = ctk.CTkFrame(sound_frame, corner_radius=10)
    click_sound_frame.pack(pady=5, padx=10, fill="x", anchor="w")

    click_sound_checkbox = ctk.CTkCheckBox(click_sound_frame, text="Aktivieren", variable=click_sound_enabled)
    click_sound_checkbox.pack(side="left", padx=(0, 10))

    upload_sound_button = ctk.CTkButton(click_sound_frame, text="Eigenen Sound hochladen", command=upload_click_sound)
    upload_sound_button.pack(side="left", padx=(10, 0))

    # MyInstants Button in separater Zeile hinzufügen
    myinstants_frame = ctk.CTkFrame(sound_frame, corner_radius=10)
    myinstants_frame.pack(pady=5, padx=10, fill="x", anchor="w")

    myinstants_button = ctk.CTkButton(myinstants_frame, text="MyInstants durchsuchen", command=open_myinstants_browser, fg_color="#ff6b35", hover_color="#e85a2b")
    myinstants_button.pack(side="left", padx=10, pady=5)

    # Label to display the current sound file
    global current_sound_label
    current_sound_label = ctk.CTkLabel(sound_frame, text=f"Aktuell: {os.path.basename(click_sound_file)}", font=("Arial", 10))
    current_sound_label.pack(pady=(5, 0), anchor="w", padx=10)

    # Move the reset button below the current sound label
    reset_sound_button = ctk.CTkButton(sound_frame, text="Standard wiederherstellen", command=reset_click_sound)
    reset_sound_button.pack(pady=(5, 0), anchor="w", padx=10)

    # Cursor Einstellungen
    cursor_label = ctk.CTkLabel(cursor_frame, text="Cursors", font=("Arial", 16))
    cursor_label.pack(pady=(0, 0), anchor="w", padx=10)  # Padding unten hinzufügen

    # Cursor Größe Einstellungen
    cursor_size_label = ctk.CTkLabel(cursor_frame, text="Cursor Größe:", font=("Arial", 11))
    cursor_size_label.pack(pady=(0, 5), anchor="w", padx=10)  # Padding unten hinzufügen

    cursor_size_frame = ctk.CTkFrame(cursor_frame, corner_radius=10)
    cursor_size_frame.pack(pady=5, padx=10, fill="x", anchor="w")

    cursor_size_slider = CTkSlider(cursor_size_frame, from_=16, to=128, orientation=HORIZONTAL)
    cursor_size_slider.set(85)  # Setze die anfängliche Größe auf 85
    cursor_size_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

    cursor_size_value_label = ctk.CTkLabel(cursor_size_frame, text="85", font=("Arial", 12))
    cursor_size_value_label.pack(side="left", padx=(5, 10))

    def update_cursor_size(size):
        size = int(size)
        cursor_size_value_label.configure(text=str(size))
        set_custom_cursor_with_size(size)  # Aktualisiere die Cursorgröße

    cursor_size_slider.configure(command=update_cursor_size)
    update_cursor_size(85)  # Initiale Größe

    # Knopf zum Zurücksetzen der Größe auf 86
    def reset_to_standard_size():
        cursor_size_slider.set(86)
        cursor_size_value_label.configure(text="86")
        set_custom_cursor_with_size(86)  # Aktualisiere die Cursorgröße

    button_reset_size = ctk.CTkButton(cursor_frame, text="Standardgröße zurücksetzen", command=reset_to_standard_size)
    button_reset_size.pack(pady=5, anchor="w", padx=10)  # Linken Abstand hinzufügen

    # Fenster Einstellungen
    window_label = ctk.CTkLabel(window_frame, text="Anwendung", font=("Arial", 16))
    window_label.pack(pady=5, anchor="w", padx=10)

    # Farbschema Einstellungen
    appearance_label = ctk.CTkLabel(window_frame, text="Farbschema:", font=("Arial", 11))
    appearance_label.pack(pady=(10, 5), anchor="w", padx=10)

    appearance_frame = ctk.CTkFrame(window_frame, corner_radius=10)
    appearance_frame.pack(pady=5, padx=10, fill="x", anchor="w")

    global dark_mode_button, light_mode_button, system_mode_button

    dark_mode_button = ctk.CTkButton(appearance_frame, text="Dunkel", command=lambda: set_appearance_mode("Dark"), width=40, height=20)
    dark_mode_button.pack(side="left", padx=5, pady=5)

    light_mode_button = ctk.CTkButton(appearance_frame, text="Hell", command=lambda: set_appearance_mode("Light"), width=40, height=20)
    light_mode_button.pack(side="left", padx=5, pady=5)

    system_mode_button = ctk.CTkButton(appearance_frame, text="System", command=lambda: set_appearance_mode("System"), width=40, height=20)
    system_mode_button.pack(side="left", padx=5, pady=5)

    # Set initial appearance mode
    update_appearance_buttons("System")

    # Weitere Fenster-Einstellungen hier hinzufügen
    
    # Dateien-Management Sektion
    files_label = ctk.CTkLabel(window_frame, text="Dateien-Management:", font=("Arial", 11))
    files_label.pack(pady=(20, 5), anchor="w", padx=10)

    files_frame = ctk.CTkFrame(window_frame, corner_radius=10)
    files_frame.pack(pady=5, padx=10, fill="x", anchor="w")

    redownload_button = ctk.CTkButton(files_frame, text="Dateien neu herunterladen", command=redownload_files, 
                                     fg_color="#0078d4", hover_color="#106ebe")
    redownload_button.pack(side="left", padx=5, pady=5)

    # Initiales Anzeigen des Sound-Tabs
    show_settings_tab("Sound", sound_frame, cursor_frame, window_frame, credits_frame)
    
    # Credits Einstellungen - Scrollable Frame
    credits_scrollable = ctk.CTkScrollableFrame(credits_frame, corner_radius=10)
    credits_scrollable.pack(fill="both", expand=True, padx=2, pady=2)

    credits_title = ctk.CTkLabel(credits_scrollable, text="Credits", font=("Arial", 20, "bold"))
    credits_title.pack(pady=(10, 8), anchor="w", padx=8)

    # Entwickler Information
    developer_frame = ctk.CTkFrame(credits_scrollable, corner_radius=10)
    developer_frame.pack(pady=5, padx=8, fill="x", anchor="w")

    developer_label = ctk.CTkLabel(developer_frame, text="Entwickler:", font=("Arial", 14, "bold"))
    developer_label.pack(pady=(8, 3), anchor="w", padx=8)

    developer_info = ctk.CTkLabel(developer_frame, text="CreepTV", font=("Arial", 12))
    developer_info.pack(pady=(0, 8), anchor="w", padx=8)

    # Version Information
    version_frame = ctk.CTkFrame(credits_scrollable, corner_radius=10)
    version_frame.pack(pady=5, padx=8, fill="x", anchor="w")

    version_label = ctk.CTkLabel(version_frame, text="Version:", font=("Arial", 14, "bold"))
    version_label.pack(pady=(8, 3), anchor="w", padx=8)

    version_info = ctk.CTkLabel(version_frame, text="HeitelCursor v3.7", font=("Arial", 12))
    version_info.pack(pady=(0, 8), anchor="w", padx=8)

    # Website Information
    website_frame = ctk.CTkFrame(credits_scrollable, corner_radius=10)
    website_frame.pack(pady=5, padx=8, fill="x", anchor="w")

    website_label = ctk.CTkLabel(website_frame, text="Website:", font=("Arial", 14, "bold"))
    website_label.pack(pady=(8, 3), anchor="w", padx=8)

    website_info = ctk.CTkLabel(website_frame, text="https://heitelcursor.tech/", font=("Arial", 12), text_color="#1f6aa5", cursor="hand2")
    website_info.pack(pady=(0, 8), anchor="w", padx=8)
    
    # Bind click event to open URL
    website_info.bind("<Button-1>", lambda e: open_url("https://heitelcursor.tech/"))

    # Verwendete Technologien
    tech_frame = ctk.CTkFrame(credits_scrollable, corner_radius=10)
    tech_frame.pack(pady=5, padx=8, fill="x", anchor="w")

    tech_label = ctk.CTkLabel(tech_frame, text="Verwendete Technologien:", font=("Arial", 14, "bold"))
    tech_label.pack(pady=(8, 3), anchor="w", padx=8)

    tech_list = [
        "• Python 3.x",
        "• CustomTkinter (GUI)",
        "• Pillow (Bildverarbeitung)",
        "• Pygame (Audio)",
        "• Pynput (Maus-Events)",
        "• Win32 API (Windows Integration)"
    ]

    for tech in tech_list:
        tech_item = ctk.CTkLabel(tech_frame, text=tech, font=("Arial", 11), wraplength=300)
        tech_item.pack(pady=(0, 1), anchor="w", padx=8)

    tech_frame.pack(pady=(0, 5))

    # Projektbeschreibung
    description_frame = ctk.CTkFrame(credits_scrollable, corner_radius=10)
    description_frame.pack(pady=5, padx=8, fill="x", anchor="w")

    description_label = ctk.CTkLabel(description_frame, text="Über HeitelCursor:", font=("Arial", 14, "bold"))
    description_label.pack(pady=(8, 3), anchor="w", padx=8)

    description_text = ctk.CTkLabel(description_frame, text="HeitelCursor ist ein benutzerfreundliches Tool zur Anpassung\ndes Windows-Cursors. Es ermöglicht das einfache Setzen\nvon benutzerdefinierten Cursors mit verschiedenen Größen\nund Funktionen.", font=("Arial", 11), justify="left", wraplength=300)
    description_text.pack(pady=(0, 8), anchor="w", padx=8)

    # Features
    features_frame = ctk.CTkFrame(credits_scrollable, corner_radius=10)
    features_frame.pack(pady=5, padx=8, fill="x", anchor="w")

    features_label = ctk.CTkLabel(features_frame, text="Features:", font=("Arial", 14, "bold"))
    features_label.pack(pady=(8, 3), anchor="w", padx=8)

    features_list = [
        "• Benutzerdefinierte Cursor-Dateien",
        "• Anpassbare Cursor-Größe (16-128px)",
        "• Separate Link- und Text-Cursor",
        "• Sound-Effekte und Benachrichtigungen",
        "• Klicksound-Funktionalität",
        "• Verschiedene Farbschemata",
        "• Automatisches Dateien-Management",
        "• Hello im Muhammed!"
    ]

    for feature in features_list:
        feature_item = ctk.CTkLabel(features_frame, text=feature, font=("Arial", 11), wraplength=300)
        feature_item.pack(pady=(0, 1), anchor="w", padx=8)

    features_frame.pack(pady=(0, 5))

    # Dankeschön
    thanks_frame = ctk.CTkFrame(credits_scrollable, corner_radius=10)
    thanks_frame.pack(pady=5, padx=8, fill="x", anchor="w")

    thanks_label = ctk.CTkLabel(thanks_frame, text="Besonderer Dank an:", font=("Arial", 14, "bold"))
    thanks_label.pack(pady=(8, 3), anchor="w", padx=8)

    thanks_text = ctk.CTkLabel(thanks_frame, text="• DXRA - für den ersten Cursor und die Idee des MuhammedCursors\n• Alle Nutzer und Supporter der HeitelCursor Community!\nDank euch wird dieses Projekt stetig weiterentwickelt.", font=("Arial", 12), justify="left", wraplength=300)
    thanks_text.pack(pady=(0, 8), anchor="w", padx=8)

    # Support Information
    support_frame = ctk.CTkFrame(credits_scrollable, corner_radius=10)
    support_frame.pack(pady=5, padx=8, fill="x", anchor="w")

    support_label = ctk.CTkLabel(support_frame, text="Support & Feedback:", font=("Arial", 14, "bold"))
    support_label.pack(pady=(8, 3), anchor="w", padx=8)

    support_text = ctk.CTkLabel(support_frame, text="Bei Fragen oder Problemen besuchen Sie bitte:\n• GitHub Repository: CreepTV/Heitel-Cursor\n• Issues und Feature Requests sind willkommen\n• Website: https://heitelcursor.tech/", font=("Arial", 11), justify="left", wraplength=300)
    support_text.pack(pady=(0, 8), anchor="w", padx=8)

    # Copyright
    copyright_label = ctk.CTkLabel(credits_scrollable, text="© 2025 HerrMuhammed- Alle Rechte vorbehalten", font=("Arial", 10))
    copyright_label.pack(pady=(10, 5), anchor="center")
    
    # Logos Frame - Zwei kleine Logos nebeneinander
    logos_frame = ctk.CTkFrame(credits_scrollable, corner_radius=10)
    logos_frame.pack(pady=5, padx=8, fill="x", anchor="center")
    
    # Container für die Logos
    logos_container = ctk.CTkFrame(logos_frame, corner_radius=0, fg_color="transparent")
    logos_container.pack(pady=10, anchor="center")
    
    try:
        # Erstes Logo (Creep MediaLogo)
        creep_logo_file = os.path.join(cursor_dir, "Creep MediaLogo.png")
        if os.path.exists(creep_logo_file):
            logo1 = CTkImage(Image.open(creep_logo_file), size=(40, 40))
            logo1_label = ctk.CTkLabel(logos_container, image=logo1, text="")
            logo1_label.pack(side="left", padx=5)
        elif os.path.exists(image_file):  # Fallback auf HeitelCursor Logo
            logo1 = CTkImage(Image.open(image_file), size=(40, 40))
            logo1_label = ctk.CTkLabel(logos_container, image=logo1, text="")
            logo1_label.pack(side="left", padx=5)
        
        # Zweites Logo (DXRA Logo)
        dxra_logo_file = os.path.join(cursor_dir, "DXRA_Logo.png")
        if os.path.exists(dxra_logo_file):
            logo2 = CTkImage(Image.open(dxra_logo_file), size=(40, 40))
            logo2_label = ctk.CTkLabel(logos_container, image=logo2, text="")
            logo2_label.pack(side="left", padx=5)
        elif os.path.exists(window_icon_file):  # Fallback auf window_icon
            logo2 = CTkImage(Image.open(window_icon_file), size=(40, 40))
            logo2_label = ctk.CTkLabel(logos_container, image=logo2, text="")
            logo2_label.pack(side="left", padx=5)
        
    except (FileNotFoundError, UnidentifiedImageError) as e:
        print(f"Fehler beim Laden der Logos: {e}")
        # Fallback: Nur Text wenn Logos nicht geladen werden können
        fallback_label = ctk.CTkLabel(logos_container, text="CreepTV & DXRA", font=("Arial", 12))
        fallback_label.pack(pady=10)
    
    # Leiste unten
    bottom_frame = ctk.CTkFrame(root, height=40, corner_radius=10)
    bottom_frame.pack(fill="x", side="bottom", padx=10, pady=5)
    
    button_exit = ctk.CTkButton(bottom_frame, text="Beenden", command=exit_program, fg_color="red", hover_color="darkred")
    button_exit.pack(pady=5, padx=10, anchor="e")  # Positioniere den Button unten rechts

def show_loading_page():
    global root, click_sound_enabled  # Declare click_sound_enabled as global
    root = ctk.CTk()
    root.title("MuhammedCursor")
    root.geometry("430x510")  # Größe des Hauptfensters um 20% vergrößern
    root.resizable(False, False)  # Fenstergröße nicht veränderbar

    # Initialize click_sound_enabled as disabled by default
    click_sound_enabled = tk.BooleanVar(value=False)  # Default to disabled

    # Bind left mouse click to play_click_sound
    root.bind("<Button-1>", lambda event: play_click_sound())

    # Icon setzen
    if os.path.exists(icon_file):
        root.iconbitmap(icon_file)

    global frame
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    loading_label = ctk.CTkLabel(frame, text="Lade Dateien herunter...", font=("Arial", 16))
    loading_label.pack(pady=20)

    progress_bar = CTkProgressBar(frame, width=300)
    progress_bar.set(0)
    progress_bar.pack(pady=10)

    # Starten des Downloads in einem separaten Thread
    download_thread = threading.Thread(target=download_files, args=(progress_bar, loading_label))
    download_thread.start()

def show_main_page():
    # Zerstöre die Lade-Widgets und den Frame
    frame.destroy()
    create_gui()

# Function to handle global mouse clicks
def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:  # Check for left mouse button press
        play_click_sound()

# Start a global mouse listener
def start_global_mouse_listener():
    listener = mouse.Listener(on_click=on_click)
    listener.start()

# Funktion zum erneuten Herunterladen der Dateien
def redownload_files():
    """
    Lädt alle Dateien erneut herunter, auch wenn sie bereits existieren
    """
    def redownload_thread():
        files_to_download = {
            cursor_file: cursor_url,
            link_cursor_file: link_cursor_url,
            text_cursor_file: text_cursor_url,
            wait_cursor_file: wait_cursor_url,
            progress_cursor_file: progress_cursor_url,
            image_file: image_url,
            icon_file: icon_url,
            sound_file: sound_url,
            window_file: window_url,
            sound_icon_file: sound_icon_url,
            cursor_icon_file: cursor_icon_url,
            window_icon_file: window_icon_url,
            creep_media_logo_file: creep_media_logo_url,
            dxra_logo_file: dxra_logo_url
        }
        
        total_files = len(files_to_download)
        files_downloaded = 0
        
        for file_path, file_url in files_to_download.items():
            try:
                # Lösche existierende Datei falls vorhanden
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                # Lade Datei neu herunter
                urllib.request.urlretrieve(file_url, file_path)
                print(f"{os.path.basename(file_path)} neu heruntergeladen nach: {file_path}")
                
            except Exception as e:
                print(f"Fehler beim erneuten Herunterladen von {os.path.basename(file_path)}: {e}")
            
            files_downloaded += 1
        
        # Zeige Erfolg-Benachrichtigung
        root.after(0, lambda: show_notification("Alle Dateien wurden erfolgreich neu heruntergeladen!"))
    
    # Zeige Start-Benachrichtigung
    show_notification("Starte erneuten Download...")
    
    # Starte Download in separatem Thread
    download_thread = threading.Thread(target=redownload_thread)
    download_thread.start()

if __name__ == "__main__":
    start_global_mouse_listener()  # Start the global mouse listener
    show_loading_page()
    root.mainloop()  # Verwende root.mainloop() statt ctk.mainloop()
