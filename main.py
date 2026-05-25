import argparse
import os
import sys

def find_bytes(data: bytearray, needle: bytes, start: int) -> int:
    """Helper function to replicate JavaScript's findBytes logic."""
    try:
        return data.index(needle, start)
    except ValueError:
        return -1

def patch_resolution(atom_name: str, data: bytearray, scale_multiplier: float) -> int:
    """Patches the resolution inside the specified MP4/QuickTime atom."""
    atom_bytes = atom_name.encode('utf-8')
    start = 0
    match_count = 0

    while True:
        found = find_bytes(data, atom_bytes, start)
        if found == -1:
            break

        header_offset = found - 4
        
        # Read 32-bit integer box size (Big Endian)
        box_size = (data[header_offset] << 24) | \
                   (data[header_offset + 1] << 16) | \
                   (data[header_offset + 2] << 8) | \
                   data[header_offset + 3]

        if box_size >= 84:
            w_off = header_offset + box_size - 8
            h_off = header_offset + box_size - 4

            # Read old dimensions
            old_w = (data[w_off] << 24) | (data[w_off + 1] << 16) | (data[w_off + 2] << 8) | data[w_off + 3]
            old_h = (data[h_off] << 24) | (data[h_off + 1] << 16) | (data[h_off + 2] << 8) | data[h_off + 3]

            # Calculate new dimensions
            new_w = int(old_w * scale_multiplier)
            new_h = int(old_h * scale_multiplier)

            # Write new width
            data[w_off]     = (new_w >> 24) & 255
            data[w_off + 1] = (new_w >> 16) & 255
            data[w_off + 2] = (new_w >> 8)  & 255
            data[w_off + 3] =  new_w        & 255

            # Write new height
            data[h_off]     = (new_h >> 24) & 255
            data[h_off + 1] = (new_h >> 16) & 255
            data[h_off + 2] = (new_h >> 8)  & 255
            data[h_off + 3] =  new_h        & 255
            
            match_count += 1

        start = found + 4
        
    return match_count

def main():
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description="Patch MP4/MOV atom resolutions by a scale factor.")
    
    parser.add_argument("-i", "--input", required=True, help="Path to the input video file")
    parser.add_argument("-o", "--output", required=True, help="Path to save the modified video file")
    parser.add_argument("-a", "--atom", default="tkhd", help="Atom name to target (default: tkhd)")
    parser.add_argument("-s", "--scale", type=float, required=True, help="Scale multiplier (e.g., 2.0 to double size, 0.5 to halve)")

    args = parser.parse_args()

    # Verify input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"Reading '{args.input}'...")
    try:
        with open(args.input, "rb") as f:
            video_data = bytearray(f.read())
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Searching for '{args.atom}' atoms and applying scale factor {args.scale}x...")
    patched_atoms = patch_resolution(args.atom, video_data, args.scale)

    if patched_atoms == 0:
        print("Warning: No valid atoms found to modify. File remains unchanged.")
    else:
        print(f"Successfully modified {patched_atoms} atom(s).")

    print(f"Writing output to '{args.output}'...")
    try:
        with open(args.output, "wb") as f:
            f.write(video_data)
        print("Done!")
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
