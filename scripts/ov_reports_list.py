
import asyncio
from playwright.async_api import async_playwright

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
        password = input("Please enter your password: ")

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

        # Keep the browser open for a while to see the result
        print("Successfully navigated to the Built-in Reports page. The browser will close in 20 seconds.")
        await asyncio.sleep(20)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
