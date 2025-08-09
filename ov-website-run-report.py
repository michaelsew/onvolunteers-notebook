import asyncio
from getpass import getpass # To securely get password input
from playwright.async_api import async_playwright

# --- Configuration ---
# You can set your username here, or leave it as None and you will be prompted to enter it.
# Replace with your actual username or set to None
USERNAME = "mikesew@gmail.com"

# You can set your password here, or leave it as None and you will be prompted to enter it.
# If PASSWORD is None, you will be prompted to enter your password securely.
# Replace with your actual password or set to None
PASSWORD = None

# URL of the login page
LOGIN_URL = "http://sfx.onvolunteers.com"

# --- Get Credentials ---
if USERNAME is None:
    USERNAME = input("Please enter your username: ")

if PASSWORD is None:
    PASSWORD = getpass("Please enter your password: ")

# --- Login Process with Playwright ---
async def login_with_playwright():
    async with async_playwright() as p:
        # Launch a browser (you can choose 'chromium', 'firefox', or 'webkit')
        browser = await p.chromium.launch(headless=False) # headless=False lets you see the browser
        page = await browser.new_page()

        try:
            # Navigate to the login page
            await page.goto(LOGIN_URL)
            print(f"Navigated to {LOGIN_URL}")

            # Click the "Administrator click here" link
            await page.click("#btSwitch")
            print("Clicked 'Administrator click here' link.")

            # Wait for the admin login header to be visible
            admin_login_header = "Administrator Login"
            print(f"Waiting for text '{admin_login_header}' to appear...")
            await page.wait_for_selector(f'text="{admin_login_header}"')
            print("Admin login page confirmed.")

            # Fill in username and password fields
            await page.fill("#tbUsername", USERNAME)
            await page.fill("#tbPassword", PASSWORD)
            print("Entered username and password.")

            # Click the login button
            await page.get_by_role("link", name="Login").click()
            print("Clicked login button.")

            # Wait for the next page to load (you might need to adjust the condition)
            # For example, wait for the URL to change or for a specific element
            await page.wait_for_url(lambda url: url != LOGIN_URL)
            print("Login successful.")

            # You are now logged in. You can perform further actions here.
            # For example, print the current URL to confirm you are on the next page:
            print("Current URL:", page.url)

            # Keep the browser open for a few seconds to see the result
            await page.wait_for_timeout(5000)


        except Exception as e:
            print(f"An error occurred during the login process: {e}")

        finally:
            # Close the browser
            await browser.close()
            print("Browser closed.")

# --- Main execution block ---
if __name__ == "__main__":
    asyncio.run(login_with_playwright())
