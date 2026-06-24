# 🚀 راهنمای گسترش سیستم

این راهنما برای توسعه‌دهندگانی است که می‌خواهند **بخش‌های جدید** به بات اضافه کنند.

## 📋 فهرست

1. [معماری کلی](#معماری-کلی)
2. [اضافه کردن handler جدید](#اضافه-کردن-handler-جدید)
3. [ایجاد صفحات پویا](#ایجاد-صفحات-پویا)
4. [مدیریت وضعیت (FSM)](#مدیریت-وضعیت-fsm)
5. [لاگینگ و عیب‌یابی](#لاگینگ-و-عیب‌یابی)

---

## معماری کلی

```
Bale User
    ↓
[aiogram Router]
    ↓
[handlers/*]  ← تمام handler‌ها
    ├── dynamic_menu_router.py (منوها)
    ├── demo_capture.py (جمع‌آوری درخواست)
    ├── reply_menu.py (دکمه‌های ریپلای)
    ├── start.py (/start)
    └── fallback.py (غیرشناخته)
    ↓
[utils/*]  ← ابزارهای کمکی
    ├── dynamic_navigation.py (مسیریابی)
    ├── screen.py (رندر)
    ├── fsm.py (وضعیت)
    └── logging_setup.py (لاگ)
    ↓
[content/loader.py]  ← بارگیری content.json
    ↓
Bale API
```

---

## اضافه کردن handler جدید

### مثال: Handler برای پرسش از نظر کاربران

#### ۱. ایجاد فایل جدید

```python
# handlers/feedback.py

import logging
from aiogram import Router
from aiogram.types import Message

from utils.fsm import fsm_store
from utils.screen import render_screen
from content.loader import SCREENS

logger = logging.getLogger(__name__)
router = Router(name="feedback_handler")

@router.message()
async def handle_feedback_text(message: Message):
    """
    هندلر برای دریافت نظرات کاربران.
    """
    chat_id = message.chat.id
    
    # اگر کاربر در حالت انتظار نظر است
    if fsm_store.is_awaiting_feedback(chat_id):
        feedback_text = message.text
        user_id = message.from_user.id
        
        # ثبت نظر
        logger.info(f"FEEDBACK | user_id={user_id} | {feedback_text}")
        
        # پیام تشکر
        thank_you_screen = SCREENS.get("feedback_thankyou")
        if thank_you_screen:
            await message.answer(
                thank_you_screen.text,
                reply_markup=thank_you_screen.keyboard
            )
        
        # بازنشانی وضعیت
        fsm_store.reset(chat_id)
```

#### ۲. ثبت router در main.py

```python
# main.py

from handlers import feedback

async def main():
    # ... کد قبلی
    
    # ثبت router جدید
    dp.include_router(feedback.router)
    
    # ... ادامه
```

---

## ایجاد صفحات پویا

### مثال: صفحه‌ای که از Database داده می‌خواند

```python
# handlers/special_offers.py

import logging
from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.screen import render_screen, safe_answer_callback

logger = logging.getLogger(__name__)
router = Router(name="special_offers_router")

# فرض کنید یک database داریم
OFFERS_DB = {
    "offer_1": {
        "title": "🎁 تخفیف ۲۰% برای خرید ۳ ماهه",
        "description": "تنها این ماه!",
        "button_text": "🚀 درخواست دمو",
    }
}

async def render_special_offers(callback: CallbackQuery):
    """صفحه‌ای که از database داده می‌خواند"""
    
    # ساخت متن از database
    offers_text = "🎁 پیشنهادهای ویژه\n\n"
    for offer_id, offer in OFFERS_DB.items():
        offers_text += f"• {offer['title']}\n  {offer['description']}\n\n"
    
    # ساخت دکمه‌های از database
    buttons = []
    for offer_id in OFFERS_DB.keys():
        buttons.append([InlineKeyboardButton(
            text=OFFERS_DB[offer_id]["button_text"],
            callback_data=f"special_offer:{offer_id}"
        )])
    
    buttons.append([InlineKeyboardButton(
        text="🏠 منوی اصلی",
        callback_data="menu:main_menu"
    )])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await safe_answer_callback(callback)
    await render_screen(callback, offers_text, keyboard)

@router.callback_query()
async def on_special_offers_callback(callback: CallbackQuery):
    """هندل کلیک روی پیشنهادهای ویژه"""
    if callback.data and callback.data.startswith("special_offer:"):
        offer_id = callback.data.split(":", 1)[1]
        offer = OFFERS_DB.get(offer_id)
        
        if offer:
            await safe_answer_callback(callback)
            await callback.message.answer(f"✅ شما درخواست دمو برای {offer['title']} را فرستادید!")
```

---

## مدیریت وضعیت (FSM)

### نمونه: Flow چند مرحله‌ای

```python
# handlers/survey.py

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from utils.fsm import fsm_store
from utils.screen import render_screen, safe_answer_callback
from content.loader import SCREENS

logger = logging.getLogger(__name__)
router = Router(name="survey_handler")

# وضعیت‌های سفارشی
class SurveyState:
    AWAITING_COMPANY_NAME = "survey_company_name"
    AWAITING_INDUSTRY = "survey_industry"
    AWAITING_EMPLOYEES = "survey_employees"
    AWAITING_BUDGET = "survey_budget"

@router.callback_query()
async def start_survey(callback: CallbackQuery):
    """شروع نظرسنجی"""
    if callback.data == "menu:survey":
        chat_id = callback.message.chat.id
        
        # تنظیم وضعیت اول
        fsm_store.surveys[chat_id] = {
            "state": SurveyState.AWAITING_COMPANY_NAME,
            "data": {}
        }
        
        await safe_answer_callback(callback)
        await callback.message.answer(
            "❓ نظرسنجی\n\nنام شرکت را وارد کنید:"
        )

@router.message()
async def handle_survey_input(message: Message):
    """دریافت ورودی‌های نظرسنجی"""
    chat_id = message.chat.id
    
    if chat_id not in fsm_store.surveys:
        return
    
    survey = fsm_store.surveys[chat_id]
    state = survey["state"]
    
    if state == SurveyState.AWAITING_COMPANY_NAME:
        survey["data"]["company_name"] = message.text
        survey["state"] = SurveyState.AWAITING_INDUSTRY
        await message.answer(
            f"✅ نام شرکت: {message.text}\n\n"
            "حالا صنعت خود را انتخاب کنید:"
        )
    
    elif state == SurveyState.AWAITING_INDUSTRY:
        survey["data"]["industry"] = message.text
        
        # ثبت نظرسنجی کامل
        logger.info(f"SURVEY | {survey['data']}")
        
        # حذف
        del fsm_store.surveys[chat_id]
        
        await message.answer(
            "✅ نظرسنجی کامل شد! ممنون از وقتتان.\n\n"
            "تیم ما ظرف ۲۴ ساعت با شما تماس خواهد گرفت."
        )
```

---

## لاگینگ و عیب‌یابی

### سیستم لاگینگ

```python
# utils/logging_setup.py (موجود)

import logging
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

def setup_logging(level="INFO"):
    """تنظیم لاگینگ"""
    
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # فایل
    fh = logging.FileHandler(LOG_DIR / "bot.log")
    fh.setLevel(level)
    
    # Console
    ch = logging.StreamHandler()
    ch.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
```

### استفاده از لاگینگ

```python
import logging

logger = logging.getLogger(__name__)

# سطح مختلف لاگینگ
logger.debug("رویداد debug")
logger.info("رویداد عادی")
logger.warning("هشدار")
logger.error("خطا")
logger.exception("استثنا")

# نمونه‌ای واقع‌گرایانه
logger.info(f"user_id={user_id} tapped route={route}")
logger.warning(f"Unknown product key: {product_key}")
logger.error(f"Failed to send photo: {exc}")
```

### بررسی لاگ‌ها

```bash
# آخرین ۵۰ خط
tail -50 logs/bot.log

# جستجو در لاگ‌ها
grep "DEMO_LEAD" logs/bot.log

# بررسی خطاها
grep "ERROR" logs/bot.log
```

---

## شروع سریع: اضافه کردن ویژگی جدید

### مرحله ۱: اضافه کردن به content.json

```json
{
  "screens": {
    "new_feature": {
      "text": "🆕 ویژگی جدید",
      "parent": "main_menu",
      "buttons": [
        [{"text": "📞 بیشتر بدانید", "route": "contact"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    }
  }
}
```

### مرحله ۲: آپدیت منوی اصلی

```json
{
  "main_menu": {
    "buttons": [
      // ... دکمه‌های دیگر
      [{"text": "🆕 ویژگی جدید", "route": "new_feature"}]
    ]
  }
}
```

### مرحله ۳: اگر logic پیچیده‌ای نیاز است

```python
# handlers/new_feature.py

@router.callback_query()
async def handle_new_feature(callback: CallbackQuery):
    if callback.data == "menu:new_feature":
        # logic خاص
        await render_screen(callback, text, keyboard)
```

### مرحله ۴: ثبت در main.py

```python
from handlers import new_feature
dp.include_router(new_feature.router)
```

---

## 🧪 تست کردن تغییرات

```bash
# چک JSON
python -c "import json; json.load(open('content/content.json'))" && echo "✅ JSON Valid"

# بات را اجرا کنید
python main.py

# بررسی لاگ‌ها در terminal
# [INFO] - رویدادهای عادی
# [WARNING] - هشدارها
# [ERROR] - خطاها
```

---

## 📚 بیشتر بخوانید

- [معرفی](README.md)
- [تنظیمات](CONFIGURATION.md)
- [شروع سریع](QUICK_START.md)
- [aiogram Docs](https://docs.aiogram.dev/)

---

**سوالی دارید؟** مشکل را گزارش دهید! 🐛
