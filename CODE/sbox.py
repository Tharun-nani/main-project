def dynamic_sbox_generation(initial_bytes, chaotic_values):
    sbox = []
    for i in range(256):
        value = initial_bytes[i % len(initial_bytes)] ^ chaotic_values[i % len(chaotic_values)]
        sbox.append(value)
    return sbox

def circular_permutation(matrix):
    permuted_matrix = []
    for row in matrix:
        permuted_row = row[-1:] + row[:-1]  # Circular right shift
        permuted_matrix.append(permuted_row)
    return permuted_matrix
