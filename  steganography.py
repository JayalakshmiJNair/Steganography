import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
from Crypto.Cipher import AES
import base64
import os
import ttkbootstrap as tb  # Themed UI

# Global variables
image_path = ""
stego_image_path = ""

# AES Encryption
def encrypt_message(message, key):
    key = key.ljust(16)[:16]
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    padded_message = message + (16 - len(message) % 16) * " "
    encrypted_message = cipher.encrypt(padded_message.encode())
    return base64.b64encode(encrypted_message).decode()

# AES Decryption
def decrypt_message(encrypted_message, key):
    key = key.ljust(16)[:16]
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message)).decode().strip()
    return decrypted_message

# Convert text to binary
def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

# Convert binary to text
def binary_to_text(binary_data):
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

# Embed message in image
def embed_in_image(image_path, message):
    image = Image.open(image_path)
    pixels = np.array(image)
    binary_message = text_to_binary(message) + '1111111111111110'  # End marker
    
    if len(binary_message) > pixels.size:
        raise ValueError("Message is too large for this image!")
    
    index = 0
    for row in pixels:
        for pixel in row:
            if index < len(binary_message):
                pixel[-1] = (pixel[-1] & ~1) | int(binary_message[index])
                index += 1

    stego_image = Image.fromarray(pixels)
    stego_image_path = os.path.splitext(image_path)[0] + "_stego.png"
    stego_image.save(stego_image_path)
    return stego_image_path

# Extract message from image
def extract_from_image(image_path):
    image = Image.open(image_path)
    pixels = np.array(image)
    
    binary_data = ""
    for row in pixels:
        for pixel in row:
            binary_data += str(pixel[-1] & 1)
    
    extracted_data = binary_data.split('1111111111111110')[0]
    return binary_to_text(extracted_data)

# Select image for embedding
def select_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if image_path:
        messagebox.showinfo("Selected Image", f"Image selected:\n{image_path}")

# Embed message into image
def embed_message():
    if not image_path:
        messagebox.showerror("Error", "Please select an image!")
        return
    
    message = message_entry.get()
    key = key_entry.get()
    if not message or not key:
        messagebox.showerror("Error", "Message and Key are required!")
        return
    
    encrypted_message = encrypt_message(message, key)
    try:
        stego_path = embed_in_image(image_path, encrypted_message)
        messagebox.showinfo("Success", f"Message embedded successfully!\nSaved as:\n{stego_path}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Select image for extraction
def select_stego_image():
    global stego_image_path
    stego_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if stego_image_path:
        messagebox.showinfo("Selected Image", f"Stego Image selected:\n{stego_image_path}")

# Extract message
def extract_message():
    if not stego_image_path:
        messagebox.showerror("Error", "Please select an image!")
        return
    
    key = key_entry.get()
    if not key:
        messagebox.showerror("Error", "Please enter the decryption key!")
        return
    
    try:
        encrypted_message = extract_from_image(stego_image_path)
        decrypted_message = decrypt_message(encrypted_message, key)
        messagebox.showinfo("Extracted Message", f"Secret Message:\n{decrypted_message}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract message!\n{str(e)}")

# Create themed GUI
root = tb.Window(themename="superhero")  # Change theme if needed
root.title("Steganography Tool")
root.geometry("500x400")

# UI Elements
tb.Label(root, text="Secret Message:", font=("Arial", 12)).pack()
message_entry = tb.Entry(root, width=50)
message_entry.pack()

tb.Label(root, text="AES Key (16 characters):", font=("Arial", 12)).pack()
key_entry = tb.Entry(root, width=50, show="*")
key_entry.pack()

embed_button = tb.Button(root, text="Select Image & Embed Message", bootstyle="primary", command=select_image)
embed_button.pack(pady=5)

embed_message_button = tb.Button(root, text="Embed Message", bootstyle="success", command=embed_message)
embed_message_button.pack(pady=5)

stego_select_button = tb.Button(root, text="Select Stego Image", bootstyle="info", command=select_stego_image)
stego_select_button.pack(pady=5)

extract_button = tb.Button(root, text="Extract Message", bootstyle="warning", command=extract_message)
extract_button.pack(pady=5)

root.mainloop()
