#!/usr/bin/env python
"""Analyze ice_secp256k1.dll PE file structure.

Upstream Repository: https://github.com/iceland2k14/secp256k1
Para utilizar este módulo, obtenha a biblioteca compilada a partir do repositório
oficial acima e coloque-a no diretório do projeto ou em System32 / PATH do sistema.
"""
import os
import struct
import sys

UPSTREAM_REPO = "https://github.com/iceland2k14/secp256k1"

def resolve_dll_path():
    """Resolve o caminho da DLL dinamicamente sem caminhos pessoais hardcoded."""
    candidates = [
        os.environ.get("ICE_DLL_PATH", ""),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "ice_secp256k1.dll"),
        os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "ice_secp256k1.dll"),
        "ice_secp256k1.dll"
    ]
    for path in candidates:
        if path and os.path.exists(path):
            return path
    return None

dll_path = resolve_dll_path()

if not dll_path:
    print(f"[AVISO] DLL 'ice_secp256k1.dll' não encontrada localmente.")
    print(f"Para baixar ou compilar a biblioteca a partir do repositório oficial, acesse:")
    print(f"-> {UPSTREAM_REPO}")
    print("Após o download, coloque o arquivo na raiz do projeto ou em C:\\Windows\\System32.")
    sys.exit(0)

print(f"Analisando DLL em: {dll_path}")

