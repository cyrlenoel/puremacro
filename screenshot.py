from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file://{os.path.abspath('curso/site/labs/identificacion.html')}")
    page.screenshot(path="screenshot.png", full_page=True)
    browser.close()
