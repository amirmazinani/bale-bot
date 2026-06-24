# راهنمای کامل: اضافه کردن مسیر و دکمه جدید به بات

این راهنما مراحل کامل اضافه کردن یک مسیر و دکمه جدید به بات رو توضیح میده.

## ۱. مثال: اضافه کردن صفحه "تیم ما" (Our Team)

فرض کنیم میخوایم یک صفحه جدید به اسم "تیم ما" اضافه کنیم که در منوی اصلی ظاهر بشه.

## ۲. مراحل کار

### مرحله ۱: تعریف مسیر جدید در `utils/navigation.py`

فایل `utils/navigation.py` رو باز کنید و تغییرات زیر رو انجام بدید:

```python
# بعد از مسیرهای موجود اضافه کنید:
ROUTE_OUR_TEAM = "menu:our_team"

# به ROUTE_MAP اضافه کنید:
ROUTE_MAP: dict[str, str] = {
    # ... مسیرهای موجود
    "our_team": ROUTE_OUR_TEAM,  # اضافه شده
}

# به PARENT_ROUTES اضافه کنید (این صفحه از منوی اصلی میاد):
PARENT_ROUTES: dict[str, str] = {
    # ... مسیرهای موجود
    ROUTE_OUR_TEAM: ROUTE_MAIN_MENU,  # اضافه شده
}

# به _ALL_ROUTES اضافه کنید:
_ALL_ROUTES: tuple[str, ...] = (
    # ... مسیرهای موجود
    ROUTE_OUR_TEAM,  # اضافه شده
)
```

### مرحله ۲: اضافه کردن رندرر در `handlers/menu_router.py`

فایل `handlers/menu_router.py` رو باز کنید و تغییرات زیر رو انجام بدید:

```python
# ۱. وارد کردن مسیر جدید:
from utils.navigation import (
    # ... مسیرهای موجود
    ROUTE_OUR_TEAM,  # اضافه شده
)

# ۲. اضافه کردن تابع رندرر:
async def _render_our_team(callback: CallbackQuery, arg: str | None) -> None:
    text = \"\"\"👥 تیم تراز
    
    ما گروهی از مهندسان نرمافزار، طراحان UX و متخصصان کسبوکار هستیم که باور داریم 
    نرمافزار ERP باید ساده، قدرتمند و در دسترس همه باشد.
    
    🎯 اعضای کلیدی:
    • علی رضایی - مدیر فنی
    • سارا محمدی - مدیر محصول
    • رضا کریمی - مهندس ارشد
    • مریم حسینی - مدیر پشتیبانی
    
    📍 دفتر ما: تهران، ونک\"\"\"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=\"🏠 منوی اصلی\", callback_data=make_callback(ROUTE_MAIN_MENU))],
        [InlineKeyboardButton(text=\"📞 تماس\", callback_data=make_callback(ROUTE_CONTACT))],
    ])
    
    await render_screen(callback, text, keyboard)

# ۳. اضافه کردن به جدول مسیرها:
ROUTE_HANDLERS: dict[str, RendererT] = {
    # ... مسیرهای موجود
    ROUTE_OUR_TEAM: _render_our_team,  # اضافه شده
}
```

### مرحله ۳: اضافه کردن دکمه در `content.json`

فایل `content.json` رو ویرایش کنید:

```json
{
  "screens": {
    "main_menu": {
      "text": "🏠 منوی اصلی\\nمیخوای چی بررسی کنی؟",
      "buttons": [
        [
          {
            "text": "📦 محصولات ما",
            "route": "products_list"
          }
        ],
        [
          {
            "text": "💰 پلنهای قیمتی",
            "route": "pricing_list"
          }
        ],
        [
          {
            "text": "🏢 درباره ما",
            "route": "about"
          }
        ],
        [
          {
            "text": "👥 تیم ما",  // دکمه جدید
            "route": "our_team"   // مسیر جدید
          }
        ],
        [
          {
            "text": "🚀 درخواست دمو",
            "route": "demo_intro"
          }
        ]
      ]
    },
    
    // اضافه کردن صفحه جدید به screens
    "our_team": {
      "text": "👥 تیم تراز\\n\\nما گروهی از مهندسان نرمافزار، طراحان UX و متخصصان کسبوکار هستیم...",
      "buttons": [
        [
          {
            "text": "📞 تماس با ما",
            "route": "contact"
          }
        ],
        [
          {
            "text": "🏠 منوی اصلی",
            "route": "main_menu"
          }
        ]
      ]
    }
  }
}
```

### مرحله ۴: آپدیت `content/loader.py`

اگر از JSON برای متن صفحه استفاده میکنید، `loader.py` به صورت خودکار صفحه جدید رو میخونه.

### مرحله ۵: اضافه کردن دکمه به ریپلای کیبورد (اختیاری)

اگر میخوایم دکمه "تیم ما" در ریپلای کیبورد هم باشه:

```json
{
  "reply_keyboard": {
    "buttons": [
      {
        "text": "📞 تماس / پشتیبانی",
        "action": "contact"
      },
      {
        "text": "🏠 منوی اصلی",
        "action": "main_menu"
      },
      {
        "text": "👥 تیم ما",
        "route": "our_team"  // استفاده از route به جای action
      }
    ]
  }
}
```

