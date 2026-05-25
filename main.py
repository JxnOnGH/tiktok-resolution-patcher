def find_bytes(data: bytearray, needle: bytes, start: int) -> int:
    """
    Safely search for a byte sequence in a bytearray.
    Returns the starting index if found, or -1 if not found.
    """
    try:
        return data.index(needle, start)
    except ValueError:
        return -1  


def patch_resolution(atom_name: str, data: bytearray, scale_multiplier: float):
    """
    Find all occurrences of a specified MP4/MOV atom and scale its width/height values.
    
    Assumes standard ISO Base Media File Format box structure:
    [4-byte box size (big-endian)][4-byte atom type][payload...]
    The last 8 bytes of the box are interpreted as 32-bit big-endian width and height.
    Modifies the `data` bytearray in-place.
    """
    atom_bytes = atom_name.encode('utf-8')
    start = 0

    while True:
        found = find_bytes(data, atom_bytes, start)
        if found == -1:
            break

        header_offset = found - 4
        
        box_size = (data[header_offset] << 24) | \
                   (data[header_offset + 1] << 16) | \
                   (data[header_offset + 2] << 8) | \
                   data[header_offset + 3]

        if box_size >= 84:
            w_off = header_offset + box_size - 8
            h_off = header_offset + box_size - 4

            old_w = (data[w_off] << 24) | (data[w_off + 1] << 16) | (data[w_off + 2] << 8) | data[w_off + 3]
            old_h = (data[h_off] << 24) | (data[h_off + 1] << 16) | (data[h_off + 2] << 8) | data[h_off + 3]

            new_w = int(old_w * scale_multiplier)
            new_h = int(old_h * scale_multiplier)

            data[w_off]     = (new_w >> 24) & 255
            data[w_off + 1] = (new_w >> 16) & 255
            data[w_off + 2] = (new_w >> 8)  & 255
            data[w_off + 3] =  new_w        & 255

            data[h_off]     = (new_h >> 24) & 255
            data[h_off + 1] = (new_h >> 16) & 255
            data[h_off + 2] = (new_h >> 8)  & 255
            data[h_off + 3] =  new_h        & 255

        start = found + 4
