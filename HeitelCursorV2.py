import ctypes
import win32gui
import win32con
import os
import urllib.request
import customtkinter as ctk
from tkinter import Toplevel, Label, Scale, HORIZONTAL
from customtkinter import CTkImage, CTkSlider  # CTkSlider importieren
from PIL import Image, ImageTk
import pygame  # Sound-Abspielfunktion importieren

# Zielpfad für den Download
cursor_dir = os.path.join(os.path.expandvars("%USERPROFILE%"), "Documents", "HerrHeitel")
os.makedirs(cursor_dir, exist_ok=True)
cursor_file = os.path.join(cursor_dir, "HeitelCursorNormal.cur")
image_file = os.path.join(cursor_dir, "HeitelCursorsLogo.png")
icon_file = os.path.join(cursor_dir, "HeitelCursorsWindowIcon.ico")  # Icon-Datei-Pfad hinzufügen
sound_file = os.path.join(cursor_dir, "HeitelHardwareSounde.mp3")  # Gemeinsame Sound-Datei für alle Buttons

# URLs der Dateien
cursor_url = "https://cloud.dxra.de/s/728PKXwP8rkxEj3/download/HeitelCursorNormal.cur"
image_url = "https://cloud.dxra.de/s/BYPieotWME2QACB/download/HeitelCursorsLogo.png"
icon_url = "https://cloud.dxra.de/s/DmESTG6g4ZZpBjK/download/HeitelCursorsWindowIcon.ico"
sound_url = "https://cloud.dxra.de/s/ieX32WHSHYjrBYy/download/HeitelHardwareSounde.mp3"

# Dateien herunterladen
def download_files():
    try:
        urllib.request.urlretrieve(cursor_url, cursor_file)
        print(f"Cursor heruntergeladen nach: {cursor_file}")
        urllib.request.urlretrieve(image_url, image_file)
        print(f"Bild heruntergeladen nach: {image_file}")
        urllib.request.urlretrieve(icon_url, icon_file)
        print(f"Icon heruntergeladen nach: {icon_file}")
        urllib.request.urlretrieve(sound_url, sound_file)
        print(f"Sound heruntergeladen nach: {sound_file}")
    except Exception as e:
        print(f"Fehler beim Herunterladen: {e}")

notification_list = []  # Liste, um aktive Benachrichtigungen zu verfolgen

# Initialisiere Pygame-Mixer
pygame.mixer.init()

# Lautstärkeregler Wert
volume_value = 0.5

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

# Lade eine benutzerdefinierte Cursor-Datei
def set_custom_cursor():
    cursor = ctypes.windll.user32.LoadImageW(0, cursor_file, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
    if cursor:
        ctypes.windll.user32.SetSystemCursor(cursor, 32512)  # IDC_ARROW
        show_notification("Heitel Cursor wurde gesetzt!")
        play_sound()
    else:
        show_notification("Fehler beim Laden des Cursors")
        play_sound()

# Setzt den Standard-Cursor zurück
def reset_cursor():
    ctypes.windll.user32.SystemParametersInfoW(87, 0, None, 0)
    show_notification("Standard-Cursor wiederhergestellt!")
    play_sound()

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
    if os.path.exists(image_file):
        img = Image.open(image_file)
        img = img.resize((32, 32))  # Größe des Bildes anpassen
        photo = ImageTk.PhotoImage(img)
        image_label = Label(content_frame, image=photo, bg='black')
        image_label.image = photo  # Referenz speichern
        image_label.pack(side='left', padx=5)

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

# GUI erstellen
def create_gui():
    ctk.set_appearance_mode("System")  # "Dark", "Light", or "System"
    ctk.set_default_color_theme("blue")
    
    global root
    root = ctk.CTk()
    root.title("Heitel Cursors")
    root.geometry("400x400")  # Festgelegte Fenstergröße
    root.resizable(False, False)  # Fenstergröße nicht veränderbar
    
    # Setze das Fenster-Icon
    root.iconbitmap(icon_file)  # Icon für das Fenster setzen
    
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Bild einfügen
    if (os.path.exists(image_file)):
        img = CTkImage(Image.open(image_file), size=(84, 84))
        image_label = ctk.CTkLabel(frame, image=img, text="")
        image_label.pack(anchor="ne", padx=10, pady=5)
    
    # Tab-Steuerung hinzufügen
    tab_control = ctk.CTkTabview(frame)
    tab_control.pack(pady=10, padx=0, fill="both", expand=True)  # Tabs weiter nach links verschieben
    
    # Tab für Cursor-Einstellungen
    tab_cursor = tab_control.add("Cursor")
    
    cursor_frame = ctk.CTkFrame(tab_cursor, corner_radius=10)
    cursor_frame.pack(pady=10, padx=10, fill="x", anchor="w")
    
    label = ctk.CTkLabel(cursor_frame, text="Wähle einen Cursor:", font=("Arial", 16))
    label.pack(pady=10, anchor="w", padx=10)  # Linken Abstand hinzufügen
    
    button_set = ctk.CTkButton(cursor_frame, text="Heitel Cursor setzen", command=set_custom_cursor, fg_color="#cc7000", hover_color="#994c00")
    button_set.pack(pady=5, anchor="w", padx=10)  # Linken Abstand hinzufügen
    
    button_reset = ctk.CTkButton(cursor_frame, text="Standard-Cursor wiederherstellen", command=reset_cursor)
    button_reset.pack(pady=5, anchor="w", padx=10)  # Linken Abstand hinzufügen
    
    # Tab für Sound-Einstellungen
    tab_sound = tab_control.add("Sound")
    
    volume_label = ctk.CTkLabel(tab_sound, text="Lautstärke:", font=("Arial", 16))
    volume_label.pack(pady=10, anchor="w", padx=10)
    
    # Ersetze den Standard-Lautstärkeregler durch CTkSlider
    volume_slider = CTkSlider(tab_sound, from_=0, to=100, command=set_volume)
    volume_slider.set(volume_value * 100)  # Setze die anfängliche Lautstärke auf 50%
    volume_slider.pack(pady=10, padx=10, anchor="w")
    
    # Prozentanzeige hinzufügen
    global volume_percentage_label
    volume_percentage_label = ctk.CTkLabel(tab_sound, text=f"{int(volume_value * 100)}%", font=("Arial", 12))
    volume_percentage_label.pack(pady=10, anchor="w", padx=10)
    
    # Leiste unten für Beenden-Button
    bottom_frame = ctk.CTkFrame(root, height=40, corner_radius=10)
    bottom_frame.pack(fill="x", side="bottom", padx=10, pady=5)
    
    button_exit = ctk.CTkButton(bottom_frame, text="Beenden", command=exit_program, fg_color="red", hover_color="darkred")
    button_exit.pack(pady=5, padx=10, anchor="e")  # Positioniere den Button unten rechts
    
    root.mainloop()

if __name__ == "__main__":
    print("Lade Dateien herunter...")
    download_files()
    create_gui()
