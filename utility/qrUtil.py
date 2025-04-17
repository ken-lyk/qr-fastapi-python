import base64
import io
from PIL import Image # Pillow library for image handling

try:
    from pyzbar import pyzbar # For QR code decoding
except ImportError:
    print("-------------------------------------------------------")
    print("ERROR: 'pyzbar' library found, but failed to import.")
    print("This usually means the underlying 'ZBar' library is missing or not configured correctly.")
    print("\nPlease ensure ZBar is installed on your system:")
    print("  - Debian/Ubuntu: sudo apt-get install zbar-tools libzbar-dev")
    print("  - macOS: brew install zbar")
    print("  - Windows: Download ZBar DLLs/binaries and add to PATH (check pyzbar docs)")
    print("  - Fedora: sudo dnf install zbar-devel")
    print("-------------------------------------------------------")
    exit(1) # Exit if the core dependency isn't working

def decode_qr_from_image_object(img: Image.Image) -> list[str]:
    """
    Decodes QR codes found within a given Pillow Image object.

    Args:
        img: A PIL.Image.Image object.

    Returns:
        A list of strings, where each string is the decoded data from a found QR code.
        Returns an empty list if no QR codes are found or if an error occurs.
    """
    decoded_values = []
    try:
        # pyzbar.decode can find multiple barcodes/QR codes in one image
        decoded_objects = pyzbar.decode(img)

        if not decoded_objects:
            # print("No QR codes found in the image.") # Optional message
            return []

        for obj in decoded_objects:
            # Check if the decoded object is a QR Code
            if obj.type == 'QRCODE':
                # Data is returned as bytes, decode to UTF-8 string
                qr_data = obj.data.decode('utf-8')
                decoded_values.append(qr_data)
                # print(f"Found QR Code. Type: {obj.type}, Data: '{qr_data}'") # Debugging

    except Exception as e:
        print(f"An error occurred during QR decoding: {e}")
        return [] # Return empty list on error

    return decoded_values

def decode_qr_from_file(file_path: str) -> list[str]:
    """
    Opens an image file, decodes any QR codes found, and returns their values.

    Args:
        file_path: The path to the image file (e.g., 'my_qrcode.png').

    Returns:
        A list of decoded QR code data strings, or an empty list on failure/not found.
    """
    try:
        # Open the image file using Pillow
        img = Image.open(file_path)
        return decode_qr_from_image_object(img)
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return []
    except Exception as e:
        # Catches potential errors during file opening or image processing
        print(f"Error opening or processing image file '{file_path}': {e}")
        return []
    
def decode_qr_from_file_content(contents: bytes) -> list[str]:
    """
    Opens an image file, decodes any QR codes found, and returns their values.

    Args:
        file_path: The path to the image file (e.g., 'my_qrcode.png').

    Returns:
        A list of decoded QR code data strings, or an empty list on failure/not found.
    """
    try:
        # Open the image file using Pillow
        image_buffer = io.BytesIO(contents)
        img = Image.open(image_buffer)
        return decode_qr_from_image_object(img)
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return []
    except Exception as e:
        # Catches potential errors during file opening or image processing
        print(f"Error opening or processing image file '{file_path}': {e}")
        return []

def decode_qr_from_base64(base64_string: str) -> list[str]:
    """
    Decodes a Base64 encoded image string, decodes any QR codes found,
    and returns their values.

    Args:
        base64_string: The Base64 encoded string of the image data.

    Returns:
        A list of decoded QR code data strings, or an empty list on failure/not found.
    """
    try:
        # Decode the Base64 string into bytes
        image_bytes = base64.b64decode(base64_string)
        # Create an in-memory bytes buffer from the decoded bytes
        image_buffer = io.BytesIO(image_bytes)
        # Open the image from the buffer using Pillow
        img = Image.open(image_buffer)

        return decode_qr_from_image_object(img)

    except base64.binascii.Error as e:
        # Error specific to base64 decoding
        print(f"Error: Invalid Base64 string provided. {e}")
        return []
    except Exception as e:
        # Catches potential errors during bytes handling or image processing
        print(f"Error processing Base64 image data: {e}")
        return []

# --- Example Usage ---
if __name__ == "__main__":

    # --- Example 1: Decoding from a file ---
    # First, create a dummy QR code image file (requires 'qrcode' library: pip install "qrcode[pil]")
    try:
        import qrcode
        qr_data_to_encode = "Hello from file!"
        qr_img = qrcode.make(qr_data_to_encode)
        dummy_file_path = "temp_qrcode.png"
        qr_img.save(dummy_file_path)
        print(f"Generated dummy QR code file: {dummy_file_path} with data: '{qr_data_to_encode}'")

        print(f"\nDecoding QR from file: {dummy_file_path}")
        decoded_data_list_file = decode_qr_from_file(dummy_file_path)

        if decoded_data_list_file:
            print("Successfully decoded:")
            for data in decoded_data_list_file:
                print(f"  - '{data}'")
        else:
            print("Could not decode QR code from file or none found.")

    except ImportError:
        print("\nSkipping file generation example: 'qrcode' library not installed.")
    except Exception as e:
        print(f"\nError during file generation example: {e}")


    # --- Example 2: Decoding from a Base64 string ---
    # Let's generate a Base64 string first (using the function from the previous request)
    try:
        import qrcode # Need qrcode lib again

        qr_data_to_encode_b64 = "https://example.com/base64_test"
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(qr_data_to_encode_b64)
        qr.make(fit=True)
        img_b64 = qr.make_image(fill_color="black", back_color="white")

        buffered = io.BytesIO()
        img_b64.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        base64_encoded_qr = base64.b64encode(img_bytes).decode('utf-8')

        print(f"\nGenerated dummy Base64 QR code for data: '{qr_data_to_encode_b64}'")
        # print(f"Base64 String (truncated): {base64_encoded_qr[:60]}...") # Optional: print the string

        print("\nDecoding QR from Base64 string...")
        decoded_data_list_b64 = decode_qr_from_base64(base64_encoded_qr)

        if decoded_data_list_b64:
            print("Successfully decoded:")
            for data in decoded_data_list_b64:
                print(f"  - '{data}'")
        else:
            print("Could not decode QR code from Base64 string or none found.")

    except ImportError:
        print("\nSkipping Base64 generation example: 'qrcode' library not installed.")
    except Exception as e:
        print(f"\nError during Base64 generation example: {e}")


    # --- Example 3: File not found ---
    print("\nDecoding QR from non-existent file:")
    decode_qr_from_file("non_existent_file.png")

    # --- Example 4: Invalid Base64 ---
    print("\nDecoding QR from invalid Base64:")
    decode_qr_from_base64("this is not valid base64!@#$")