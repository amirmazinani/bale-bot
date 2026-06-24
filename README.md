# Bale Bot - ERP/CRM منوی خودکار

بات پیام‌رسان Bale برای شرکت‌های نرم‌افزاری ERP/CRM. سیستم **کاملاً داینامیک** - فقط فایل JSON را ویرایش کنید، کدنویسی مورد نیاز نیست!

## 🚀 شروع سریع

### پیش‌نیازها
- Python 3.9+
- Bale Bot Token (از [@bale_iris_bot](https://t.me/bale_iris_bot) در Bale بگیرید)

### نصب و اجرا

```bash
# 1. مخزن را clone کنید
git clone <repo-url>
cd bale-bot

# 2. محیط مجازی ایجاد کنید
python -m venv venv
source venv/bin/activate  # روی Windows: venv\Scripts\activate

# 3. وابستگی‌ها را نصب کنید
pip install -r requirements.txt

# 4. فایل محیط را تنظیم کنید
cp .env.example .env
# حالا .env را ویرایش کنید و BALE_BOT_TOKEN را وارد کنید

# 5. بات را اجرا کنید
python main.py
```

## 📁 ساختار پروژه

```
bale-bot/
├── main.py                  # نقطه ورود بات
├── bot_instance.py          # تنظیم Bale API
├── config.py                # تنظیمات (از محیط بخوانده شده)
├── .env.example             # مثال تنظیمات محیط
├── requirements.txt         # وابستگی‌های Python
│
├── content/
│   ├── content.json         # ✨ **فایل اصلی - همه محتوا اینجا تعریف می‌شود**
│   ├── loader.py            # پردازش content.json
│   └── __init__.py
│
├── handlers/
│   ├── dynamic_menu_router.py   # روتینگ منوها
│   ├── reply_menu.py             # دکمه‌های ریپلای کیبورد
│   ├── demo_capture.py           # جمع‌آوری درخواست دمو
│   ├── start.py                  # دستور /start
│   ├── fallback.py               # پیام‌های ناشناخته
│   └── __init__.py
│
├── keyboards/
│   ├── reply.py             # دکمه‌های پایین صفحه
│   └── __init__.py
│
├── utils/
│   ├── dynamic_navigation.py # مسیریابی خودکار
│   ├── fsm.py                # مدیریت وضعیت چت
│   ├── screen.py             # رندر صفحات
│   ├── logging_setup.py      # تنظیم لاگینگ
│   └── __init__.py
│
├── assets/                   # عکس‌ها و PDF‌های محصولات
│   ├── crm_promo.png
│   ├── tasks_promo.png
│   └── finance_promo.png
│
├── logs/                     # فایل‌های لاگ
│   └── bot.log
│
└── docs/
    ├── README.md             # این فایل
    ├── QUICK_START.md        # شروع سریع (فارسی)
    ├── CONFIGURATION.md      # راهنمای content.json
    └── EXTENDING.md          # افزودن ویژگی‌های جدید
```

## 🎯 چگونه کار می‌کند

### سیستم داینامیک

تمام محتوا (منوها، صفحات، دکمه‌ها، متن‌ها) در **یک فایل JSON** تعریف می‌شوند:

```json
{
  "company": {
    "name": "نام شرکت",
    "phone": "+98...",
    "email": "email@...",
    ...
  },
  "screens": {
    "main_menu": {
      "text": "سلام! یک گزینه را انتخاب کنید:",
      "buttons": [...]
    },
    "about": {
      "text": "درباره ما...",
      "parent": "main_menu",
      "buttons": [...]
    }
  },
  "products": [...],
  "pricing": [...]
}
```

### جریان درخواست

```
👤 کاربر
    ↓ [بات را شروع می‌کند]
📱 صفحه خوش‌آمد
    ↓ [روی دکمه کلیک می‌کند]
🔄 Callback Query
    ↓ [dynamic_menu_router.py پردازش می‌کند]
📄 صفحه جدید (edit-in-place)
```

## 📝 استفاده

### راهنمای سریع

راهنمای کامل برای:
- ✅ [شروع سریع](QUICK_START.md) - تغییرات ساده
- ✅ [کانفیگ‌ها](CONFIGURATION.md) - ساختار content.json
- ✅ [گسترش سیستم](EXTENDING.md) - اضافه کردن ویژگی‌های جدید

### مثال سریع: اضافه کردن صفحه FAQ

**۱. صفحه را به `content.json` اضافه کنید:**

```json
"screens": {
  "faq": {
    "text": "❓ سوالات متداول\n\nموضوع را انتخاب کنید:",
    "parent": "main_menu",
    "buttons": [
      [{"text": "💰 قیمتها", "route": "contact"}],
      [{"text": "🏠 برگشت", "route": "main_menu"}]
    ]
  }
}
```

**۲. دکمه را به منوی اصلی اضافه کنید:**

```json
"main_menu": {
  "buttons": [
    // ... دکمه‌های قبلی
    [{"text": "❓ سوالات متداول", "route": "faq"}]
  ]
}
```

**۳. بات را ریاستارت کنید:**

```bash
python main.py
```

**بس! صفحه جدید کار می‌کند.** ✨

## 🔧 ویژگی‌های کلیدی

| ویژگی | توضیح |
|--------|--------|
| **داینامیک** | بدون کدنویسی - فقط JSON |
| **خودکار** | مسیرها، دکمه‌های back، وضعیت‌ها خودکار |
| **تمیز** | یک پیام، ویرایش‌ در جا |
| **محکم** | بدون پایگاه‌داده، بدون API خارجی |
| **چند زبان** | فارسی، انگلیسی، ... |

## 📊 ساختار منو

```
🏠 منوی اصلی
├── 📦 محصولات
│   ├── CRM
│   ├── مدیریت وظایف
│   └── انبار/مالی
├── 💰 قیمت‌ها
│   ├── استارتر
│   ├── حرفه‌ای
│   └── سازمانی
├── 🏢 درباره ما
├── 📝 وبلاگ
└── 🚀 درخواست دمو

+ هر وقت در هر جا:
  📞 تماس/پشتیبانی (پایین صفحه)
  🏠 منوی اصلی (پایین صفحه)
```

## 🔄 Webhook vs Polling

### Polling (پیش‌فرض)
```bash
# بدون نیاز به دامنه عمومی
python main.py
```

### Webhook (تولید)
```bash
USE_WEBHOOK=true \
WEBHOOK_HOST=https://yourdomain.com \
WEBHOOK_PATH=/webhook/bale \
python main.py
```

## 🧪 تست

```bash
# تمام تست‌ها
pytest tests/

# تنها یک تست
pytest tests/test_navigation.py::test_route_generation
```

## 🐛 عیب‌یابی

### بات شروع نمی‌شود
```
❌ Error: BOT_TOKEN not found
✅ حل: BALE_BOT_TOKEN را در .env قرار دهید
```

### صفحه نمایش داده نمی‌شود
```
❌ Error: Screen not found
✅ حل: screen_key را در content.json بررسی کنید
```

### دکمه کار نمی‌کند
```
❌ Error: Unknown route
✅ حل: route را درست نوشته‌اید؟ screen وجود دارد؟
```

## 📚 منابع

- [Bale Docs](https://docs.bale.ai/)
- [aiogram 3.x Docs](https://docs.aiogram.dev/)
- [راهنمای سریع](QUICK_START.md)
- [تنظیمات](CONFIGURATION.md)
- [گسترش](EXTENDING.md)

## 📄 مجوز

MIT License - می‌تونید از این پروژه برای هر منظوری استفاده کنید.

## 🤝 مشارکت

مشکلاتی پیدا کردید؟ یک Issue باز کنید یا PR ارسال کنید!

---

**نیاز کمک دارید؟** ببینید [QUICK_START.md](QUICK_START.md) 👈
