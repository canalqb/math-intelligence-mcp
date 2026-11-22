$dllPath = "C:\Users\Qb\Desktop\sequenciadores\lp\mcp\ice_secp256k1.dll"
$raw = [system.io.file]::ReadAllBytes($dllPath)

Write-Output "=== BASIC INFO ==="
Write-Output "File size: $($raw.Length) bytes"

# Check MZ signature (PE file)
$mz = [int]($raw[0]) + ([int]($raw[1]) * 256)
Write-Output "MZ signature value: $mz"

if ($raw[0] -eq 0x4D -and $raw[1] -eq 0x5A) {
    Write-Output "Format: PE32+ (PE file with MZ signature)"
} else {
    Write-Output "Format: NOT a PE file"
}

# Get PE header info
# COFF header at offset 60 (4 bytes for PE offset)
$peOffset = [int]($raw[60]) + ([int]($raw[61]) * 256) + ([int]($raw[62]) * 65536) + ([int]($raw[63]) * 16777216)
Write-Output "PE header offset: $peOffset"

# Optional header starts at peOffset + 24 (for 32-bit) or peOffset + 24 (for 64-bit, after COFF)
# For 64-bit PE, the COFF header is still at the same place, but NumberOfSections is at peOffset+4
$numSections = [int]($raw[$peOffset+4]) + ([int]($raw[$peOffset+5]) * 256) + ([int]($raw[$peOffset+6]) * 65536) + ([int]($raw[$peOffset+7]) * 16777216)
Write-Output "Number of sections: $numSections"

# Magic number at optional header offset 60 (2 bytes after standard fields)
$optionalHeaderStart = $peOffset + 24
$magic = [int]($raw[$optionalHeaderStart+16]) + ([int]($raw[$optionalHeaderStart+17]) * 256)
Write-Output "Magic number: $magic (0x10b = 32-bit, 0x20b = 64-bit)"

# Export directory - need to find it via data directories
# Data directory entry 0 is at optional header + 96 (for 64-bit) or +80 (for 32-bit)
$exportDirRva = [int]($raw[$optionalHeaderStart+92]) + ([int]($raw[$optionalHeaderStart+93]) * 256) + ([int]($raw[$optionalHeaderStart+94]) * 65536) + ([int]($raw[$optionalHeaderStart+95]) * 16777216)
Write-Output "Export directory RVA: $exportDirRva"

# Section table starts at peOffset + 28 (after COFF header)
# Each section is 40 bytes
# Find which section contains the RVA
$sectionIdx = 0
while ($sectionIdx -lt $numSections) {
    $secStart = $peOffset + 28 + ($sectionIdx * 40)
    $secVaddr = [int]($raw[$secStart]) + ([int]($raw[$secStart+1]) * 256) + ([int]($raw[$secStart+2]) * 65536) + ([int]($raw[$secStart+3]) * 16777216)
    $secVsize = [int]($raw[$secStart+8]) + ([int]($raw[$secStart+9]) * 256) + ([int]($raw[$secStart+10]) * 65536) + ([int]($raw[$secStart+11]) * 16777216)
    $secPtrRaw = [int]($raw[$secStart+24]) + ([int]($raw[$secStart+25]) * 256) + ([int]($raw[$secStart+26]) * 65536) + ([int]($raw[$secStart+27]) * 16777216)
    $secPtrRawSize = [int]($raw[$secStart+32]) + ([int]($raw[$secStart+33]) * 256) + ([int]($raw[$secStart+34]) * 65536) + ([int]($raw[$secStart+35]) * 16777216)
    
    if ($exportDirRva -ge $secVaddr -and $exportDirRva -lt $secVaddr + $secVsize) {
        $exportPtrRaw = $secPtrRaw + ($exportDirRva - $secVaddr)
        Write-Output "Export directory found in section $sectionIdx (raw offset: $exportPtrRaw)"
        break
    }
    $sectionIdx++
}

# Try using command-line tools if available
Write-Output "`n=== TRYING DUMPBIN ==="
try {
    $result = powershell -noprofile -command "dumpbin /exports `"$dllPath`" 2>&1" 2>&1
    Write-Output "dumpbin output length: $($result.Length)"
    if ($result) {
        # Show first 30 lines
        $lines = $result -split "`n" | where-object { $_ -ne "" } | select-object -first 30
        Write-Output "First 30 export lines:"
        $lines | ForEach-Object { Write-Output "  $_" }
    }
} catch {
    Write-Output "dumpbin not available or error: $_"
}

# Try using powershell to read the export directory
Write-Output "`n=== USING .NET TO EXAMINE EXPORTS ==="
$asm = [system.Reflection.Assembly]::LoadFile($dllPath)
$types = $asm.GetExportedTypes()
Write-Output "Exported types count: $($types.Length)"
$types | ForEach-Object { Write-Output "  Type: $($_.Name)" }

Write-Output "`n=== DONE ==="