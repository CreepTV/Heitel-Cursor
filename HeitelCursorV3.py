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
from pynput import mouse  # Mausereignisse erfassen

# Zielpfad für den Download
cursor_dir = os.path.join(os.path.expandvars("%USERPROFILE%"), "Documents", "HerrHeitel")
os.makedirs(cursor_dir, exist_ok=True)
cursor_file = os.path.join(cursor_dir, "HeitelCursorNormal.cur")
link_cursor_file = os.path.join(cursor_dir, "HeitelCursorLink.cur")  # Link-Cursor-Datei hinzufügen
image_file = os.path.join(cursor_dir, "HeitelCursorsLogo.png")
icon_file = os.path.join(cursor_dir, "HeitelCursorsWindowIcon.ico")  # Icon-Datei-Pfad hinzufügen
sound_file = os.path.join(cursor_dir, "HeitelHardwareSounde.mp3")  # Gemeinsame Sound-Datei für alle Buttons

# URLs der Dateien
cursor_url = "https://cloud.dxra.de/s/728PKXwP8rkxEj3/download/HeitelCursorNormal.cur"
link_cursor_url = "https://cloud.dxra.de/s/2soESG2J2P2Xt3y/download/HeitelCursorLink.cur"  # Link-Cursor-URL hinzufügen
image_url = "https://cloud.dxra.de/s/BYPieotWME2QACB/download/HeitelCursorsLogo.png"
icon_url = "https://cloud.dxra.de/s/DmESTG6g4ZZpBjK/download/HeitelCursorsWindowIcon.ico"
sound_url = "https://cloud.dxra.de/s/ieX32WHSHYjrBYy/download/HeitelHardwareSounde.mp3"

# Dateien herunterladen
def download_files(force_download=False):
    try:
        if force_download or not os.path.exists(cursor_file):
            urllib.request.urlretrieve(cursor_url, cursor_file)
            print(f"Cursor heruntergeladen nach: {cursor_file}")
        else:
            print(f"Cursor bereits vorhanden: {cursor_file}")

        if force_download or not os.path.exists(link_cursor_file):
            urllib.request.urlretrieve(link_cursor_url, link_cursor_file)
            print(f"Link-Cursor heruntergeladen nach: {link_cursor_file}")
        else:
            print(f"Link-Cursor bereits vorhanden: {link_cursor_file}")

        if force_download or not os.path.exists(image_file):
            urllib.request.urlretrieve(image_url, image_file)
            print(f"Bild heruntergeladen nach: {image_file}")
        else:
            print(f"Bild bereits vorhanden: {image_file}")

        if force_download or not os.path.exists(icon_file):
            urllib.request.urlretrieve(icon_url, icon_file)
            print(f"Icon heruntergeladen nach: {icon_file}")
        else:
            print(f"Icon bereits vorhanden: {icon_file}")

        if force_download or not os.path.exists(sound_file):
            urllib.request.urlretrieve(sound_url, sound_file)
            print(f"Sound heruntergeladen nach: {sound_file}")
        else:
            print(f"Sound bereits vorhanden: {sound_file}")
    except Exception as e:
        print(f"Fehler beim Herunterladen: {e}")

# Dateien neu herunterladen
def reload_files():
    download_files(force_download=True)
    show_notification("Dateien wurden neu heruntergeladen!")

notification_list = []  # Liste, um aktive Benachrichtigungen zu verfolgen

# Initialisiere Pygame-Mixer
pygame.mixer.init()

# Lautstärkeregler Wert
volume_value = 0.5
click_sound_enabled = True  # Variable für Klick-Sound

global click_sound_label

# Lautstärke einstellen
def set_volume(value):
    global volume_value
    volume_value = float(value) / 100
    pygame.mixer.music.set_volume(volume_value)
    volume_percentage_label.configure(text=f"{int(value)}%")  # Aktualisiere die Prozentanzeige

# Klick-Sound ein-/ausschalten
def toggle_click_sound():
    global click_sound_enabled
    click_sound_enabled = not click_sound_enabled
    click_sound_switch.configure(text="An" if click_sound_enabled else "Aus", fg_color="green" if click_sound_enabled else "red")

# Sound abspielen
def play_sound():
    if click_sound_enabled:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

# Maus-Event-Handler für Linksklick
def on_click(x, y, button, pressed):
    if button == mouse.Button.left and pressed:
        play_sound()

