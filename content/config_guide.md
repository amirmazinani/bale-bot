# راهنمای تنظیم دکمه‌ها در content.json

## ۱. دکمه‌های ریپلای کیبورد (Reply Keyboard)

در بخش `reply_keyboard` می‌توانید دکمه‌ها را اضافه/کم کنید:

```json
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
      "text": "📊 گزارش‌ها",
      "action": "reports"
    },
    {
      "text": "🎯 محصولات ویژه",
      "action": "special_products"
    }
  ]
}
```

**عملکردهای پشتیبانی‌شده:**
- `"action": "main_menu"` - بازگشت به منوی اصلی
- `"action": "contact"` - نمایش اطلاعات تماس
- سایر عملکردها نیاز به توسعه در `handlers/reply_menu.py` دارند

## ۲. دکمه‌های منوی اصلی (Main Menu)

در بخش `screens.main_menu.buttons`:

```json
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
          "text": "🚀 درخواست دمو",
          "route": "demo_intro"
        }
      ],
      [
        {
          "text": "⭐ محصولات ویژه",
          "route": "special_products"
        }
      ]
    ]
  }
}
```

**راهنما:**
- هر آرایه `[]` در `buttons` یک ردیف (row) جداگانه ایجاد می‌کند
- برای ردیف‌های تک‌دکمه‌ای از `[[{...}]]` استفاده کنید
- `"route"` باید یکی از مسیرهای تعریف‌شده در `ROUTE_MAP` باشد

## ۳. مسیرهای موجود در سیستم

```python
ROUTE_MAP = {
    "main_menu":        "menu:main",
    "products_list":    "menu:products", 
    "product_detail":   "menu:product_detail",
    "pricing_list":     "menu:pricing",
    "pricing_detail":   "menu:pricing_detail",
    "about":            "menu:about",
    "demo_intro":       "menu:demo_intro",
    "demo_for_product": "menu:demo_for_product",
    "contact":          "menu:contact",
}
```

## ۴. مثال‌های کاربردی

### الف) اضافه کردن دکمه جدید به ریپلای کیبورد:

```json
{
  "text": "🆘 کمک فوری",
  "action": "emergency_help"
}
```

### ب) کم کردن دکمه از منوی اصلی:

```json
"buttons": [
  [
    {"text": "📦 محصولات ما", "route": "products_list"}
  ],
  [
    {"text": "💰 پلنهای قیمتی", "route": "pricing_list"}
  ],
  [
    {"text": "🏢 درباره ما", "route": "about"}
  ]
  // دکمه درخواست دمو حذف شد
]
```

### ج) تغییر ترتیب دکمه‌ها:

```json
"buttons": [
  [
    {"text": "🚀 درخواست دمو", "route": "demo_intro"}
  ],
  [
    {"text": "📦 محصولات ما", "route": "products_list"}
  ],
  [
    {"text": "💰 پلنهای قیمتی", "route": "pricing_list"}
  ],
  [
    {"text": "🏢 درباره ما", "route": "about"}
  ]
]
```

## ۵. نکات مهم

۱. **تغییرات فوری**: پس از ویرایش `content.json`، باید بات را ری‌استارت کنید
۲. **تست تغییرات**: همیشه تغییرات را در محیط آزمایشی تست کنید
۳. **پشتیبان‌گیری**: از فایل `content.json` پشتیبان بگیرید
۴. **ایجاد مسیر جدید**: برای ایجاد مسیرهای جدید نیاز به توسعه کد دارید

## ۶. محدودیت‌ها فعلی

- دکمه‌های ریپلای کیبورد فقط دو عملکرد `main_menu` و `contact` را پشتیبانی می‌کنند
- برای عملکردهای جدید باید `handlers/reply_menu.py` را توسعه دهید
- مسیرهای جدید نیاز به تعریف در `utils/navigation.py` و `handlers/menu_router.py` دارند