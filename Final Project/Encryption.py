import numpy as np
from PIL import Image
import hashlib
import random

def circular_permutation(matrix):
    permuted_matrix = []
    for row in matrix:
        permuted_row = row[-1:] + row[:-1]  # Circular right shift
        permuted_matrix.append(permuted_row)
    return permuted_matrix

def encrypt_image(image_path, key):
    # Load and preprocess the image
    image = Image.open(image_path).convert('L')  # Convert to grayscale
    image_array = np.array(image)
    rows, cols = image_array.shape
    
    # Flatten the image array and pad if necessary
    flat_image = image_array.flatten()
    if len(flat_image) % 16 != 0:
        padding_length = 16 - (len(flat_image) % 16)
        flat_image = np.pad(flat_image, (0, padding_length), 'constant')
    
    # Key generation
    chaotic_key = chaotic_map_key_generation(3.9, 0.5, 256)
    lorenzo_key = lorenzo_map_key_generation(10, 28, 8/3, 0.1, 0.1, 0.1, 256)
    combined_key = chaotic_key[:128] + lorenzo_key[:128]
    
    # Generate S-boxes
    initial_bytes = list(range(256))
    sbox_odd = dynamic_sbox_generation(initial_bytes, chaotic_key)
    sbox_even = dynamic_sbox_generation(initial_bytes, lorenzo_key)
    
    # Encrypt the image using the enhanced AES algorithm
    encrypted_image = []
    for i in range(0, len(flat_image), 16):
        block = flat_image[i:i+16]
        for round_num in range(10):
            # Substitute bytes using dynamic S-box
            if round_num % 2 == 0:
                block = [sbox_even[b] for b in block]
            else:
                block = [sbox_odd[b] for b in block]
            # Circular permutation
            block = circular_permutation([block])[0]
            # Add round key (XOR with part of the combined key)
            block = [block[j] ^ combined_key[(i+j) % len(combined_key)] for j in range(16)]
        encrypted_image.extend(block)
    
    # Reshape and save the encrypted image
    encrypted_image_array = np.array(encrypted_image).reshape(rows, cols)
    encrypted_image = Image.fromarray(encrypted_image_array)
    encrypted_image.save('encrypted_image.png')
    print("Image encrypted and saved as 'encrypted_image.png'")
