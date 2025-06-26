# Chaotic map-based key generation
def chaotic_map_key_generation(p, x, n):
    key = []
    for _ in range(n):
        x = (p * x * (1 - x)) % 1
        binary_string = format(int(x * 256), '08b')
        key.append(int(binary_string, 2))
    return key

# 3D Lorenzo function for key generation
def lorenzo_map_key_generation(p, r, t, x0, y0, z0, n):
    key = []
    for _ in range(n):
        x1 = p * (x0 - y0)
        y1 = (x0 * z0) + (r * x0) - y0
        z1 = (x0 * y0) + (t * z0)
        key.append((x1, y1, z1))
        x0, y0, z0 = x1, y1, z1
    return key