# Lade eine benutzerdefinierte Cursor-Datei
def set_custom_cursor():
    cursor = ctypes.windll.user32.LoadImageW(0, cursor_file, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
    link_cursor = ctypes.windll.user32.LoadImageW(0, link_cursor_file, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
    if cursor and link_cursor:
        ctypes.windll.user32.SetSystemCursor(cursor, 32512)  # IDC_ARROW
        # Versetze den Link-Cursor um 30 Pixel nach links und 40 Pixel nach unten
        ctypes.windll.user32.SetSystemCursor(link_cursor, 32649)  # IDC_HAND
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

# Cursorgröße einstellen
def set_cursor_size(value):
    cursor_size = int(value)
    cursor = ctypes.windll.user32.LoadImageW(0, cursor_file, win32con.IMAGE_CURSOR, cursor_size, cursor_size, win32con.LR_LOADFROMFILE)
    link_cursor = ctypes.windll.user32.LoadImageW(0, link_cursor_file, win32con.IMAGE_CURSOR, cursor_size, cursor_size, win32con.LR_LOADFROMFILE)
    if cursor and link_cursor:
        ctypes.windll.user32.SetSystemCursor(cursor, 32512)  # IDC_ARROW
        # Versetze den Link-Cursor um 30 Pixel nach links und 40 Pixel nach unten
        ctypes.windll.user32.SetSystemCursor(link_cursor, 32649)  # IDC_HAND
    cursor_size_percentage_label.configure(text=f"{cursor_size}px")  # Aktualisiere die Prozentanzeige

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
    
    # Tab für Einstellungen
    tab_settings = tab_control.add("Einstellungen")
    
    settings_frame = ctk.CTkFrame(tab_settings, corner_radius=10)
    settings_frame.pack(pady=10, padx=10, fill="x", anchor="w")
    
    settings_label = ctk.CTkLabel(settings_frame, text="Einstellungen:", font=("Arial", 16))
    settings_label.pack(pady=10, anchor="w", padx=10)  # Linken Abstand hinzufügen
    
    cursor_size_label = ctk.CTkLabel(settings_frame, text="Cursorgröße:", font=("Arial", 16))
    cursor_size_label.pack(pady=5, anchor="w", padx=10)
    
    cursor_size_frame = ctk.CTkFrame(settings_frame)
    cursor_size_frame.pack(pady=5, padx=10, anchor="w", fill="x")
    
    cursor_size_slider = CTkSlider(cursor_size_frame, from_=16, to=128, command=set_cursor_size)
    cursor_size_slider.set(128)  # Standardgröße des Cursors auf maximal einstellen
    cursor_size_slider.pack(side="left", fill="x", expand=True)
    
    global cursor_size_percentage_label
    cursor_size_percentage_label = ctk.CTkLabel(cursor_size_frame, text="128px", font=("Arial", 12))
    cursor_size_percentage_label.pack(side="left", padx=10)
    
    # Button zum Neuladen der Dateien
    reload_button = ctk.CTkButton(settings_frame, text="Dateien neu herunterladen", command=reload_files)
    reload_button.pack(pady=10, anchor="w", padx=10)  # Linken Abstand hinzufügen
    
    # Tab für Sound-Einstellungen
    tab_sound = tab_control.add("Sound")
    
    volume_label = ctk.CTkLabel(tab_sound, text="Lautstärke:", font=("Arial", 16))
    volume_label.pack(pady=5, anchor="w", padx=10)  # Abstand verringert
    
    # Frame für Lautstärkeregler und Prozentanzeige
    volume_frame = ctk.CTkFrame(tab_sound)
    volume_frame.pack(pady=5, padx=10, anchor="w", fill="x")  # Abstand verringert
    
    # Ersetze den Standard-Lautstärkeregler durch CTkSlider
    volume_slider = CTkSlider(volume_frame, from_=0, to=100, command=set_volume, button_color="#cc7000")
    volume_slider.set(volume_value * 100)  # Setze die anfängliche Lautstärke auf 50%
    volume_slider.pack(side="left", fill="x", expand=True)
    
    # Prozentanzeige hinzufügen
    global volume_percentage_label
    volume_percentage_label = ctk.CTkLabel(volume_frame, text=f"{int(volume_value * 100)}%", font=("Arial", 12))
    volume_percentage_label.pack(side="left", padx=10)
    
    # Frame für Klick-Sound-Einstellungen
    click_sound_frame = ctk.CTkFrame(tab_sound)
    click_sound_frame.pack(pady=10, padx=10, anchor="w", fill="x")
    
    click_sound_label = ctk.CTkLabel(click_sound_frame, text="Klick-Sound:", font=("Arial", 16))
    click_sound_label.pack(side="left", padx=10)
    
    global click_sound_switch
    click_sound_switch = ctk.CTkSwitch(click_sound_frame, text="An" if click_sound_enabled else "Aus", command=toggle_click_sound)
    click_sound_switch.configure(fg_color="green" if click_sound_enabled else "red")
    click_sound_switch.pack(side="left", padx=10)
    
    # Binde das Linksklick-Ereignis an die Funktion
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    
    # Leiste unten für Beenden-Button
    bottom_frame = ctk.CTkFrame(root, height=40, corner_radius=10)
    bottom_frame.pack(fill="x", side="bottom", padx=10, pady=5)
    
    button_exit = ctk.CTkButton(bottom_frame, text="Beenden", command=exit_program, fg_color="red", hover_color="darkred")
    button_exit.pack(pady=5, padx=10, anchor="e")  # Positioniere den Button unten rechts
    
    root.mainloop()

if __name__ == "__main__":
    print("Überprüfe und lade Dateien herunter...")
    download_files()
    create_gui()
