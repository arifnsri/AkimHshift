import ctypes
import time
import threading

# Load user32.dll untuk mengakses Windows API
user32 = ctypes.windll.user32

# Definisi Virtual-Key Codes Microsoft
VK_LBUTTON = 0x01  # Klik Kiri Mouse
VK_LSHIFT = 0xA0   # Left Shift
VK_9 = 0x39        # Angka 9

# Konstanta untuk simulasi keyboard
KEYEVENTF_KEYUP = 0x0002

# Variabel Status (True = ON, False = OFF)
is_active = True
running = True

print("=========================================")
print("  WINDOWS VK-CODE: L-Click -> Left Shift ")
print("  STATUS SAAT INI: [ AKTIF / ON ]        ")
print("  Tekan angka 9 untuk ON / OFF program   ")
print("=========================================")

def get_key_state(vk_code):
    """Memeriksa apakah tombol sedang ditekan (state < 0)"""
    return user32.GetAsyncKeyState(vk_code) & 0x8000

def toggle_logic():
    global is_active, running
    last_9_state = False
    
    while running:
        # 1. Cek input tombol angka 9 untuk Toggle ON/OFF
        current_9_state = bool(get_key_state(VK_9))
        if current_9_state and not last_9_state:
            is_active = not is_active
            print("\n-----------------------------------------")
            if is_active:
                print("[STATUS] PROGRAM DIUBAH KE -> [ ON / AKTIF ]")
            else:
                print("[STATUS] PROGRAM DIUBAH KE -> [ OFF / NON-AKTIF ]")
                # Pastikan melepas Shift jika program di-matikan saat klik ditahan
                user32.keybd_event(VK_LSHIFT, 0, KEYEVENTF_KEYUP, 0)
            print("-----------------------------------------\n")
        last_9_state = current_9_state
        
        # Jeda kecil agar CPU tidak bekerja 100%
        time.sleep(0.1)

def main_loop():
    global is_active, running
    shift_pressed = False
    
    while running:
        if is_active:
            # 2. Cek apakah klik kiri mouse sedang ditekan
            if get_key_state(VK_LBUTTON):
                if not shift_pressed:
                    # Tekan Left Shift menggunakan VK Code
                    user32.keybd_event(VK_LSHIFT, 0, 0, 0)
                    print("[VK_INFO] L-Click Aktif -> VK_LSHIFT Tertekan")
                    shift_pressed = True
            else:
                if shift_pressed:
                    # Lepas Left Shift menggunakan VK Code
                    user32.keybd_event(VK_LSHIFT, 0, KEYEVENTF_KEYUP, 0)
                    print("[VK_INFO] L-Click Lepas -> VK_LSHIFT Dilepas")
                    shift_pressed = False
                    
        time.sleep(0.01) # Response time super cepat (10ms)

# Menjalankan toggle di thread terpisah agar pembacaan tombol 9 tidak mengganggu mouse
toggle_thread = threading.Thread(target=toggle_logic, daemon=True)
toggle_thread.start()

# Jalankan loop utama
try:
    main_loop()
except KeyboardInterrupt:
    running = False
