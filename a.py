from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
import re
import os

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Simpan status dan pilihan pengguna
user_states = {}

def get_start_keyboard() -> ReplyKeyboardMarkup:
    """Sediakan papan kekunci untuk arahan /start."""
    keyboard = [
        [KeyboardButton("Bug Vless")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_bugvless_keyboard() -> ReplyKeyboardMarkup:
    """Sediakan papan kekunci untuk arahan Bug Vless."""
    keyboard = [
        [KeyboardButton("Digi BS"), KeyboardButton("Digi XL")],
        [KeyboardButton("UmoFunz XL"), KeyboardButton("Maxis UL")],
        [KeyboardButton("Unifi XL"), KeyboardButton("Yes XL")],
        [KeyboardButton("Celcom XL"), KeyboardButton("Booster 1"), KeyboardButton("Booster 2")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Sediakan papan kekunci untuk membatalkan permintaan."""
    keyboard = [
        [KeyboardButton("Cancel")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

@app.on_message(filters.command("start"))
def handle_start(client, message):
    """Handle /start command."""
    message.reply(
        "===================================\nBot MF By IMMANVPN\n\n"
        "Hi! Saya adalah bot yang dapat membantu anda dalam beberapa hal "
        "yang dapat memudahkan kerja anda!\n\nSaya mempunyai beberapa fungsi "
        "menarik yang dapat anda gunakan!\n\nKlik butang di bawah untuk memulakan.\n"
        "===================================",
        reply_markup=get_start_keyboard()
    )

@app.on_message(filters.text & filters.regex("^Bug Vless$"))
def handle_bugvless(client, message):
    """Handle Bug Vless button and show options."""
    user_states[message.chat.id] = {'state': 'awaiting_vless_url', 'format': None}
    message.reply(
        "Pilih salah satu pilihan di bawah:",
        reply_markup=get_bugvless_keyboard()
    )

@app.on_message(filters.text & filters.regex("^(Digi BS|Digi XL|UmoFunz XL|Maxis UL|Unifi XL|Yes XL|Celcom XL|Booster 1|Booster 2)$"))
def handle_bugvless_option(client, message):
    """Handle the options selected by user for Bug Vless."""
    if message.chat.id in user_states and user_states[message.chat.id]['state'] == 'awaiting_vless_url':
        selected_option = message.text
        user_states[message.chat.id]['format'] = selected_option
        message.reply(
            f"Anda memilih {selected_option}. Sila hantar URL Vless anda:",
            reply_markup=get_cancel_keyboard()
        )

@app.on_message(filters.text & filters.regex("^vless://"))
def handle_vless_url(client, message):
    """Handle the Vless URL sent by the user."""
    if message.chat.id in user_states and user_states[message.chat.id]['state'] == 'awaiting_vless_url':
        selected_format = user_states[message.chat.id].get('format')
        if selected_format:
            # Process the URL with the selected format
            user_text = message.text
            uuid, subdo, name = extract_info_from_text(user_text)
            if uuid and subdo and name:
                conversion_options = {
                    "Digi BS": f"vless://{uuid}@162.159.134.61:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
                    "Digi XL": f"vless://{uuid}@app.optimizely.com:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
                    "UmoFunz XL": f"vless://{uuid}@{subdo}:80?path=/vlessws&encryption=none&type=ws&host=m.pubgmobile.com#{name}",
                    "Maxis UL": f"vless://{uuid}@speedtest.net:443?path=/vlessws&encryption=none&type=ws&host=fast.{subdo}&sni=speedtest.net#{name}",
                    "Unifi XL": f"vless://{uuid}@104.17.10.12:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
                    "Yes XL": f"vless://{uuid}@104.17.113.188:80?path=/vlessws&encryption=none&type=ws&host=tap-database.who.int.{subdo}#{name}",
                    "Celcom XL": f"vless://{uuid}@104.17.148.22:80?path=/vlessws&encryption=none&type=ws&host=opensignal.com.{subdo}#{name}",
                    "Booster 1": f"vless://{uuid}@104.17.147.22:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}",
                    "Booster 2": f"vless://{uuid}@www.speedtest.net:80?path=/vlessws&encryption=none&type=ws&host={subdo}#{name}"
                }
                reply = conversion_options.get(selected_format, "Invalid option selected.")
                message.reply(reply)
            else:
                message.reply("Invalid URL format. Please send a valid vless URL.")
            
            # Reset user state
            user_states[message.chat.id] = {'state': None, 'format': None}

@app.on_message(filters.text & filters.regex("^Cancel$"))
def handle_cancel(client, message):
    """Handle Cancel button and reset state."""
    if message.chat.id in user_states:
        user_states[message.chat.id] = {'state': None, 'format': None}
        message.reply(
            "Permintaan dibatalkan. Sila pilih butang lain jika anda ingin memulakan semula.",
            reply_markup=get_start_keyboard()
        )

def extract_info_from_text(user_text: str) -> tuple:
    """Extract UUID, subdomain, and name from a full vless URL."""
    pattern = r"vless://([^@]+)@([^:]+):(\d+)\?path=/vlessws&encryption=none&type=ws#(.+)"
    match = re.match(pattern, user_text)
    if match:
        uuid = match.group(1)
        subdo = match.group(2)
        name = match.group(4)
        return uuid, subdo, name
    return None, None, None

# Mulakan bot
app.run()
