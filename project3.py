import os
import math
import struct
import wave
import time
import colorsys
from PIL import Image
import pygame
from tkinter import Tk, filedialog

SAMPLE_RATE = 44100
SAMPLE_WIDTH = 2
CHANNELS = 1

def color_to_freq_and_volume(r, g, b):
    rn, gn, bn = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(rn, gn, bn)

    freq = (r / 255) * 880 + (g / 255) * 440 + (b / 255) * 220
    freq *= (0.8 + 0.6 * v)
    volume = max(0.1, v)

    return freq, volume

def make_sine_wave(freq, duration, volume=0.5):
    frames = bytearray()
    total_samples = int(SAMPLE_RATE * duration)

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        sample = math.sin(2 * math.pi * freq * t)
        sample = int(sample * volume * 32767)
        frames += struct.pack("<h", sample)

    return bytes(frames)

def create_wav(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((48, 48))

    audio_data = bytearray()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            freq, vol = color_to_freq_and_volume(r, g, b)
            audio_data += make_sine_wave(freq, 0.02, vol)

    wav_path = "melody.wav"

    with wave.open(wav_path, "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_data)

    return wav_path

def main():
    print("=== Synesthetic Composer ===")
    print("Select an image file from the window...")

    # Open a file selection dialog
    root = Tk()
    root.withdraw()  # hide default window

    image_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )

    root.destroy()

    if not image_path:
        print("\n❌ No file selected.")
        return

    print("\n✅ Selected:", image_path)

    print("Processing and generating melody...")
    wav_file = create_wav(image_path)

    print("🎵 Playing melody...")
    pygame.mixer.init()
    sound = pygame.mixer.Sound(wav_file)
    sound.play()
    time.sleep(sound.get_length())
    pygame.mixer.quit()

    print("\n✅ Done! Melody generated from your image.")

if __name__ == "__main__":
    main()

