from pynput import mouse, keyboard
import time

# Inisialisasi controller keyboard untuk mensimulasikan tekanan tombol
kb_controller = keyboard.Controller()

def on_click(x, y, button, pressed):
    # Memeriksa apakah tombol yang ditekan adalah klik kiri (Button.left)
    if button == mouse.Button.left:
        if pressed:
            # Ketika klik kiri DITEKAN, tekan juga Left Shift
            kb_controller.press(keyboard.Key.shift_left)
            print("[INFO] Klik Kiri Ditekan -> Left Shift Ditekan")
        else:
            # Ketika klik kiri DILEPAS, lepas juga Left Shift
            kb_controller.release(keyboard.Key.shift_left)
            print("[INFO] Klik Kiri Dilepas -> Left Shift Dilepas")

def on_press(key):
    # Fitur tambahan: Tekan tombol ESC untuk menghentikan program
    if key == keyboard.Key.esc:
        print("[INFO] Program dihentikan.")
        return False

# Menjalankan listener untuk mouse dan keyboard secara bersamaan
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()

# Menjaga agar main thread tetap berjalan selama listener aktif
keyboard_listener.join()
mouse_listener.stop()
