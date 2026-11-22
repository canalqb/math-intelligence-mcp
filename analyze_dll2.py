#!/usr/bin/env python
"""Deep analysis of ice_secp256k1.dll - focus on secp256k1 strings."""
import struct
import sys

dll_path = r'C:\Users\Qb\Desktop\sequenciadores\lp\mcp\ice_secp256k1.dll'

with open(dll_path, 'rb') as f:
    data = f.read()

size = len(data)
print(f"File size: {size} bytes")

# Find all positions of 'secp256k1'
term = b'secp256k1'
pos = 0
positions = []
while True:
    pos = data.find(term, pos)
    if pos == -1:
        break
    positions.append(pos)
    pos += 1  # move past this match

print(f"'\''secp256k1'\'' found {len(positions)} times")
for p in positions:
    # Print 80 bytes before and 80 after
    start = max(0, p - 80)
    end = min(size, p + len(term) + 80)
    chunk = data[start:end]
    # Print as hex + ASCII
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    # Also try to decode as much as possible
    print(f"\n  Position {p} (0x{p:x}):")
    print(f"  Hex: {hex_str}")
    # Decode readable portion
    try:
        readable = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        print(f"  ASCII: {readable}")
    except:
        print("  ASCII: (decode error)")

# Also find 'secp256' (without the 'k1')
term2 = b'secp256'
pos2 = 0
positions2 = []
while True:
    pos2 = data.find(term2, pos2)
    if pos2 == -1:
        break
    positions2.append(pos2)
    pos2 += 1

print(f"\n'\''secp256'\'' found {len(positions2)} times (overlaps with secp256k1)")
for p in positions2:
    start = max(0, p - 40)
    end = min(size, p + len(term2) + 40)
    chunk = data[start:end]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    try:
        readable = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        print(f"  Position {p} (0x{p:x}): ASCII: {readable}")
    except:
        print(f"  Position {p}: (decode error)")

# Find 'point_mul'
term3 = b'point_mul'
pos3 = 0
positions3 = []
while True:
    pos3 = data.find(term3, pos3)
    if pos3 == -1:
        break
    positions3.append(pos3)
    pos3 += 1

print(f"\n'\''point_mul'\'' found {len(positions3)} times")
for p in positions3:
    start = max(0, p - 60)
    end = min(size, p + len(term3) + 60)
    chunk = data[start:end]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    try:
        readable = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        print(f"  Position {p} (0x{p:x}): ASCII: {readable}")
    except:
        print(f"  Position {p}: (decode error)")

# Find 'scalar_mul'
term4 = b'scalar_mul'
pos4 = 0
positions4 = []
while True:
    pos4 = data.find(term4, pos4)
    if pos4 == -1:
        break
    positions4.append(pos4)
    pos4 += 1

print(f"\n'\''scalar_mul'\'' found {len(positions4)} times")
for p in positions4:
    start = max(0, p - 60)
    end = min(size, p + len(term4) + 60)
    chunk = data[start:end]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    try:
        readable = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        print(f"  Position {p} (0x{p:x}): ASCII: {readable}")
    except:
        print(f"  Position {p}: (decode error)")

# Also check for 'curve25519' or 'nistp'
for term5 in [b'curve25519', b'Curve25519', b'nistp256', b'NIST_P256', b'prime256v1', b'P-256']:
    pos5 = data.find(term5)
    if pos5 != -1:
        print(f"\nFound '{term5.decode()}': position {pos5}")
        start = max(0, pos5 - 40)
        end = min(size, pos5 + len(term5) + 40)
        chunk = data[start:end]
        try:
            readable = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
            print(f"  ASCII: {readable}")
        except:
            pass

# Check for 'verify' 'sign' 'context' etc near the secp256k1 area
print(f"\n=== CONTEXT AROUND secp256k1 POSITION 416781 ===")
p = 416781
start = max(0, p - 120)
end = min(size, p + 120)
chunk = data[start:end]
# Print as hex with ASCII
print(f"Bytes {start:#x}-{end:#x} (len {len(chunk)}):")
for i in range(0, len(chunk), 16):
    hex_part = ' '.join(f'{chunk[i+j]:02x}' for j in range(min(16, len(chunk)-i)))
    ascii_part = ''.join(chr(chunk[i+j]) if 32 <= chunk[i+j] <= 126 else '.' for j in range(min(16, len(chunk)-i)))
    print(f"  {start+i//16*16:08x}: {hex_part:<48s}  {ascii_part}")

# Also check around point_mul position 467871
print(f"\n=== CONTEXT AROUND point_mul POSITION 467871 ===")
p = 467871
start = max(0, p - 120)
end = min(size, p + 120)
chunk = data[start:end]
print(f"Bytes {start:#x}-{end:#x} (len {len(chunk)}):")
for i in range(0, len(chunk), 16):
    hex_part = ' '.join(f'{chunk[i+j]:02x}' for j in range(min(16, len(chunk)-i)))
    ascii_part = ''.join(chr(chunk[i+j]) if 32 <= chunk[i+j] <= 126 else '.' for j in range(min(16, len(chunk)-i)))
    print(f"  {start+i//16*16:08x}: {hex_part:<48s}  {ascii_part}")