from bs4 import BeautifulSoup
import requests
import streamlit as st

st.set_page_config(
    page_title="ParadiseFilter Bot & Content Generator",
    page_icon="🚗",
    layout="centered",
)

st.title("🤖 ربات هوشمند پارادایس فیلتر (استخراج خودکار و ارسال به بله)")
st.write(
    "فقط لینک محصول را وارد کنید؛ ربات عنوان، قیمت، مشخصات و تصویر را به صورت"
    " خودکار استخراج کرده و به بله ارسال می‌کند."
)

# ----------------- تنظیمات توکن و مقصد در بله -----------------
with st.expander("⚙️ تنظیمات اتصال به ربات بله (توکن و مقصد)"):
  if "ble_token" not in st.session_state:
    st.session_state.ble_token = ""

  token_input = st.text_input(
      "🔑 توکن ربات بله (Bot Token):",
      value=st.session_state.ble_token,
      type="password",
      placeholder="توکن ربات خود را اینجا وارد کنید...",
  )

  chat_id_input = st.text_input(
      "🆔 آیدی کانال یا شناسه مقصد (Chat ID):",
      value="@ParadiseFilter",
      placeholder="مثلاً @ParadiseFilter",
  )

  if st.button("💾 ذخیره تنظیمات"):
    st.session_state.ble_token = token_input
    st.success("تنظیمات با موفقیت ذخیره شد!")

# ----------------- بخش دریافت لینک محصول -----------------
url = st.text_input(
    "🔗 لینک محصول در سایت پارادایس فیلتر:",
    placeholder="https://paradisefilter.ir/product/...",
)

