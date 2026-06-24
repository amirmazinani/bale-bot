# 🚀 شروع سریع

آهنگ بات شما را **بدون نوشتن کد** تغییر دهید!

## 📝 ۵ دقیقه‌ای آپ شو

### ۱. منو ساده را تغییر دهید

فایل `content/content.json` را باز کنید و متن `main_menu` را تغییر دهید:

```json
{
  "screens": {
    "main_menu": {
      "text": "🏠 منوی اصلی\n🆕 متن جدید خوش آمد!",
      "buttons": [
        // ... دکمه‌ها
      ]
    }
  }
}
```

بات را ریاستارت کنید:
```bash
python main.py
```

✅ **انجام شد!** منو تغییر یافت!

---

### ۲. دکمه‌ای اضافه کنید

دکمه جدید را به منوی اصلی اضافه کنید:

```json
"main_menu": {
  "buttons": [
    // ... دکمه‌های قبلی
    [
      {
        "text": "🆕 دکمه جدید",
        "route": "new_page"
      }
    ]
  ]
}
```

---

### ۳. صفحه جدید ایجاد کنید

صفحه جدید را تعریف کنید:

```json
"screens": {
  "new_page": {
    "text": "🆕 صفحه جدید\n\nسلام! من یک صفحه جدید هستم.",
    "parent": "main_menu",
    "buttons": [
      [
        {
          "text": "🏠 منوی اصلی",
          "route": "main_menu"
        }
      ]
    ]
  }
}
```

✅ **کمال!** دکمه و صفحه جدید کار می‌کند!

---

## 🎯 ۱۰ مثال عملی

### مثال ۱: صفحه درباره ما

```json
{
  "screens": {
    "about_us": {
      "text": "🏢 درباره ما\n\nما یک شرکت نرم‌افزاری ERP هستیم که به شرکت‌های کوچک و متوسط کمک می‌کند.",
      "parent": "main_menu",
      "buttons": [
        [{"text": "🌐 وب‌سایت", "url": "https://example.com"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    }
  }
}
```

### مثال ۲: صفحه رابط تیم

```json
{
  "screens": {
    "team": {
      "text": "👥 تیم ما\n\n👨‍💼 علی رئیسی - مدیر اجرایی\n👩‍💼 سارا احمدی - مدیر فروش\n👨‍💻 رضا کریمی - CTO\n\n📧 team@example.com",
      "parent": "main_menu",
      "buttons": [
        [{"text": "📧 ایمیل", "url": "mailto:team@example.com"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    }
  }
}
```

### مثال ۳: سایت را در Bale نمایش دهید

```json
{
  "screens": {
    "web_embed": {
      "text": "🌐 وب‌سایت ما\n\nبرای مشاهده وب‌سایت کامل، روی دکمه زیر کلیک کنید.",
      "parent": "main_menu",
      "buttons": [
        [{"text": "🌐 وب‌سایت", "url": "https://example.com"}],
        [{"text": "📱 اپلیکیشن", "url": "https://app.example.com"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    }
  }
}
```

### مثال ۴: منو سه سطحی

```json
{
  "screens": {
    "products_category": {
      "text": "📦 دسته‌بندی محصولات",
      "parent": "main_menu",
      "buttons": [
        [{"text": "🏢 ERP", "route": "products_erp"}],
        [{"text": "📊 تجزیه و تحلیل", "route": "products_analytics"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    },
    
    "products_erp": {
      "text": "🏢 محصولات ERP\n\n• مدیریت فروش\n• مدیریت انبار\n• حسابداری",
      "parent": "products_category",
      "buttons": [
        [{"text": "🚀 درخواست دمو", "route": "demo_intro"}],
        [{"text": "🔙 دسته‌بندی", "route": "products_category"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    },
    
    "products_analytics": {
      "text": "📊 محصولات تجزیه و تحلیل\n\n• گزارشات فروش\n• تحلیل مشتری\n• پیش‌بینی درآمد",
      "parent": "products_category",
      "buttons": [
        [{"text": "🚀 درخواست دمو", "route": "demo_intro"}],
        [{"text": "🔙 دسته‌بندی", "route": "products_category"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    }
  }
}
```

### مثال ۵: کوپن و تخفیف

```json
{
  "screens": {
    "coupons": {
      "text": "🎁 کوپن‌های ویژه\n\n🔴 کوپن SUMMER20: تخفیف ۲۰%\n🔵 کوپن BUSINESS30: تخفیف ۳۰% برای کسب‌وکار\n🟢 کوپن FREE: ۱ ماه رایگان",
      "parent": "main_menu",
      "buttons": [
        [{"text": "🚀 استفاده از کوپن", "route": "demo_intro"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    }
  }
}
```

### مثال ۶: سوالات متداول ساده

```json
{
  "screens": {
    "faq": {
      "text": "❓ سوالات متداول\n\n❓ سوال ۱: قیمت چقدر است؟\n💬 پاسخ: قیمت بر اساس نیاز شرکت متفاوت است.\n\n❓ سوال ۲: تست رایگان دارد؟\n💬 پاسخ: بله! ۲ هفته تست رایگان.\n\n❓ سوال ۳: پشتیبانی ۲۴/۷ دارد؟\n💬 پاسخ: بله! تیم پشتیبانی ما همیشه آنلاین است.",
      "parent": "main_menu",
      "buttons": [
        [{"text": "📞 تماس برای بیشتر", "route": "contact"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    }
  }
}
```