try:
    with open(dll_path, 'rb') as f:
        data = f.read()
    size = len(data)
    print(f"=== BASIC INFO ===")
    print(f"File size: {size} bytes")

    # Check MZ signature
    if data[0] == 0x4D and data[1] == 0x5A:
        print("MZ signature: present (PE32+/PE32 file)")
    else:
        print("MZ signature: NOT present")

    # PE header at offset 60 (4 bytes, little-endian)
    pe_offset = struct.unpack_from('<I', data, 60)[0]
    print(f"PE header offset: {pe_offset}")

    # Number of sections at pe_offset + 2 (2 bytes)
    num_sections = struct.unpack_from('<H', data, pe_offset + 2)[0]
    print(f"Number of sections: {num_sections}")

    # Optional header magic at offset 96 from PE header (2 bytes)
    # For PE32: offset 96, for PE32+: offset 104... actually standard is:
    # PE32: optional header starts at pe_offset + 24, magic at pe_offset + 96+19 = 115? 
    # Let's use the standard: optional header starts at pe_offset + 24 (COFF header is 20 bytes + 4 bytes padding)
    # Actually COFF is 20 bytes, so optional header at pe_offset + 20
    # Magic is at optional_header + 0 for PE32, or +128 for PE32+? 
    # Standard: at pe_offset + 24 (after COFF), the magic is at bytes 96-97 from start of optional header
    # For PE32+: magic at bytes 120-121 from pe header start? Let me just check.
    
    # Actually, the Windows PE spec says:
    # - COFF header: 20 bytes at pe_offset
    # - Optional header starts at pe_offset + 20
    # - Magic number is the first 2 bytes of optional header
    # But in practice, many implementations put it at pe_offset + 24 (with 4 bytes padding)
    # Let's try both
    
    # Magic at pe_offset + 96 (from start of file) for PE32, or pe_offset + 104 for PE32+
    # Actually let me just read it from the correct location
    
    # Standard PE: optional header starts at pe_offset + 24 (some add 4 padding)
    # Magic at offset 96 from optional header start for PE32, 104 for PE32+
    # But we can just check: the export directory data directory entry
    
    # Data directory entries start at optional header + 96 (PE32) or + 112 (PE32+)
    # Each entry is 8 bytes (RVA + Size), there are 16 entries
    
    # Let's just print the magic we can find
    # Try reading from pe_offset + 96
    magic_at_96 = struct.unpack_from('<H', data, pe_offset + 96)[0]
    magic_at_104 = struct.unpack_from('<H', data, pe_offset + 104)[0]
    print(f"Magic at offset pe+96: {magic_at_96:#06x}")
    print(f"Magic at offset pe+104: {magic_at_104:#06x}")
    
    # 0x10b = PE32, 0x20b = PE32+
    if magic_at_96 == 0x10b or magic_at_104 == 0x20b:
        if magic_at_104 == 0x20b:
            print("Format: PE32+ (64-bit)")
        elif magic_at_96 == 0x10b:
            print("Format: PE32 (32-bit)")
    
    # Export directory - data directory entry 0
    # For PE32+: data directories start at optional header + 112
    # Optional header size for PE32+ is typically larger
    # The number of data directories is 16
    # Each is 8 bytes (4 RVA + 4 Size)
    
    # Try to find export directory RVA/size
    # In PE32+, optional header starts at pe_offset + 24 (after COFF)
    # NumberOfRvaAndSizes is at optional_header + 92 (for PE32+) or +96 (for PE32)
    # Actually: 
    # - PE32: NumberOfRvaAndSizes at optional_header + 92, data directories at +96
    # - PE32+: NumberOfRvaAndSizes at optional_header + 96, data directories at +112
    
    # Let me just try to read the export directory directly
    # The image data directories are at the end of the optional header
    # For PE32+: optional header size is in field at pe_offset + 60 (or +64?)
    
    # Get optional header size
    # For PE32+: SizeOfOptionalHeader at pe_offset + 60 (from file header start? No...)
    # Actually: file header is 20 bytes at pe_offset
    # Optional header starts at pe_offset + 20 (or +24 with padding)
    # SizeOfOptionalHeader is at pe_offset + 60... wait, that's the fields after file header
    
    # Let me use a simpler approach: just enumerate all data directories
    # They start at: pe_offset + 24 (or +28) + SizeOfOptionalHeader
    # But we don't know SizeOfOptionalHeader exactly...
    
    # Alternative: just try common offsets
    for try_offset in [pe_offset + 112, pe_offset + 96, pe_offset + 120]:
        rva = struct.unpack_from('<I', data, try_offset)[0]
        size = struct.unpack_from('<I', data, try_offset + 4)[0]
        if rva > 0 and size > 0:
            print(f"Data directory at try_offset {try_offset}: RVA={rva:#010x}, Size={size}")
    
    # String extraction (simplified)
    print(f"\n=== STRING EXTRACTION (min 4 chars) ===")
    min_len = 4
    curr_len = 0
    strings_found = []
    for i in range(size):
        b = data[i]
        if 32 <= b <= 126:
            curr_len += 1
        else:
            if curr_len >= min_len:
                start = i - curr_len
                s = data[start:start+curr_len].decode('utf-8', errors='replace')
                strings_found.append((curr_len, s))
            curr_len = 0
    if curr_len >= min_len:
        start = size - curr_len
        s = data[start:start+curr_len].decode('utf-8', errors='replace')
        strings_found.append((curr_len, s))
    
    # Sort by length descending and print top 40
    strings_found.sort(key=lambda x: x[0], reverse=True)
    for length, s in strings_found[:40]:
        print(f"  [{length}]: {s}")
    
    # Search for secp256k1 related strings
    print(f"\n=== SEARCHING FOR SECP256K1 RELATED STRINGS ===")
    search_terms = ['secp256k1', 'secp256', 'curve256', 'SECP256K1', 'SECP256', 'ECDSA', 'ecdsa', 
                    'public_key', 'PublicKey', 'point_mul', 'point_mul', 'scalar_mul', 'NIST_P',
                    '2^256', '256-bit', 'order_p', 'prime_p']
    
    # Decode full text
    try:
        text = data.decode('utf-8', errors='replace')
        for term in search_terms:
            count = text.count(term)
            if count > 0:
                # Find first occurrence position
                pos = text.find(term)
                print(f"  '{term}': found {count} times, first at position {pos}")
    except:
        print("Could not decode as UTF-8")
    
    # Also try ASCII-7 bit only range
    ascii_text = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data)
    # Simple count of likely relevant terms in the ascii portion
    for term in ['SEC', 'sec', '256', 'curve', 'ECD']:
        count = ascii_text.lower().count(term.lower())
        if count > 3:
            print(f"  '{term}' appears ~{count} times in ASCII section")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()