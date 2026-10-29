from bs4 import BeautifulSoup
import requests
import streamlit as st

st.set_page_config(page_title="تولیدکننده پست هوشمند پارادایس", page_icon="🚗")

st.title("🚗 ربات تخصصی تولید پست پارادایس فیلتر")
st.write(
    "لینک محصول را وارد کنید تا پست اختصاصی و از نظر بصری جذاب برای همان"
    " پلتفرم آماده شود."
)

url = st.text_input("لینک صفحه محصول (URL):")

# منوی انتخاب پلتفرم با در نظر گرفتن نوع جذابیت بصری
platform = st.selectbox(
    "انتخاب پلتفرم مقصد (بر اساس ساختار بصری):",
    (
        "📸 اینستاگرام (آلبوم تصاویر + کپشن جذاب و هشتگ‌گذاری مدرن)",
        "📱 پیام‌رسان بله / سروش (پست کانالی مرتب با باکس‌های مشخصات)",
        "💬 واتس‌اپ (متن تمیز، خلاصه و بولدشده مناسب ارسال سریع)",
    ),
)

if st.button("✨ تولید پست متناسب با پلتفرم"):
  if url:
    with st.spinner("در حال استخراج هوشمند اطلاعات..."):
      headers = {
          "User-Agent": (
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
              " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
          )
      }
      try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
          soup = BeautifulSoup(response.text, "html.parser")

          # استخراج عناوین و مشخصات ثابت
          title_el = soup.find("h1")
          title = (
              title_el.get_text(strip=True)
              if title_el
              else "فیلتر هوا پارادایس"
          )

          price_el = soup.find("span", class_="amount") or soup.find(
              "div", class_="price"
          )
          price = (
              price_el.get_text(strip=True) if price_el else "تماس بگیرید"
          )

          images = []
          for img in soup.select(
              ".woocommerce-product-gallery__image img, .product-gallery img,"
              " .woocommerce-Tabs-panel img, img.wp-post-image"
          ):
            img_url = img.get("src") or img.get("data-src")
            if img_url and img_url not in images:
              if "-300x300" in img_url:
                img_url = img_url.replace("-300x300", "")
              images.append(img_url)

          specs = {}
          for row in soup.select(
              "table.woocommerce-product-attributes tr, .product-attributes tr,"
              " .spec-table tr"
          ):
            cols = row.find_all(["th", "td"])
            if len(cols) >= 2:
              specs[cols[1].get_text(strip=True)] = cols[0].get_text(strip=True)

          product_type = specs.get("نوع محصول", "وارداتی")
          packaging = specs.get("بسته‌بندی", "جعبه اصلی")
          brand = specs.get("برند", "GENUINE")
          compatible_cars = specs.get("مناسب خودروهای", "")

          clean_type = product_type.replace(" ", "").replace("‌", "")
          clean_pkg = packaging.replace(" ", "").replace("‌", "")
          clean_brand = brand.replace(" ", "").replace("/", "")

          car_tags = ""
          if "NISSAN" in compatible_cars.upper() or "نیسان" in title:
            car_tags += "#نیسان #آلتیما #تیانا "
          if "HYUNDAI" in compatible_cars.upper():
            car_tags += "#هیوندای #سوناتا #توسان "
          if "KIA" in compatible_cars.upper():
            car_tags += "#کیا #اسپورتیج "

          hashtags = (
              f"#{clean_type} #{clean_pkg} #{clean_brand} {car_tags}#فیلترهوا"
              " #لوازم_یدکی #پارادایس_فیلتر"
          )

          specs_text = ""
          for k, v in specs.items():
            specs_text += f"🔹 {k} : {v}\n"

          st.success("✅ پست جذاب شما آماده شد!")

          # ۱. خروجی اینستاگرام (تمرکز روی جذب مخاطب بصری، هشتگ‌های انتهای کار و ساختار اسلایدی)
          if "اینستاگرام" in platform:
            st.subheader("📸 خروجی بصری مخصوص اینستاگرام")
            post_output = f"""🔥 معرفی محصول جدید در پارادایس فیلتر

📌 {title}

💰 قیمت ویژه: {price}

📑 مشخصات فنی کالا:
{specs_text}
🛒 ثبت سفارش سریع از طریق لینک موجود در بیو پیج:
{url}

{hashtags}"""
            st.text_area("کپشن آماده اینستاگرام:", post_output, height=250)
            st.info(
                f"💡 پیشنهاد بصری: برای این پست از {len(images)} تصویر گالری و"
                " بنرهای راهنمای سازگاری خودرو به صورت اسلایدی (Carousel)"
                " استفاده کنید."
            )
            for idx, img in enumerate(images, 1):
              st.write(f"لینک تصویر {idx}: {img}")

          # ۲. خروجی بله و سروش (تمرکز روی کادربندی کانالی، نظم بصری بالا و فونت‌های تمیز)
          elif "بله" in platform:
            st.subheader("📱 خروجی کانالی مخصوص بله / سروش")
            post_output = f"""✨ **{title}** ✨

━━━━━━━━━━━━━━━
💵 **قیمت مصرف‌کننده:** {price}
━━━━━━━━━━━━━━━

🛠 **اطلاعات و مشخصات:**
{specs_text}
🔗 **لینک مشاهده و خرید آنلاین:**
{url}

{hashtags}"""
            st.text_area("متن کانال:", post_output, height=250)
            if images:
              st.image(
                  images[0],
                  width=350,
                  caption="بنر اصلی جهت انتشار در بالای پست",
              )

          # ۳. خروجی واتس‌اپ (خلاصه، خوانا در موبایل و به دور از شلوغی بیش از حد)
          else:
            st.subheader("💬 خروجی بهینه برای واتس‌اپ")
            post_output = f"""*🎯 {title}*

💰 *قیمت:* {price}

📋 *مشخصات اصلی:*
{specs_text}
🔗 *لینک خرید مستقیم:* 
{url}"""
            st.text_area("متن واتس‌اپ:", post_output, height=200)

        else:
          st.error("خطا در بارگذاری صفحه. لطفاً لینک را بررسی کنید.")
      except Exception as e:
        st.error(f"خطا در پردازش: {e}")
  else:
    st.warning("لطفاً لینک محصول را وارد کنید.")
