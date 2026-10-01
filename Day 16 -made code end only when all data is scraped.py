# 1. Complete the scrolling actions
for i in range(1, 6):
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    
# 2. Halt execution until all background API packets land safely
print("Waiting for network streams to settle...")
await page.wait_for_load_state("networkidle")

# 3. Safe to dismantle the engine now
print("All data captured safely. Closing browser.")
await browser.close(

)
