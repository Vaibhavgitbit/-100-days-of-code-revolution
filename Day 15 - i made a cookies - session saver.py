import asyncio
import json
from playwright.async_api import async_playwright

async def capture_session():
    print("🚀 Initializing The Token Thief Engine...")
    
    async with async_playwright() as p:
        # 1. Establish a persistent local profile directory
        # This acts like a real, dedicated Chrome profile folder on your disk
        user_data_dir = "./browser_session_profile"
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,  # Must be False so you can see and interact with the UI
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        
        page = await context.new_page()
        
        # Target Website — Change this to Blinkit, Zepto, Swiggy, or any target site
        target_url = "https://jiomart.com"
        print(f"🌐 Navigating to {target_url}...")
        await page.goto(target_url, wait_until="domcontentloaded")
        
        print("\n⚡ Bypassing Showroom Barriers ⚡")
        print("1. Set your location / address pincode.")
        print("2. Complete any mobile phone OTP login forms if required.")
        print("3. Click away any initial intrusive offer pop-ups.")
        print("-" * 50)
        
        # 2. The Human Yield Gate
        # Python halts here completely. The browser stays open until you press Enter in the terminal.
        input("👉 PRESS [ENTER] IN THIS TERMINAL once you are fully logged in and your address is set... ")
        
        print("\n📸 Snapping session photograph... Extracting secure tokens...")
        
        # 3. Extract the complete state array
        cookies = await context.cookies()
        
        # 4. Flush the cookies safely to a local storage file
        output_filename = "session_cookies.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=4)
            
        print(f"💾 Success! Stolen session state successfully committed to '{output_filename}'.")
        print("🔒 Dismantling browser sandbox safely.")
        await context.close()

if __name__ == "__main__":
    # Run our async token harvester loop
    asyncio.run(capture_session(
      
    ))
