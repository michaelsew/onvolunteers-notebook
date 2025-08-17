import asyncio
from playwright.async_api import async_playwright
import getpass
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

async def login(browser, username, password):
    page = await browser.new_page()

    logging.debug("Navigating to http://sfx.onvolunteers.com ...")
    await page.goto("http://sfx.onvolunteers.com")

    logging.debug("Clicking Administrator Click Here button ...")
    await page.get_by_role("link", name="Administrator Click Here ").click()
    logging.debug("Waiting for Administrator Login screen ... OK")
    await page.wait_for_selector("text=Administrator Login")

    logging.debug("Filling username ...")
    await page.get_by_placeholder("username or email").fill(username)
    logging.debug("Filling password ...")
    await page.get_by_placeholder("password").fill(password)

    logging.debug("Clicking Login button ...")
    await page.get_by_role("link", name="Login").click()

    logging.debug("Waiting for successful login navigation ...")
    await page.wait_for_url("https://portal.onvolunteers.com/Default.aspx")

    logging.info("Successfully logged in.")

    return page


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # Get username and password from environment variables or prompt the user
        username = os.environ.get("OV_USERNAME")
        password = os.environ.get("OV_PASSWORD")

        if not username or not password:
            logging.info("Environment variables OV_USERNAME and OV_PASSWORD not found, prompting for credentials.")
            username = input("Please enter your username: ")
            password = getpass.getpass("Please enter your password: ")

        page = await login(browser, username, password)

        logging.debug("Hovering over Reports menu ...")
        await page.get_by_role("link", name=" Reports").hover()

        logging.debug("Clicking Built-in Reports link ...")
        await page.get_by_role("link", name="Built-in Reports").click()

        logging.debug("Waiting for reports page to load ...")
        await page.wait_for_url("https://portal.onvolunteers.com/Report.aspx")

        logging.debug("Getting report options from combobox ...")
        report_options_text = await page.get_by_role("combobox").inner_text()
        report_options = report_options_text.splitlines()

        logging.info("Available reports:")
        for option in report_options:
            if option != "Select Report":
                logging.debug(option)

        logging.debug("Selecting 'User Volunteer Hours' report ...")
        await page.get_by_role("combobox").select_option(label="User Volunteer Hours")

        logging.debug("Clicking Generate Report button ...")
        await page.get_by_role("link", name="Generate Report").click()

        logging.debug("Waiting for report generation (5 seconds) ...")
        await asyncio.sleep(5)
        logging.debug("Taking screenshot: report.png ... OK")
        await page.screenshot(path="report.png")

        logging.debug("Waiting for 'Close' button to appear ...")
        await page.wait_for_selector("text=Close")
        logging.info("Report generated successfully. 'Close' button found.")

        logging.debug("Clicking 'Close' button ...")
        await page.wait_for_load_state("networkidle") # Wait for network to be idle
        await page.get_by_text("Close").click()
        logging.info("Clicked 'Close' button. Returned to report selection.")

        logging.info("The browser will close in 5 seconds.")
        await asyncio.sleep(5)

        # await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
