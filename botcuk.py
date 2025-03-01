import logging
import asyncio
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, filters
from datetime import datetime

# Loglama yapılandırması
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
    handlers=[logging.FileHandler("bot_log.txt", mode="w")]  # Logları bu dosyaya kaydeder
)
logger = logging.getLogger(__name__)

# Kanal kullanıcı adı
KANAL_USERNAME = "@ethancheater"
DESTEK_KANAL_USERNAME = "@ethandestekbotuu"  # Destek kanalı kullanıcı adı
YONETICI_USERNAME = "@viphesaphanem"  # Yönetici kullanıcı adı

# Rastgele 0.00 - 1.00 arasında bir sayı üretme
def random_hiz():
    return round(random.uniform(0.00, 1.00), 2)

# /start komutu
async def start(update: Update, context: CallbackContext):
    try:
        user = update.message.from_user
        chat_member = await context.bot.get_chat_member(KANAL_USERNAME, user.id)

        # Kullanıcının tam adı
        user_name = user.full_name

        keyboard = [
            [InlineKeyboardButton("💎 Altyapıyı Satın Al", callback_data="altyapi_satin_al")],
            [InlineKeyboardButton("📷 Kanıt Yolla", callback_data="kanit_yolla"),
             InlineKeyboardButton("🆘 Destek Talep Et", callback_data="destek_talep_et")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if chat_member.status in ["member", "administrator", "creator"]:
            await update.message.reply_text(
                f"*👋 Merhaba, {user_name}! Altyapıyı satın almak, kanıt göndermek veya destek talebi oluşturmak için aşağıdaki butonları kullanabilirsiniz.*",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            keyboard = [
                [InlineKeyboardButton("📢 Kanala Katıl", url=f"https://t.me/{KANAL_USERNAME[1:]}"),
                 InlineKeyboardButton("✅ Kontrol Et", callback_data="kontrol")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "*❌ Bu botu kullanabilmek için önce kanala katılmalısınız.*\n\n"
                "*✅ Katıldıktan sonra aşağıdaki kontrol et butonuna tıklayarak kullanabilirsiniz.*",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Bir hata oluştu: {e}")

# Altyapıyı satın al butonuna tıklandığında
async def altyapi_satin_al(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        user = query.from_user
        chat_member = await context.bot.get_chat_member(KANAL_USERNAME, user.id)

        if chat_member.status not in ["member", "administrator", "creator"]:
            await query.answer(
                "❌ Altyapıyı satın alabilmek için önce kanala katılmanız gerekiyor. "
                "Kanala katılmak için /start komutunu kullanabilirsiniz.",
                show_alert=True
            )
            return

        keyboard = [[InlineKeyboardButton("⬅️ Geri Dön", callback_data="geri_don")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "💰 *Fiyat: 200 TL*\n"
            "📩 *İletişim: @viphesaphanem*",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Bir hata oluştu: {e}")

# Destek talep et butonuna tıklandığında
async def destek_talep_et(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        user = query.from_user
        chat_member = await context.bot.get_chat_member(KANAL_USERNAME, user.id)

        if chat_member.status not in ["member", "administrator", "creator"]:
            await query.answer("❌ Destek talebi oluşturabilmek için önce kanala katılmanız gerekiyor. Kanala katılmak için /start komutunu kullanabilirsiniz.", show_alert=True)
            return

        # "Evet" ve "Hayır" butonları
        keyboard = [
            [InlineKeyboardButton("❌ Hayır", callback_data="destek_hayir"),
             InlineKeyboardButton("✅ Evet", callback_data="destek_evvet")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "*🆘 Destek talebi oluşturmak istiyor musunuz?*",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Bir hata oluştu: {e}")

# Destek talebini kabul ettiğinde kanala mesaj at
async def destek_evvet(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        user = query.from_user

        await query.answer()

        # Destek talebini kalın formatta mesaj olarak hazırlıyoruz
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Destek talebini gönderme
        talep_mesaji = (
            f"*🆘 Yeni Destek Talebi!*\n\n"
            f"*🪧 Kullanıcı Adı:* @{user.username if user.username else 'Bilinmiyor'}\n"
            f"*👤 Adı-Soyadı:* {user.full_name}\n"
            f"*⚙️ Kullanıcı ID:* {user.id}\n"
            f"*📅 Talep Tarihi:* {timestamp}"
        )

        await context.bot.send_message(
            chat_id=DESTEK_KANAL_USERNAME,
            text=talep_mesaji,
            parse_mode='Markdown'
        )

        keyboard = [
            [InlineKeyboardButton("⬅️ Geri Dön", callback_data="geri_don")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "*🟢 Destek talebiniz başarıyla gönderildi, teşekkür ederiz!*\n\n"
            "*⚡ Tekrar talep oluşturmak için aşağıdaki butonları tıklayabilirsiniz.*",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Bir hata oluştu: {e}")

# Destek talebini reddettiğinde
async def destek_hayir(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("⬅️ Geri Dön", callback_data="geri_don")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "*❌ Destek talebiniz iptal edildi. Eğer değişiklik yapmak isterseniz, tekrar destek talebi oluşturabilirsiniz.*",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Bir hata oluştu: {e}")

# Geri dön butonuna tıklandığında
async def geri_don(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        user = query.from_user
        full_name = user.full_name

        keyboard = [
            [InlineKeyboardButton("💎 Altyapıyı Satın Al", callback_data="altyapi_satin_al")],
            [InlineKeyboardButton("📷 Kanıt Yolla", callback_data="kanit_yolla"),
             InlineKeyboardButton("🆘 Destek Talep Et", callback_data="destek_talep_et")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.answer()
        await query.edit_message_text(
            f"*👋 Merhaba, {full_name}! Altyapıyı satın almak, kanıt göndermek veya destek talebi oluşturmak için aşağıdaki butonları kullanabilirsiniz.*",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Bir hata oluştu: {e}")

# Kanala katılım kontrolü için callback
async def kontrol_et(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        user = query.from_user
        chat_member = await context.bot.get_chat_member(KANAL_USERNAME, user.id)

        if chat_member.status in ["member", "administrator", "creator"]:
            await query.answer("✅ Kanala katılım doğrulandı! Botu kullanabilirsiniz.", show_alert=True)
            keyboard = [
                [InlineKeyboardButton("💎 Altyapıyı Satın Al", callback_data="altyapi_satin_al")],
                [InlineKeyboardButton("📷 Kanıt Yolla", callback_data="kanit_yolla"),
                 InlineKeyboardButton("🆘 Destek Talep Et", callback_data="destek_talep_et")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"*✅ Teşekkür ederiz {user.full_name}! Altyapıyı satın almak, kanıt göndermek veya destek talebi oluşturmak için aşağıdaki butonları kullanabilirsiniz.*",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await query.answer(
                "❌ Hâlâ kanala katılmamışsınız. Lütfen önce kanala katılın.",
                show_alert=True
            )
    except Exception as e:
        logger.error(f"Bir hata oluştu: {e}")

# Kanıt yolla butonuna tıklandığında
async def kanit_yolla(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        user = query.from_user
        chat_member = await context.bot.get_chat_member(KANAL_USERNAME, user.id)

        if chat_member.status not in ["member", "administrator", "creator"]:
            await query.answer("❌ Kanıt gönderebilmek için önce kanala katılmanız gerekiyor. Kanala katılmak için /start komutunu kullanabilirsiniz.", show_alert=True)
            return

        # Kullanıcının "Kanıt Yolla" butonuna bastığını kaydet
        context.user_data["son_buton"] = "kanit_yolla"

        keyboard = [
            [InlineKeyboardButton("⬅️ Geri Dön", callback_data="geri_don")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.answer()
        await query.edit_message_text(
            "*📸 Lütfen kanıt olarak bir fotoğraf gönderin.*",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Bir hata oluştu: {e}")

# Fotoğraf gönderildiğinde tetiklenen işlem
async def handle_photo(update: Update, context: CallbackContext):
    try:
        user = update.message.from_user
        chat_member = await context.bot.get_chat_member(KANAL_USERNAME, user.id)

        if chat_member.status in ["member", "administrator", "creator"]:
            username = f"@{user.username}" if user.username else user.full_name
            user_id = user.id

            await context.bot.send_photo(
                chat_id=KANAL_USERNAME,
                photo=update.message.photo[-1].file_id,
                caption=f"*Kullanıcı:* {username}\n"
                        f"*ID:* {user_id}\n"
                        "*Kanıt gönderdi!*",
                parse_mode='Markdown'
            )

            keyboard = [
                [InlineKeyboardButton("⬅️ Geri Dön", callback_data="geri_don")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                "*🟢 Kanıtınız başarıyla gönderildi, teşekkür ederiz!*\n\n"
                "*⚡ Tekrar kanıt göndermek için aşağıdaki butonlara tıklayabilirsiniz.*",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            keyboard = [
                [InlineKeyboardButton("📢 Kanala Katıl", url=f"https://t.me/{KANAL_USERNAME[1:]}"),
                 InlineKeyboardButton("✅ Kontrol Et", callback_data="kontrol")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "*❌ Bu botu kullanabilmek için önce kanala katılmalısınız.*\n\n"
                "*✅ Katıldıktan sonra aşağıdaki kontrol et butonuna tıklayarak kontrol edebilirsiniz.*",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Bir hata oluştu: {e}")

# Ana bot fonksiyonu
def main():
    try:
        BOT_TOKEN = "7845621458:AAHAgUWam14iJWU_VZB0CV9XwpmCxsnWhi8"

        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
        application.add_handler(CallbackQueryHandler(kontrol_et, pattern="kontrol"))
        application.add_handler(CallbackQueryHandler(kanit_yolla, pattern="kanit_yolla"))
        application.add_handler(CallbackQueryHandler(geri_don, pattern="geri_don"))
        application.add_handler(CallbackQueryHandler(destek_talep_et, pattern="destek_talep_et"))
        application.add_handler(CallbackQueryHandler(altyapi_satin_al, pattern="altyapi_satin_al"))
        application.add_handler(CallbackQueryHandler(destek_evvet, pattern="destek_evvet"))
        application.add_handler(CallbackQueryHandler(destek_hayir, pattern="destek_hayir"))

        print("✅ Bot Aktif")
        application.run_polling()
    except Exception as e:
        logger.critical(f"Bot başlatılamadı: {e}")

if __name__ == "__main__":
    main()