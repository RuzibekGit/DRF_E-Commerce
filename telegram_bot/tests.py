import cv2


def scan_qr_code(image_path):


  image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

  decoded_objects = cv2.QRCodeDetector().detectAndDecode(image)

  if decoded_objects:
    return decoded_objects[0].encode("utf-8")  # Access data and decode

  else:
    return None  # No QR code found
  

# Example usage (replace 'path/to/your/image.jpg' with your actual image path)
image_path = 'C:/Code_PY/dJango/Month-08/class_work/E_Commerce/telegram_bot/photo_2024-07-22_17-34-21.jpg'
decoded_text = scan_qr_code(image_path)

if decoded_text:
  print("Decoded Text:", decoded_text)
else:
  print("No QR code found in the image.")
