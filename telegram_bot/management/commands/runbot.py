import numpy as np
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from bs4 import BeautifulSoup
from telegram import Update
import requests

import cv2

from decouple import config

BOT_TOKEN = config('BOT_TOKEN')

def print_like_table( name, ext, price):
    formatted_filename = f"{name[:10]}{'_' * (12 - len(name[:10]))}"
    formatted_ext = f"{ext[:9]}{" " * (12 - len(ext[:9]))}"
    text = f" {formatted_filename}  |  {formatted_ext}  | {price}"
    # print(text)
    return '\n'+ text


def scrape_receipt_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')

    memo = []
    memo_dict = {}
    products = table.find('tbody').find_all('tr')
    
    for index, tr in enumerate(products):

        if 'products-row' in tr.get('class', []):
            if memo_dict:
                memo.append(memo_dict)
                memo_dict = {}
            for i, td in enumerate(tr.find_all('td')):
                match i:
                    case 0: memo_dict["name"] = td.text.strip()
                    case 1: memo_dict["soni"] = td.text.strip()
                    case 2: memo_dict["narxi"] = td.text.strip()

        else:
            for i, td in enumerate(tr.find_all('td')):
                if i == 0:
                    m = td.text.strip()
                else:
                    memo_dict[m] = td.text.strip()
    memo.append(memo_dict)

   
    data = {
        'receipt_number': soup.title.text,
        'shop_name': soup.title.text,
        'date': soup.title.text,
        'product': memo,
    }

    return memo





def scan_qr_code(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    qr_code_detector = cv2.QRCodeDetector()
    decoded_text, points, _ = qr_code_detector.detectAndDecode(image)

    if decoded_text:
        return decoded_text  # Return the decoded text directly
    else:
        return None


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send me a QR code image!')



async def handle_photo(update: Update, context: CallbackContext) -> None:
    file_id = update.message.photo[-1].file_id
   
    file_info = await context.bot.get_file(file_id)
    file_path = file_info.file_path
    
    response = requests.get(file_path)
    
    if response.status_code == 200:
        with open('test_image.jpg', 'wb') as f:
            f.write(response.content)
        print("Image saved successfully.")
    else:
        print(f"Failed to retrieve the image. Status code: {response.status_code}")




    try:
        qr_data = scan_qr_code('test_image.jpg')
        if qr_data:
            await update.message.reply_text(f'Url: {qr_data}')
            message = ""
            count = 0
            if update.message.caption and update.message.caption.lower() == 'about':
                print(update.message.caption)

                for mess in scrape_receipt_data(qr_data):
                    message = ""
                    for k, v in mess.items():
                        message += f"{k} :  {v}\n"
                    await update.message.reply_text(message)
            else:
                for data in scrape_receipt_data(qr_data):
                    message += print_like_table(data['name'], f"{data['soni']} {'kg' if data['name'].endswith('kg') else 'dona'}", data["narxi"])
                    count += 1
                print(f"Product:  {count}")
                await update.message.reply_text(message)
        else:
            await update.message.reply_text('No QR code found.')
    except:
        await update.message.reply_text('Not a valid QR code !')
    
    




async def handle_text(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text.lower()

    if user_text == 'hello':
        await update.message.reply_text('Hello! How can I assist you today?')
    elif user_text == 'help':
        await update.message.reply_text('You can send me a QR code image or type "hello" to greet me.')
    elif user_text.startswith("http"):
        
        print(user_text)
        for mess in scrape_receipt_data('https://ofd.soliq.uz/check?t=UZ210317259332&r=135011&c=20240703163649&s=752204180546'):
            message = ""
            for k, v in mess.items():
                message += f"{k} :  {v}\n"
            await update.message.reply_text(message)
        
    else:
        await update.message.reply_text(f'You said: {user_text}')


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.run_polling()


if __name__ == '__main__':
    main()

