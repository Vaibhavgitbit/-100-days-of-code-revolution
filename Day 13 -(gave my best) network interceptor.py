
import asyncio
import json
from playwright.async_api import async_playwright

async def main():
    extracted_products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
       
        # Intercept network responses to capture the product API payload
        async def interceptor(response):
            if response.request.resource_type in ["fetch", "xhr"]:
                try:
                    data = await response.json()
                    # Recursively or directly search for product items in the JSON response
                    # JioMart API structures often place items in lists under keys like 'items', 'products', or data blocks
                    def find_products(obj):
                        if isinstance(obj, dict):
                            for k, v in obj.items():
                                if k == "items" and isinstance(v, list):
                                    for item in v:
                                        if isinstance(item, dict) and item.get("type") == "product":
                                            parse_product_item(item)
                                else:
                                    find_products(v)
                        elif isinstance(obj, list):
                            for item in obj:
                                find_products(item)

                    def parse_product_item(item):
                        name = item.get("name")
                        if not name:
                            return
                       
                        # Extract pricing info safely
                        price_obj = item.get("price", {})
                        effective_price = price_obj.get("effective", {}).get("min", "N/A")
                        marked_price = price_obj.get("marked", {}).get("min", "N/A")
                        currency = price_obj.get("currency_symbol", "₹")
                       
                        # Extract brand
                        brand_name = item.get("brand", {}).get("name", "N/A")
                       
                        # Extract image URL
                        medias = item.get("medias", [])
                        image_url = medias[0].get("url") if medias else ""
                       
                        # Build product URL slug
                        slug = item.get("slug", "")
                        product_url = f"https://www.jiomart.com/p/product/{slug}" if slug else ""

                        product_entry = {
                            "title": name,
                            "brand": brand_name,
                            "price": f"{currency}{effective_price}",
                            "mrp": f"{currency}{marked_price}" if marked_price != "N/A" else "N/A",
                            "image": image_url,
                            "url": product_url
                        }
                       
                        # Avoid duplicates
                        if not any(p["title"] == name for p in extracted_products):
                            extracted_products.append(product_entry)

                    find_products(data)
                except Exception:
                    pass

        page.on("response", interceptor)
       
        print("Opening JioMart...")
        await page.goto("https://www.jiomart.com", wait_until="domcontentloaded")
       
        # --- LOCATION SETUP ---
        WAIT_SECONDS = 25
        print(f"\n[!!!] PAUSING FOR {WAIT_SECONDS} SECONDS. Set your location/pincode now...")
        for remaining in range(WAIT_SECONDS, 0, -1):
            print(f"Resuming automation loop in {remaining} seconds...", end="\r")
            await asyncio.sleep(1)
        print("\nResuming! Scrolling to trigger API payload fetches...\n")

        # Scroll down to trigger lazy-loaded API responses
        for i in range(1, 6):
            print(f"Scrolling down... (Step {i}/5)")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            await asyncio.sleep(5.0)
           
        # Write clean data out
        with open("clean_products.json", "w", encoding="utf-8") as f:
            json.dump(extracted_products, f, indent=4)

        print(f"\nSuccess! Captured {len(extracted_products)} clean products inside 'clean_products.json'.")
        await browser.close()

if __name__ == "__main__":
    asyncio.ru
n(main())
