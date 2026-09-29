# old way in which this code was leaving some data in ending and closing bowser:
for i in range(1, 6):
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
    await asyncio.sleep(5.0)
await browser.close()  # <-- The Panic Switch but now 

#New way 
await page.wait_for_load_state("networkidle", timeout=10000)
while active_requests > 0:
    await asyncio.sleep(0.5) # <-- this code block garuntees all data is parsed then closes browser
  

