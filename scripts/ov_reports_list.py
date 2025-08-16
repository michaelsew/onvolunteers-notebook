import asyncio
from playwright.async_api import async_playwright
import getpass
import os

async def login(browser, username, password):
    page = await browser.new_page()

    # Navigate to the login page
    await page.goto("http://sfx.onvolunteers.com")

    # Click the "Administrator Click Here" link
    await page.get_by_role("link", name="Administrator Click Here ").click()

    # Fill in the username and password
    await page.get_by_placeholder("username or email").fill(username)
    await page.get_by_placeholder("password").fill(password)

    # Click the login button
    await page.get_by_role("link", name="Login").click()

    # Wait for navigation to complete
    await page.wait_for_url("https://portal.onvolunteers.com/Default.aspx")

    print("Successfully logged in.")

    return page

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # Get username and password from environment variables or prompt the user
        username = os.environ.get("OV_USERNAME")
        password = os.environ.get("OV_PASSWORD")

        if not username or not password:
            print("Environment variables OV_USERNAME and OV_PASSWORD not found, prompting for credentials.")
            username = input("Please enter your username: ")
            password = getpass.getpass("Please enter your password: ")

        page = await login(browser, username, password)

        # Hover over the "Reports" menu
        await page.get_by_role("link", name=" Reports").hover()

        # Click the "Built-in Reports" link
        await page.get_by_role("link", name="Built-in Reports").click()

        # Wait for the reports page to load
        await page.wait_for_url("https://portal.onvolunteers.com/Report.aspx")

        # Get the report options from the combobox
        report_options_text = await page.get_by_role("combobox").inner_text()
        report_options = report_options_text.splitlines()

        print("Available reports:")
        for option in report_options:
            if option != "Select Report":
                print(option)

        # Select the "User Volunteer Hours" report
        await page.get_by_role("combobox").select_option(label="User Volunteer Hours")

        # Click the "Generate Report" button
        await page.get_by_role("link", name="Generate Report").click()

        # Wait for the report to be generated
        await asyncio.sleep(5)
        await page.screenshot(path="report.png")

        # Keep the browser open for a while to see the result
        print("The browser will close in 10 seconds.")
        await asyncio.sleep(10)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())