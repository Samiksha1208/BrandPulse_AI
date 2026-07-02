import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        print("Navigating to dashboard...")
        await page.goto("http://localhost:8501", wait_until="networkidle")
        
        # Give Streamlit a few seconds to load the charts and data
        print("Waiting for Streamlit to render...")
        await asyncio.sleep(5) 
        
        print("Taking screenshot...")
        await page.screenshot(path="docs/dashboard_screenshot.png", full_page=True)
        
        await browser.close()
        print("Screenshot saved to docs/dashboard_screenshot.png")

if __name__ == "__main__":
    asyncio.run(main())