### مثال ۷: مقایسه محصولات

```json
{
  "screens": {
    "comparison": {
      "text": "📊 مقایسه محصولات\n\n| ویژگی | استارتر | حرفه‌ای | سازمانی |\n|-------|---------|--------|--------|\n| ماژول CRM | ✅ | ✅ | ✅ |\n| مدیریت وظایف | ❌ | ✅ | ✅ |\n| پشتیبانی ۲۴/۷ | ❌ | ❌ | ✅ |\n| کاربران | 10 | 50 | نامحدود |",
      "parent": "main_menu",
      "buttons": [
        [{"text": "💰 قیمت‌ها", "route": "pricing_list"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    }
  }
}
```

### مثال ۸: اخبار و اطلاعیه‌ها

```json
{
  "screens": {
    "news": {
      "text": "📰 اخبار و اطلاعیه‌ها\n\n🔴 [جدید] نسخه جدید منتشر شد!\nویژگی‌های جدید: گزارش‌های پیشرفته، API جدید\n\n🔵 [تعمیر] هفته‌ای یک‌بار نگهداری\nهر دوشنبه ساعت ۲ صبح تا ۳ صبح\n\n🟢 [اطلاع] دروس آموزشی منتشر شد\nیاد بگیرید چگونه از سیستم ERP استفاده کنید",
      "parent": "main_menu",
      "buttons": [
        [{"text": "📧 خبرنامه", "url": "https://example.com/newsletter"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    }
  }
}
```

### مثال ۹: شهادات مشتری

```json
{
  "screens": {
    "testimonials": {
      "text": "⭐ شهادات مشتری‌ها\n\n👤 علی رحیمی - شرکت الفا\n⭐⭐⭐⭐⭐\n\"بهترین سیستم ERP که تا حالا استفاده کردم!\"\n\n👤 فاطمه احمدی - شرکت بتا\n⭐⭐⭐⭐⭐\n\"پشتیبانی عالی و پاسخ سریع!\"\n\n👤 رضا کریمی - شرکت گاما\n⭐⭐⭐⭐⭐\n\"به تیم ما کمک زیادی کرد. پیشنهاد می‌کنم!\"",
      "parent": "main_menu",
      "buttons": [
        [{"text": "🚀 شروع کنید", "route": "demo_intro"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    }
  }
}
```

### مثال ۱۰: فرم تماس

```json
{
  "screens": {
    "contact_form": {
      "text": "📋 فرم تماس\n\nبرای دریافت مشاوره رایگان:\n\n📞 تلفن: {phone}\n📧 ایمیل: {email}\n💬 Bale: {bale_username}\n\nیا روی دکمه‌های زیر کلیک کنید:",
      "parent": "main_menu",
      "buttons": [
        [{"text": "📞 تماس", "url": "tel:{phone}"}],
        [{"text": "📧 ایمیل", "url": "mailto:{email}"}],
        [{"text": "💬 Bale", "url": "https://bale.ai/@example"}],
        [{"text": "🏠 منوی اصلی", "route": "main_menu"}]
      ]
    }
  }
}
```

---

## 🎨 Emoji‌های مفید

```
منو: 🏠 🏢 🏭 🏪 🏬 🎯 📍
محصول: 📦 📫 🎁 🎀 ✨ 🌟 💎
قیمت: 💰 💵 💴 💶 💷 🤑 💸
تماس: 📞 📱 ☎️ 📧 ✉️ 💬 📮
درخواست: 🚀 🎯 🔗 ➡️ 👆 👇
متن: ❓ ℹ️ ⭐ ✅ ❌ 🔔 📢
عمومی: 🔙 ↩️ 🔄 ⚙️ 🎮 🎪 🎭
```

---

## ✅ Checklist قبل از تولید

- [ ] تمام `"route"` ها به صفحات موجود اشاره می‌کنند
- [ ] تمام `"parent"` ها صحیح هستند
- [ ] JSON syntax معتبر است (`python -c "import json; json.load(open('content/content.json'))"`)
- [ ] اموجی‌ها درست انتخاب شده‌اند
- [ ] متن‌ها بدون تایپ‌اوروی فارسی هستند
- [ ] لینک‌ها صحیح هستند

---

## 🔍 عیب‌یابی سریع

| مشکل | حل |
|------|-----|
| صفحه نشان نمی‌دهد | صفحه را در `screens` بررسی کنید |
| دکمه کار نمی‌کند | `route` را درست بنویسید و صفحه را ایجاد کنید |
| بات اجرا نمی‌شود | JSON syntax را بررسی کنید |
| متن نمایش داده نمی‌شود | `/n` را به `\n` تغییر دهید |
| Back button کار نمی‌کند | `parent` را اضافه کنید |

---

## 🚀 بعدی

برای تغییرات پیشرفته‌تر:
- ببینید [CONFIGURATION.md](CONFIGURATION.md) برای ساختار کامل
- ببینید [EXTENDING.md](EXTENDING.md) برای اضافه کردن logic جدید

**سوال؟** ببینید [README.md](README.md) 👈
