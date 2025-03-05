# Steganography Tool with AES Encryption

This Python application provides a simple way to hide encrypted messages inside images using steganography techniques. It utilizes AES encryption for securing messages and the Least Significant Bit (LSB) method for embedding data in image pixels.

## Features
- Encrypts messages using AES encryption before embedding.
- Uses the LSB method to hide messages inside image pixels.
- Allows extracting and decrypting messages from stego images.
- User-friendly GUI built with Tkinter and ttkbootstrap.

## Prerequisites
Ensure you have Python installed on your system along with the required dependencies.

### Required Libraries:
You can install them using:
```sh
pip install pillow pycryptodome numpy ttkbootstrap
```

## How to Use

### 1. Embedding a Message
- Run the script: `python steganography_tool.py`
- Enter the secret message and a 16-character AES key.
- Click "Select Image & Embed Message" to choose an image.
- Click "Embed Message" to embed and save the stego image.

### 2. Extracting a Message
- Click "Select Stego Image" to load the modified image.
- Enter the AES key used during embedding.
- Click "Extract Message" to retrieve and decrypt the hidden message.

## File Structure
```
/Steganography-Tool
│── steganography_tool.py  # Main application script
│── README.md              # Project documentation
│── requirements.txt       # Required dependencies
```

## Notes
- The AES key must be exactly 16 characters for encryption/decryption.
- The message is padded to fit encryption requirements.
- Images with low resolution might not be able to hold large messages.

## License
This project is open-source and available under the MIT License.
