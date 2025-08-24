#!/usr/bin/env python
"""
This script logs in to OnVolunteers and provides an interactive way to generate reports.
"""

import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv(dotenv_path='ov.env')

async def main():
    """
    Main function to run the script.
    """
    headless_mode = os.getenv("OV_HEADLESS", "false").lower() in ["true", "1"]
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless_mode)
        page = await browser.new_page()

        # Navigate to the login page
        await page.goto("http://sfx.onvolunteers.com")
        await page.wait_for_load_state('networkidle')

        # Click the "Administrator Click Here" link
        await page.get_by_text("Administrator Click Here").click()
        await page.wait_for_load_state()

        # Get username and password from environment variables
        username = os.getenv("OV_USERNAME")
        password = os.getenv("OV_PASSWORD")

        if not username or not password:
            print("Please set the OV_USERNAME and OV_PASSWORD environment variables.")
            await browser.close()
            return

        # Fill in the username and password
        await page.get_by_placeholder("username or email").fill(username)
        await page.get_by_placeholder("password").fill(password)

        # Click the login button
        await page.get_by_role("link", name="Login").click()

        # Wait for navigation to complete
        await page.wait_for_url("https://portal.onvolunteers.com/Default.aspx")

        print("Successfully logged in to SFX OnVolunteers.")

        # Check if we need to switch to the admin portal
        switch_to_admin_link = page.locator('a[href="Switch.aspx?p=0"]')
        if await switch_to_admin_link.is_visible():
            print("Switching to Admin Portal...")
            await switch_to_admin_link.click()
            await page.wait_for_url("https://portal.onvolunteers.com/Default.aspx")

        # Verify we are in the admin portal
        switch_to_parent_link = page.locator('a[href="Switch.aspx?p=1"]')
        if not await switch_to_parent_link.is_visible():
            print("Could not verify that we are in the admin portal. Exiting.")
            await browser.close()
            return

        print("Successfully in the Admin Portal.")

        # Hover over the "Reports" menu
        await page.get_by_role("link", name=" Reports").hover()

        # Click the "Built-in Reports" link
        await page.get_by_role("link", name="Built-in Reports").click()

        # Wait for the reports page to load
        await page.wait_for_url("https://portal.onvolunteers.com/Report.aspx")

        while True:
            # Get the report options from the combobox
            report_options_text = await page.locator("#ddlReport").inner_text()
            report_options = report_options_text.split('\n')

            print("\nAvailable reports:")
            for i, option in enumerate(report_options):
                if option != "Select Report":
                    print(f"{i}. {option}")
            print(f"{len(report_options)}. exit")


            choice = input("\nEnter the number of the report you want to generate: ")

            if choice == str(len(report_options)) or choice.lower() == 'exit':
                await browser.close()
                print("Exiting...")
                break

            try:
                choice_index = int(choice)
                selected_report = report_options[choice_index]
                print(f"\nYou selected: {selected_report}")

                await page.locator('button[data-id="ddlReport"]').click()
                await page.locator('.dropdown-menu.open').get_by_role("option", name=selected_report, exact=True).click()

                if selected_report == "User Volunteer Hours":
                    # Get activity options
                    print("Clicking on the activity dropdown...")
                    await page.locator('button[data-id="ddlActivity"]').click()
                    print("Activity dropdown clicked.")
                    
                    print("Getting activity options...")
                    activity_options_elements = await page.locator('button[data-id="ddlActivity"] ~ .dropdown-menu.open .text').all()
                    print(f"Found {len(activity_options_elements)} activity options.")
                    activity_options = [await el.inner_text() for el in activity_options_elements]

                    print("\nAvailable activities:")
                    for i, option in enumerate(activity_options):
                        print(f"{i}. {option}")

                    activity_choice = input("\nEnter the number of the activity: ")
                    selected_activity = activity_options[int(activity_choice)]
                    await page.locator(f'.dropdown-menu.open .text:has-text("{selected_activity}")').click()
                    print(f"\nYou selected activity: {selected_activity}")

                    # Generate report
                    await page.get_by_role("link", name="Generate Report").click()
                    
                    # Wait for the report to be generated, then close it
                    # This assumes a "Close" button appears. If not, this will need adjustment.
                    print("\nReport generated. Closing the report...")
                    await page.locator('button[data-dismiss="modal"]:has-text("Close")').click()
                    print("Report closed.")

                else:
                    await page.get_by_role("link", name="Generate Report").click()
                    # This assumes a "Close" button appears. If not, this will need adjustment.
                    print("\nReport generated. Closing the report...")
                    await page.locator('button[data-dismiss="modal"]:has-text("Close")').click()
                    print("Report closed.")


            except (ValueError, IndexError):
                print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
