def rail_fence_encrypt(text, rails):
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1
    return "".join("".join(rail) for rail in fence)

# Example usage:
text = "HELLO WORLD"
rails = 3
encrypted = rail_fence_encrypt(text, rails)
print(f"Encrypted: {encrypted}")
