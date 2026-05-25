from pynput import mouse, keyboard

# Inisialisasi controller keyboard
kb_controller = keyboard.Controller()

# Variabel status (True = Aktif, False = Nonaktif)
is_active = True

print("=========================================")
print("  PROGRAM TOGGLE: L-Click -> Left Shift  ")
print("  STATUS SAAT INI: [ AKTIF / ON ]        ")
print("  Tekan angka 9 untuk ON / OFF program   ")
print("=========================================")

def on_click(x, y, button, pressed):
    global is_active
    
    # Script hanya akan berjalan jika status is_active = True (ON)
    if is_active and button == mouse.Button.left:
        if pressed:
            kb_controller.press(keyboard.Key.shift_left)
            print("[INFO] Klik Kiri -> Left Shift [TERTEKAN]")
        else:
            kb_controller.release(keyboard.Key.shift_left)
            print("[INFO] Klik Kiri -> Left Shift [DILEPAS]")

def on_press(key):
    global is_active
    try:
        # Memeriksa apakah user menekan tombol angka 9
        if key.char == '9':
            # Membalikkan status (Jika True jadi False, jika False jadi True)
            is_active = not is_active
            
            print("\n-----------------------------------------")
            if is_active:
                print("[STATUS] PROGRAM DIUBAH KE -> [ ON / AKTIF ]")
                print("[INFO] Klik kiri akan otomatis menekan Shift.")
            else:
                print("[STATUS] PROGRAM DIUBAH KE -> [ OFF / NON-AKTIF ]")
                print("[INFO] Klik kiri kembali normal (Shift mati).")
            print("-----------------------------------------\n")
            
    except AttributeError:
        # Mengabaikan tombol spesial (Ctrl, Alt, dll) agar tidak error
        pass

# Menjalankan listener mouse dan keyboard
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()

# Menjaga CMD tetap terbuka tanpa menutup program
keyboard_listener.join()
