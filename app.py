from bs4 import BeautifulSoup
import requests
import streamlit as st

st.set_page_config(
    page_title="ParadiseFilter Bot & Content Generator",
    page_icon="🚗",
    layout="centered",
)

st.title("🤖 ربات تخصصی پست‌ساز و ارسال به بله - پارادایس فیلتر")
st.write(
    "لینک محصول را وارد کنید، کپشن استاندارد و فراگیر را بسازید و با اتصال توکن"
    " ربات، مستقیماً به بله ارسال کنید."
)

# ----------------- تنظیمات توکن ربات بله با قابلیت ذخیره (Session State) -----------------
with st.expander("⚙️ تنظیمات اتصال به ربات بله (توکن)"):
  if "ble_token" not in st.session_state:
    st.session_state.ble_token = ""

  token_input = st.text_input(
      "🔑 توکن ربات بله (Bot Token):",
      value=st.session_state.ble_token,
      type="password",
      placeholder="توکن ربات خود را اینجا وارد کنید...",
  )

  chat_id_input = st.text_input(
      "🆔 شناسه چت یا کانال مقصد (Chat ID / Channel Username):",
      value="@ParadiseFilter",
      placeholder="مثلا @ChannelName یا آیدی عددی",
  )

  if st.button("💾 ذخیره توکن"):
    st.session_state.ble_token = token_input
    st.success("توکن ربات با موفقیت ذخیره شد!")

# ----------------- بخش دریافت لینک محصول -----------------
url = st.text_input(
    "🔗 لینک محصول در سایت پارادایس فیلتر:",
    placeholder="https://paradisefilter.ir/product/...",
)

if url:
  try:
    with st.spinner("در حال استخراج اطلاعات و تصاویر از سایت..."):
      headers = {
          "User-Agent": (
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
              " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
          )
      }
      response = requests.get(url, headers=headers)
      response.raise_for_status()

      soup = BeautifulSoup(response.text, "html.parser")

      # استخراج عنوان
      title_tag = soup.find("h1") or soup.find(
          "div", class_="product-title"
      ) or soup.find("title")
      product_title = (
          title_tag.get_text(strip=True)
          if title_tag
          else "فیلتر هوا پارادایس"
      )

      # استخراج قیمت
      price_text = "تماس بگیرید"
      price_selectors = [
          "p.price ins bdi",
          "p.price bdi",
          "span.price",
          ".amount",
          ".product-price",
      ]
      for selector in price_selectors:
        p_tag = soup.select_one(selector)
        if p_tag:
          cleaned_price = p_tag.get_text(strip=True)
          if cleaned_price:
            price_text = f"{cleaned_price} تومان"
            break

      if price_text == "تماس بگیرید":
        for tag in soup.find_all(
            ["span", "div", "p"], text=lambda t: t and "تومان" in t
        ):
          txt = tag.get_text(strip=True)
          if len(txt) < 30:
            price_text = txt
            break

      # استخراج جدول مشخصات فنی
      specs = {}
      spec_rows = soup.select("table.shop_attributes tr, .product-attributes tr")
      for row in spec_rows:
        cols = row.find_all(["th", "td"])
        if len(cols) == 2:
          key = cols[0].get_text(strip=True)
          val = cols[1].get_text(strip=True)
          specs[key] = val

      # استخراج تصاویر
      images = []
      img_tags = soup.select(
          ".woocommerce-product-gallery__image img, .product-gallery img,"
          " .gallery img, .images img"
      )
      for img in img_tags:
        img_url = img.get("src") or img.get("data-src")
        if img_url and img_url not in images:
          if img_url.startswith("//"):
            img_url = "https:" + img_url
          elif img_url.startswith("/"):
            img_url = "https://paradisefilter.ir" + img_url
          images.append(img_url)

    st.success("اطلاعات محصول با موفقیت استخراج شد!")

    # نمایش تصاویر
    if images:
      with st.expander("🖼️ مشاهده آلبوم تصاویر محصول"):
        cols = st.columns(min(len(images), 3))
        for idx, img_url in enumerate(images):
          with cols[idx % len(cols)]:
            st.image(img_url, use_container_width=True)

    # ساخت مشخصات فنی کوتاه کلیدی
    specs_summary = ""
    if specs:
      for k, v in list(specs.items())[:3]:
        specs_summary += f"• __{k}:__ {v}\n"
    else:
      specs_summary = "• __اصالت و کیفیت:__ تضمین شده توسط پارادایس فیلتر\n"

    # هشتگ‌های فراگیر فارسی و انگلیسی
    hashtags = (
        "#فیلتر_هوا #Cabin_Filter #Air_Filter #پارادایس_فیلتر #ParadiseFilter"
        " #لوازم_یدکی #قطعات_یدکی #AutoParts #SpareParts #فیلترهوا_خودرو"
        " #جنیون_پارت #GenuineParts #خرید_آنلاین #فیلتر_خودرو #CarFilter"
    )

    # افزودن هوشمند هشتگ‌های مرتبط با خودرو بر اساس عنوان
    if "نیسان" in product_title or "Nissan" in product_title:
      hashtags += " #نیسان #Nissan"
    if "تیانا" in product_title:
      hashtags += " #تیانا #Teana"
    if "آلتیما" in product_title:
      hashtags += " #آلتیما #Altima"

    # متن نهایی پست با تکنیک‌های کپشن‌نویسی استاندارد
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

    st.subheader("📝 متن نهایی آماده برای انتشار:")
    final_post = st.text_area("متن پست:", clean_post_text, height=300)

    # دکمه ارسال مستقیم به بله
    if st.button("🚀 ارسال مستقیم پست به بله"):
      if not st.session_state.ble_token:
        st.error(
            "لطفاً ابتدا توکن ربات بله را در بخش تنظیمات بالا وارد و ذخیره کنید!"
        )
      else:
        with st.spinner("در حال ارسال پیام به بله..."):
          token = st.session_state.ble_token
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
              st.success("✅ پست با موفقیت به بله ارسال شد!")
            else:
              st.error(f"❌ خطا در ارسال از سوی بله: {res_json}")
          except Exception as api_err:
            st.error(f"خطای ارتباط با سرور بله: {api_err}")

  except Exception as e:
    st.error(f"خطا در پردازش لینک: {e}")
