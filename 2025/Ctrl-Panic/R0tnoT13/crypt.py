from binascii import unhexlify
S = unhexlify("3721d4ef20940a4e78a4ab209a07acbd")
ct = unhexlify("477eb79b46ef667f16ddd94ca933c7c0")

pt = bytes(a ^ b for a, b in zip(S, ct))

print(pt)
print(pt.decode())
