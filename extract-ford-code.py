import os
import struct


def extract_ford_radio_code(bin_file_path, serial_number):
    """
    Extracts a 4-digit Ford radio unlock code from the binary file.
    
    :param bin_file_path: Path to the 'radiocodes.bin' file
    :param serial_number: String like 'M123456' or 'V045621'
    """
    serial_number = serial_number.strip().upper()
    if len(serial_number) != 7 or serial_number[0] not in ['M', 'V']:
        return "Error: Invalid serial format. Must be M or V followed by 6 digits."
        
    try:
        series = serial_number[0]
        index = int(serial_number[1:])
    except ValueError:
        return "Error: Serial number must contain 6 valid digits."

    # Replicate the exact offset logic from the Flipper Zero C code
    offset = index * 2
    if series == 'V':
        offset += 2000000

    if not os.path.exists(bin_file_path):
        return f"Error: File '{bin_file_path}' not found."

    file_size = os.path.getsize(bin_file_path)
    if offset + 2 > file_size:
        return f"Error: Serial index out of file bounds. File size is {file_size} bytes."

    # Extract the 2-byte raw data chunk
    with open(bin_file_path, "rb") as f:
        f.seek(offset)
        raw_bytes = f.read(2)
        
        # Unpack little-endian 16-bit integer (<H)
        result = struct.unpack("<H", raw_bytes)[0]
        
        # Match the %04d string formatting from the C code UI
        return f"{result:04d}"

def dump_entire_bin_to_csv(bin_file_path, output_csv_path):
    with open(bin_file_path, "rb") as bin_file, open(output_csv_path, "w") as csv_file:
        csv_file.write("Serial,RadioCode\n")
        
        # Process M-Series (Indices from 0 to 999,999 -> up to offset 2,000,000)
        # Note: adjust range bounds based on your expected maximum database size
        for index in range(1000000):
            bytes_data = bin_file.read(2)
            if not bytes_data or len(bytes_data) < 2:
                break
            code = struct.unpack("<H", bytes_data)[0]
            csv_file.write(f"M{index:06d},{code:04d}\n")
            
        # Jump specifically to the start of V-Series data block
        bin_file.seek(2000000)
        for index in range(1000000):
            bytes_data = bin_file.read(2)
            if not bytes_data or len(bytes_data) < 2:
                break
            code = struct.unpack("<H", bytes_data)[0]
            csv_file.write(f"V{index:06d},{code:04d}\n")


# dump_entire_bin_to_csv("docs/fordradiocodes.bin", "extracted_codes.csv")
# extract_ford_radio_code("docs/fordradiocodes.bin", serial_number)
