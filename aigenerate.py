import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from io import BytesIO
import logging
import time

TELEGRAM_TOKEN = & '7888367344:AAHEWg57r3lwg7dpYJpGXz2P4mcYYu0vNPg' #توكنك
CHANNEL_LINK = "https://t.me/S_T3S" # قناتك

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

API_URL = "https://ai-api.magicstudio.com/api/ai-art-generator"

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 12; SM-A025F Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.137 Mobile Safari/537.36",
    'Accept': "application/json, text/plain, */*",
    'sec-ch-ua-platform': "\"Android\"",
    'sec-ch-ua': "\"Not(A:Brand\";v=\"99\", \"Android WebView\";v=\"133\", \"Chromium\";v=\"133\"",
    'sec-ch-ua-mobile': "?1",
    'origin': "https://magicstudio.com",
    'sec-fetch-site': "same-site",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://magicstudio.com/ai-art-generator/",
    'accept-language': "ar-AE,ar-IQ;q=0.9,ar;q=0.8,en-US;q=0.7,en;q=0.6",
    'priority': "u=1, i"
}

def generate_image(prompt):
    """إنشاء صورة باستخدام واجهة MagicStudio API"""
    logger.info(f"جاري إنشاء صورة للوصف: {prompt}")
    
    payload = {
        'prompt': prompt,  
        'output_format': 'bytes',
        'user_profile_id': 'null',
        'user_is_subscribed': 'true',
    }
    
    try:
        logger.info("جاري إرسال الطلب إلى الواجهة البرمجية...")
        response = requests.post(API_URL, data=payload, headers=HEADERS, timeout=30)
        logger.info(f"حالة الاستجابة: {response.status_code}")
        
        if response.status_code == 200:
            logger.info("تم إنشاء الصورة بنجاح")
            return response.content
        else:
            logger.error(f"خطأ في الواجهة البرمجية: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"فشل في طلب الواجهة البرمجية: {str(e)}")
        return None

def start(update: Update, context: CallbackContext):
    """معالجة أمر /start مع صورة ورسالة ترحيبية"""
    user = update.effective_user
    welcome_image_url = "https://via.placeholder.com/600x400?text=Welcome+Bot"  
    
    try:
        update.message.reply_photo(
            photo=welcome_image_url,
            caption=f"مرحباً {user.first_name}! 👋\n"
                    "أنا بوت إنشاء الصور باستخدام الذكاء الاصطناعي.\n\n"
                    "ما عليك سوى إرسال وصف للصورة التي تريدها وسأقوم بإنشائها لك!\n\n"
                    "استخدم الأمر:\n"
                    "/generate متبوعاً بوصف الصورة\n"
                    "مثال: /generate منظر غروب الشمس",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
            ])
        )
    except Exception as e:
        logger.error(f"فشل في إرسال الصورة: {str(e)}")
        update.message.reply_text(
            f"مرحباً {user.first_name}! 👋\n"
            "أنا بوت إنشاء الصور باستخدام الذكاء الاصطناعي.\n\n"
            "ما عليك سوى إرسال وصف للصورة التي تريدها وسأقوم بإنشائها لك!\n\n"
            "استخدم الأمر:\n"
            "/generate متبوعاً بوصف الصورة\n"
            "مثال: /generate منظر غروب الشمس",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
            ])
        )

def handle_image_request(update: Update, context: CallbackContext):
    """معالجة طلبات إنشاء الصور مع شريط التقدم"""
    if not context.args:
        update.message.reply_text(
            "⚠️ الرجاء إدخال وصف للصورة بعد الأمر /generate\n"
            "مثال: /generate منظر غروب الشمس على البحر",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
            ])
        )
        return
    
    prompt = ' '.join(context.args)
    if len(prompt) < 5:
        update.message.reply_text(
            "⚠️ الوصف قصير جداً. الرجاء إدخال وصف مفصل أكثر",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
            ])
        )
        return
    
   
    progress_msg = update.message.reply_text(
        "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%\nجاري معالجة طلبك...",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
        ])
    )
    
    # محاكاة شريط التقدم
    for i in range(1, 11):
        time.sleep(0.5)
        progress_bar = "🟩" * i + "⬜" * (10 - i)
        try:
            progress_msg.edit_text(
                f"{progress_bar} {i*10}%\nجاري إنشاء صورتك المطلوبة...",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
                ])
            )
        except Exception as e:
            logger.error(f"خطأ في تحديث شريط التقدم: {str(e)}")
    
   
    image_data = generate_image(prompt)
    
    if image_data:
        try:
         
            update.message.reply_photo(
                photo=BytesIO(image_data),
                caption=f"🎨 الصورة الناتجة لوصفك:\n{prompt}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
                ])
            )
            progress_msg.edit_text(
                "✅ تم إنشاء الصورة بنجاح!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
                ])
            )
        except Exception as e:
            logger.error(f"خطأ في إرسال الصورة: {str(e)}")
            progress_msg.edit_text(
                "❌ فشل في إرسال الصورة. يرجى المحاولة لاحقاً.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
                ])
            )
    else:
        progress_msg.edit_text(
            "❌ لم أتمكن من إنشاء الصورة. قد يكون الوصف غير مناسب أو هناك مشكلة في الخدمة.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
            ])
        )

def handle_text(update: Update, context: CallbackContext):
    """معالجة الرسائل النصية العادية"""
    text = update.message.text
    if not text.startswith('/'):
        update.message.reply_text(
            "📝 لإنشاء صورة، يمكنك استخدام الأمر:\n"
            "/generate متبوعاً بوصف الصورة\n"
            "مثال: /generate منظر غروب الشمس على البحر",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
            ])
        )

def error_handler(update: Update, context: CallbackContext):
    """معالجة الأخطاء"""
    logger.error(f"التحديث {update} تسبب في الخطأ {context.error}")
    if update.message:
        update.message.reply_text(
            "❌ حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("قناتي", url=CHANNEL_LINK)]
            ])
        )

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("generate", handle_image_request, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    

    dp.add_error_handler(error_handler)
 
    updater.start_polling()
    logger.info("تم تشغيل البوت بنجاح...")
    updater.idle()

if __name__ == '__main__':
    main()