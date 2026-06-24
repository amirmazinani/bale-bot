"""
setup_dynamic.py
================
اسکریپت برای فعال کردن سیستم داینامیک.

استفاده:
python setup_dynamic.py
"""

import shutil
from pathlib import Path

def setup_dynamic_system():
    """سیستم داینامیک رو فعال میکنه."""
    content_dir = Path(__file__).parent / "content"
    
    # ۱. کپی کردن فایل داینامیک
    source = content_dir / "content.dynamic.json"
    destination = content_dir / "content.json"
    
    if not source.exists():
        print("❌ فایل content.dynamic.json پیدا نشد!")
        return False
    
    try:
        shutil.copy2(source, destination)
        print(f"✅ فایل داینامیک کپی شد: {destination}")
    except Exception as e:
        print(f"❌ خطا در کپی کردن: {e}")
        return False
    
    # ۲. بررسی فایلهای ایجاد شده
    files_to_check = [
        "utils/dynamic_navigation.py",
        "handlers/dynamic_menu_router.py", 
        "content/loader.py",
        "handlers/reply_menu.py",
        "main.py"
    ]
    
    print("\n📋 بررسی فایلهای سیستم داینامیک:")
    all_ok = True
    for file_path in files_to_check:
        path = Path(__file__).parent / file_path
        if path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (پیدا نشد!)")
            all_ok = False
    
    if all_ok:
        print("\n🎉 سیستم داینامیک آماده است!")
        print("\n📖 راهنماها:")
        print("  1. content/dynamic_config_guide.md - راهنمای استفاده")
        print("  2. content/how_to_add_new_route.md - اضافه کردن مسیر")
        print("  3. content/config_guide.md - تنظیم دکمهها")
        print("\n🚀 برای شروع:")
        print("  python main.py")
    else:
        print("\n⚠️  برخی فایلها پیدا نشدند. سیستم ممکن است کامل کار نکند.")
    
    return all_ok

def show_usage():
    """نمایش راهنمای استفاده."""
    print("""
🤖 سیستم کاملاً داینامیک بات تراز
    
🔧 قابلیتها:
  • اضافه کردن صفحات جدید بدون کدنویسی
  • تغییر منوها و دکمهها از طریق JSON
  • مسیرهای خودکار
  • دکمههای ریپلای کیبورد داینامیک
    
📁 فایلهای ایجاد شده:
  1. utils/dynamic_navigation.py - سیستم مسیریابی داینامیک
  2. handlers/dynamic_menu_router.py - هندلر صفحات داینامیک  
  3. content/content.dynamic.json - مثال ساختار داینامیک
  4. content/dynamic_config_guide.md - راهنمای کامل
    
🛠️ استفاده:
  python setup_dynamic.py  # فعال کردن سیستم داینامیک
  python main.py          # اجرای بات
    
📝 ویرایش محتوا:
  • فایل content.json رو ویرایش کنید
  • صفحات جدید به screens اضافه کنید
  • دکمههای جدید به buttons اضافه کنید
  • بات رو ریاستارت کنید
    
🎯 مثال اضافه کردن صفحه جدید:
  1. در content.json به screens اضافه کنید:
     "new_page": {
       "text": "متن صفحه",
       "parent": "main_menu",
       "buttons": [...]
     }
     
  2. دکمه به main_menu اضافه کنید:
     {
       "text": "صفحه جدید",
       "route": "new_page"
     }
     
  3. بات رو ریاستارت کنید!
    
ℹ️ برای اطلاعات بیشتر راهنماها رو مطالعه کنید.
    """)

if __name__ == "__main__":
    print("=" * 50)
    print("فعال کردن سیستم کاملاً داینامیک")
    print("=" * 50)
    
    # نمایش راهنما
    show_usage()
    
    # درخواست تایید
    response = input("\nآیا میخواهید سیستم داینامیک رو فعال کنید؟ (y/n): ").strip().lower()
    
    if response == 'y':
        print("\n" + "=" * 50)
        print("در حال فعال کردن سیستم داینامیک...")
        print("=" * 50)
        success = setup_dynamic_system()
        
        if success:
            print("\n✅ سیستم داینامیک با موفقیت فعال شد!")
            print("📚 حتماً راهنماها رو مطالعه کنید.")
        else:
            print("\n❌ خطا در فعال کردن سیستم داینامیک!")
    else:
        print("\n❌ عملیات لغو شد.")
        print("💡 میتوانید بعداً با دستور python setup_dynamic.py سیستم رو فعال کنید.")