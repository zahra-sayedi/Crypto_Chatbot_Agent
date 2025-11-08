# (Your entire TEMPLATES dictionary)
TEMPLATES = {
    'en': {
        'price_header': "Current prices for {symbol} (Source: Wallex.ir at {timestamp}):",
        'price_line': "• {quote} ({symbol}): {price}",
        'price_not_found': "Sorry, I couldn't find any markets for the symbol {symbol} on Wallex.ir.",
        'price_api_error': "Sorry, I had trouble connecting to the Wallex.ir API. Please try again later.",
        'price_parse_error': "Sorry, I had trouble understanding the response from the price API.",
        'search_no_results': "Sorry, I couldn't find any web results for that query.",
        'search_api_error': "Sorry, I had trouble connecting to the web search API. (Error: {e})",
        'synth_prompt': "You are a cryptocurrency research assistant. Answer the user's question based *only* on the provided search results. Do not use any prior knowledge. Be concise and helpful. You MUST answer in English.",
        'synth_api_error': "Sorry, I had trouble generating an answer from the search results.",
        'synth_service_unavailable': "Sorry, the text synthesis service is not available.",
        'synth_sources_header': "\n\nSources:\n"
    },
    'fa': {
        'price_header': "قیمت‌های فعلی برای {symbol} (منبع: Wallex.ir در {timestamp}):",
        'price_line': "• {quote} ({symbol}): {price}",
        'price_not_found': "متاسفانه، هیچ بازاری برای نماد {symbol} در Wallex.ir پیدا نشد.",
        'price_api_error': "متاسEOFشتم، در اتصال به API Wallex.ir مشکلی پیش آمد. لطفا بعدا تلاش کنید.",
        'price_parse_error': "متاسفانه، در درک پاسخ API قیمت مشکلی وجود داشت.",
        'search_no_results': "متاسفانه، هیچ نتیجه‌ای در وب برای این پرسش پیدا نکردم.",
        'search_api_error': "متاسفانه، در اتصال به API جستجوی وب مشکلی پیش آمد. (خطا: {e})",
        'synth_prompt': "شما یک دستیار تحقیق ارز دیجیتال هستید. *فقط* بر اساس نتایج جستجوی ارائه‌شده، به سوال کاربر پاسخ دهید. از هیچ دانش قبلی استفاده نکنید. مختصر و مفید باشید. شما *باید* به زبان فارسی پاسخ دهید.",
        'synth_api_error': "متاسفانه، در تولید پاسخ از نتایج جستجو مشکلی پیش آمد.",
        'synth_service_unavailable': "متاسOFنا، سرویس تولید متن در دسترس نیست.",
        'synth_sources_header': "\n\nمنابع:\n"
    }
}

def get_template(lang: str) -> dict:
    """Fetches the template dictionary for a given language, defaulting to 'en'."""
    return TEMPLATES.get(lang, TEMPLATES['en'])