import ctypes
import time
import threading

# Mengatur struktur data untuk SendInput (Hardware Level)
LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(ctypes.c_ulong)
WORD = ctypes.c_ushort

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", WORD),
        ("wScan", WORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]
    _fields_ = [("type", DWORD), ("_input", _INPUT)]

# Konstanta Windows API
INPUT_KEYBOARD = 1
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002

# Scancode untuk Left Shift (Lebih aman dari VK Code untuk game)
SCAN_LSHIFT = 0x2A 

# Virtual-Key Codes untuk deteksi
VK_LBUTTON = 0x01
VK_9 = 0x39

user32 = ctypes.windll.user32
is_active = True
running = True

print("=========================================")
print("  ROBLOX HARDWARE INPUT (SendInput)      ")
print("  STATUS SAAT INI: [ AKTIF / ON ]        ")
print("  Tekan angka 9 untuk ON / OFF program   ")
print("=========================================")

def press_shift_hardware():
    """Mengirim sinyal tekan Shift tingkat hardware"""
    extra = ctypes.c_ulong(0)
    ii_ = INPUT._INPUT()
    ii_.ki = KEYBDINPUT(0, SCAN_LSHIFT, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
    x = INPUT(INPUT_KEYBOARD, ii_)
    user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def release_shift_hardware():
    """Mengirim sinyal lepas Shift tingkat hardware"""
    extra = ctypes.c_ulong(0)
    ii_ = INPUT._INPUT()
    ii_.ki = KEYBDINPUT(0, SCAN_LSHIFT, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
    x = INPUT(INPUT_KEYBOARD, ii_)
    user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def get_key_state(vk_code):
    return user32.GetAsyncKeyState(vk_code) & 0x8000

def toggle_logic():
    global is_active, running
    last_9_state = False
    while running:
        current_9_state = bool(get_key_state(VK_9))
        if current_9_state and not last_9_state:
            is_active = not is_active
            print("\n-----------------------------------------")
            if is_active:
                print("[STATUS] PROGRAM -> [ ON / AKTIF ]")
            else:
                print("[STATUS] PROGRAM -> [ OFF / NON-AKTIF ]")
                release_shift_hardware()
            print("-----------------------------------------\n")
        last_9_state = current_9_state
        time.sleep(0.1)

def main_loop():
    global is_active, running
    shift_pressed = False
    try:
        while running:
            if is_active:
                if get_key_state(VK_LBUTTON):
                    if not shift_pressed:
                        press_shift_hardware()
                        shift_pressed = True
                else:
                    if shift_pressed:
                        release_shift_hardware()
                        shift_pressed = False
            time.sleep(0.01)
    finally:
        release_shift_hardware()

toggle_thread = threading.Thread(target=toggle_logic, daemon=True)
toggle_thread.start()

try:
    main_loop()
except KeyboardInterrupt:
    running = False
