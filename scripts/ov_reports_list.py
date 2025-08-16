import asyncio
from playwright.async_api import async_playwright
import getpass

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Navigate to the login page
        await page.goto("http://sfx.onvolunteers.com")

        # Click the "Administrator Click Here" link
        await page.get_by_role("link", name="Administrator Click Here ").click()

        # Get username and password from the user
        username = input("Please enter your username: ")
        password = getpass.getpass("Please enter your password: ")

        # Fill in the username and password
        await page.get_by_placeholder("username or email").fill(username)
        await page.get_by_placeholder("password").fill(password)

        # Click the login button
        await page.get_by_role("link", name="Login").click()

        # Wait for navigation to complete
        await page.wait_for_url("https://portal.onvolunteers.com/Default.aspx")

        # Hover over the "Reports" menu
        await page.get_by_role("link", name=" Reports").hover()

        # Click the "Built-in Reports" link
        await page.get_by_role("link", name="Built-in Reports").click()

        # Wait for the reports page to load
        await page.wait_for_url("https://portal.onvolunteers.com/Report.aspx")

        # Get the report options from the combobox
        report_options_text = await page.get_by_role("combobox").inner_text()
        report_options = report_options_text.split('\n')

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