## ۳. مثال پیچیدهتر: صفحه محصولات ویژه با پارامتر

### مرحله ۱: تعریف مسیر پارامتری

```python
# در utils/navigation.py
ROUTE_SPECIAL_PRODUCT = "menu:special_product"  # نیاز به :<product_id>

# در ROUTE_MAP
"special_product": ROUTE_SPECIAL_PRODUCT,

# در PARENT_ROUTES (بازگشت به لیست محصولات ویژه)
ROUTE_SPECIAL_PRODUCT: "menu:special_products",

# در _ALL_ROUTES
ROUTE_SPECIAL_PRODUCT,
```

### مرحله ۲: رندرر با پارامتر

```python
# در handlers/menu_router.py
async def _render_special_product(callback: CallbackQuery, arg: str | None) -> None:
    if not arg:
        await _render_special_products_list(callback, None)
        return
    
    # بر اساس arg محصول رو پیدا کن
    special_product = get_special_product_by_id(arg)
    if not special_product:
        await _render_special_products_list(callback, None)
        return
    
    text = f\"{special_product['title']}\\n\\n{special_product['description']}\"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=\"🚀 درخواست دمو\", 
                             callback_data=make_callback(ROUTE_DEMO_FOR_PRODUCT, arg))],
        [InlineKeyboardButton(text=\"🔙 بازگشت\", 
                             callback_data=make_callback(ROUTE_SPECIAL_PRODUCTS))],
    ])
    
    await render_screen(callback, text, keyboard)

# اضافه کردن به ROUTE_HANDLERS
ROUTE_HANDLERS[ROUTE_SPECIAL_PRODUCT] = _render_special_product
```

### مرحله ۳: JSON برای محصولات ویژه

```json
{
  "special_products": [
    {
      "id": "premium_crm",
      "title": "🏆 CRM پرمیوم",
      "description": "نسخه پیشرفته CRM با هوش مصنوعی...",
      "buttons": [
        {
          "text": "🚀 درخواست دمو",
          "route": "demo_for_product",
          "arg": "premium_crm"
        }
      ]
    }
  ],
  
  "screens": {
    "special_products": {
      "text": "⭐ محصولات ویژه\\n\\nمحصولات پیشرفته ما برای کسبوکارهای بزرگ:",
      "buttons": [
        [
          {
            "action": "list_special_products"  // این رو در loader.py توسعه بدید
          }
        ],
        [
          {
            "text": "🏠 منوی اصلی",
            "route": "main_menu"
          }
        ]
      ]
    }
  }
}
```

## ۴. توسعه `content/loader.py` برای اکشنهای جدید

اگر در JSON از `action` جدید استفاده کردید، باید `loader.py` رو توسعه بدید:

```python
def _build_keyboard(button_rows, ...):
    for btn in row:
        action = btn.get("action")
        
        if action == "list_special_products":
            # دکمه‌های محصولات ویژه رو ایجاد کن
            for product in special_products:
                rows.append([InlineKeyboardButton(
                    text=product["title"],
                    callback_data=make_callback(ROUTE_SPECIAL_PRODUCT, product["id"]),
                )])
            continue
```

## ۵. تست کردن تغییرات

۱. **تست واحد**: بعد از هر تغییر کوچک بات رو ریاستارت کنید
۲. **تست دکمهها**: همه دکمهها رو توی چت تست کنید
۳. **تست بازگشت**: دکمه Back رو تست کنید
۴. **تست ریپلای کیبورد**: اگر اضافه کردید تست کنید

## ۶. خطاهای رایج و راهحل

### خطا: `No renderer registered for route`
معنی: مسیر تعریف شده اما رندرر اضافه نشده
راهحل: مطمئن شید `ROUTE_HANDLERS` رو آپدیت کردید

### خطا: دکمه کار نمیکنه
معنی: callback_data درست ساخته نشده
راهحل: `make_callback(route, arg)` رو چک کنید

### خطا: متن صفحه نمایش داده نمیشه
معنی: صفحه در `SCREENS` تعریف نشده
راهحل: مطمئن شید صفحه رو در JSON اضافه کردید

## ۷. بهترین روشها

۱. **نامگذاری**: از نامهای واضح استفاده کنید (`our_team` نه `ot`)
۲. **مستندسازی**: کدها رو کامنت کنید
۳. **تست تدریجی**: اول مسیر ساده اضافه کنید بعد پیچیده
۴. **پشتیبانگیری**: قبل از تغییرات از فایلها بکاپ بگیرید
۵. **استفاده از JSON**: تا جای ممکن متنها رو در JSON نگه دارید

## ۸. مثال کامل: راهاندازی سریع

برای اضافه کردن صفحه جدید "وبلاگ":

```bash
# ۱. navigation.py آپدیت کنید
# ۲. menu_router.py آپدیت کنید  
# ۳. content.json آپدیت کنید
# ۴. بات رو ریاستارت کنید
# ۵. تست کنید
```

با این روش میتونید هر نوع صفحه و دکمه جدیدی رو به راحتی اضافه کنید!