if url:
  try:
    with st.spinner(
        "در حال استخراج هوشمند اطلاعات و تصاویر از سایت پارادایس..."
    ):
      headers = {
          "User-Agent": (
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
              " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
          )
      }
      response = requests.get(url, headers=headers)
      response.raise_for_status()

      soup = BeautifulSoup(response.text, "html.parser")

      # ۱. استخراج دقیق عنوان محصول (اولویت با h1 و تگ‌های ووکامرس)
      product_title = ""
      title_elem = soup.select_one(
          "h1.product_title, h1.entry-title, .product-title, h1"
      )
      if title_elem:
        product_title = title_elem.get_text(strip=True)
      else:
        product_title = "فیلتر هوا پارادایس"

      # ۲. استخراج دقیق قیمت (حتی قیمت‌های تخفیف‌خورده یا معمولی)
      price_text = "تماس بگیرید"
      price_elem = soup.select_one(
          "p.price ins bdi, p.price bdi, .summary p.price, span.price"
      )
      if price_elem:
        p_val = price_elem.get_text(strip=True)
        if p_val:
          # پاکسازی اعداد و اضافه کردن تومان اگر نداشت
          price_text = (
              p_val if "تومان" in p_val or "ریال" in p_val else f"{p_val} تومان"
          )

      # ۳. استخراج مشخصات فنی (جدول مشخصات محصول)
      specs = {}
      spec_rows = soup.select(
          "table.shop_attributes tr, .product-attributes tr, .woocommerce-product-attributes tr"
      )
      for row in spec_rows:
        cols = row.find_all(["th", "td"])
        if len(cols) == 2:
          k = cols[0].get_text(strip=True)
          v = cols[1].get_text(strip=True)
          specs[k] = v

      # ۴. استخراج تصویر اصلی محصول با کیفیت بالا
      image_url = ""
      # بررسی تگ‌های تصویر گالری ووکامرس
      img_elem = soup.select_one(
          ".woocommerce-product-gallery__image img, .product-image img,"
          " .wp-post-image, .images img"
      )
      if img_elem:
        image_url = (
            img_elem.get("data-large_image")
            or img_elem.get("data-src")
            or img_elem.get("src")
        )

      if image_url:
        if image_url.startswith("//"):
          image_url = "https:" + image_url
        elif image_url.startswith("/"):
          image_url = "https://paradisefilter.ir" + image_url

    st.success("✅ اطلاعات و تصویر محصول با موفقیت استخراج شد!")

    # ساخت مشخصات فنی کوتاه کلیدی
    specs_summary = ""
    if specs:
      for k, v in list(specs.items())(
          if hasattr(specs.items(), "__iter__") else specs.items()
      ):
        pass
      # برداشتن ۳ مورد اول مشخصات
      count = 0
      for k, v in specs.items():
        if count < 3:
          specs_summary += f"• __{k}:__ {v}\n"
          count += 1
    else:
      specs_summary = "• __اصالت و کیفیت:__ تضمین شده توسط پارادایس فیلتر\n"

    # هشتگ‌های فراگیر فارسی و انگلیسی
    hashtags = (
        "#فیلتر_هوا #Cabin_Filter #Air_Filter #پارادایس_فیلتر #ParadiseFilter"
        " #لوازم_یدکی #قطعات_یدکی #AutoParts #SpareParts #فیلترهوا_خودرو"
        " #جنیون_پارت #GenuineParts #خرید_آنلاین #فیلتر_خودرو #CarFilter"
    )

    # افزودن هوشمند هشتگ برندها بر اساس نام محصول
    if "هایما" in product_title or "Haima" in product_title:
      hashtags += " #هایما #Haima"
    if "س S8" in product_title or "S8" in product_title:
      hashtags += " #هایماS8 #Haima_S8"
    if "نیسان" in product_title or "Nissan" in product_title:
      hashtags += " #نیسان #Nissan"
    if "تیانا" in product_title:
      hashtags += " #تیانا #Teana"

    # متن نهایی پست با قالب استاندارد
    clean_post_text = f"""🎯 *{product_title}*  

💰 قیمت: *{price_text}*  

📋 _مشخصات فنی کلیدی:_  
{specs_summary}
🔗 _برای مشاهده جزئیات کامل و ابعاد، محصول را در سایت بررسی کنید._  

🛒 *روش‌های ثبت سفارش و خرید:*  
👉 [ثبت سفارش مستقیم از وب‌سایت پارادایس]({url})  
👉 [پرداخت آنی و خرید امن در بله](https://ble.ir/paradiselinkpay/YOUR_PAY_ID)  
👉 [گفتگو و مشاوره با ادمین](https://ble.ir/paradisefilter)  

🆔 @ParadiseFilter  

{hashtags}"""

    st.subheader("📝 پیش‌نمایش کپشن نهایی:")
    final_post = st.text_area("متن پست:", clean_post_text, height=280)

    if image_url:
      st.image(image_url, width=250, caption="تصویر استخراج‌شده از سایت")

    # دکمه ارسال به بله
    if st.button("🚀 ارسال خودکار عکس و پست به بله"):
      if not st.session_state.ble_token:
        st.error("لطفاً ابتدا توکن ربات بله را در بخش تنظیمات بالا ذخیره کنید!")
      else:
        token = st.session_state.ble_token
        with st.spinner("در حال ارسال عکس و پست به کانال بله..."):
          if image_url:
            api_url = f"https://tapi.bale.ai/bot{token}/sendPhoto"
            payload = {
                "chat_id": chat_id_input,
                "photo": image_url,
                "caption": final_post,
                "parse_mode": "Markdown",
            }
          else:
            api_url = f"https://tapi.bale.ai/bot{token}/sendMessage"
            payload = {
                "chat_id": chat_id_input,
                "text": final_post,
                "parse_mode": "Markdown",
            }

          try:
            r = requests.post(api_url, json=payload)
            res_json = r.json()
            if res_json.get("ok"):
              st.success("✅ پست همراه با تصویر با موفقیت به بله ارسال شد!")
            else:
              st.error(
                  f"❌ خطا در ارسال از سوی بله: {res_json.get('description')}"
              )
          except Exception as api_err:
            st.error(f"خطای ارتباط با سرور بله: {api_err}")

  except Exception as e:
    st.error(f"خطا در پردازش لینک: {e}")
