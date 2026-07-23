import asyncio
import os
from playwright.async_api import async_playwright

async def render():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1200, "height": 300}, device_scale_factor=1)
        html_path = os.path.abspath("banner.html")
        await page.goto(f"file:///{html_path.replace('\\\\', '/')}")
        await page.wait_for_timeout(1000) # wait for fonts/rendering
        output_path = os.path.abspath("banner.png")
        await page.screenshot(path=output_path, clip={"x": 0, "y": 0, "width": 1200, "height": 300})
        await browser.close()
        print(f"Banner saved successfully to {output_path}")

if __name__ == "__main__":
    asyncio.run(render())
