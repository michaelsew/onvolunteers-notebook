#!/usr/bin/env python
"""
This script logs in to OnVolunteers and provides an interactive way to generate reports.
"""

import asyncio
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(dotenv_path=os.path.join(SCRIPT_DIR, 'ov.env'))

class ReportGenerator:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def login(self):
        """Logs in to OnVolunteers."""
        # Navigate to the login page
        await self.page.goto("http://sfx.onvolunteers.com")
        await self.page.wait_for_load_state('networkidle')

        # Click the "Administrator Click Here" link
        await self.page.get_by_text("Administrator Click Here").click()
        await self.page.wait_for_load_state()

        # Get username and password from environment variables
        username = os.getenv("OV_USERNAME")
        password = os.getenv("OV_PASSWORD")

        if not username or not password:
            print("Please set the OV_USERNAME and OV_PASSWORD environment variables.")
            return False

        # Fill in the username and password
        await self.page.get_by_placeholder("username or email").fill(username)
        await self.page.get_by_placeholder("password").fill(password)

        # Click the login button
        await self.page.get_by_role("link", name="Login").click()

        # Wait for navigation to complete
        await self.page.wait_for_url("https://portal.onvolunteers.com/Default.aspx")

        print("Successfully logged in to SFX OnVolunteers.")

        # Check if we need to switch to the admin portal
        switch_to_admin_link = self.page.locator('a[href="Switch.aspx?p=0"]')
        if await switch_to_admin_link.is_visible():
            print("Switching to Admin Portal...")
            await switch_to_admin_link.click()
            await self.page.wait_for_url("https://portal.onvolunteers.com/Default.aspx")

        # Verify we are in the admin portal
        switch_to_parent_link = self.page.locator('a[href="Switch.aspx?p=1"]')
        if not await switch_to_parent_link.is_visible():
            print("Could not verify that we are in the admin portal. Exiting.")
            return False

        print("Successfully in the Admin Portal.")
        return True

    async def navigate_to_reports(self):
        """Navigates to the Built-in Reports page."""
        # Hover over the "Reports" menu
        await self.page.get_by_role("link", name=" Reports").hover()

        # Click the "Built-in Reports" link
        await self.page.get_by_role("link", name="Built-in Reports").click()

        # Wait for the reports page to load
        await self.page.wait_for_url("https://portal.onvolunteers.com/Report.aspx")
        print("Successfully navigated to the Built-in Reports page.")

    async def generate_user_volunteer_hours_report(self, activity_id):
        """Generates the 'User Volunteer Hours' report for a specific activity."""
        print(f"Generating 'User Volunteer Hours' report for activity ID: {activity_id}")

        # Select the "User Volunteer Hours" report
        await self.page.locator('button[data-id="ddlReport"]').click()
        await self.page.locator('.dropdown-menu.open').get_by_role("option", name="User Volunteer Hours", exact=True).click()

        # Select the activity
        await self.page.locator('button[data-id="ddlActivity"]').click()
        
        # We can select the option by its value.
        await self.page.locator('#ddlActivity').select_option(str(activity_id))

        # Click on the body to close the dropdown
        await self.page.locator('body').click()

        print(f"Selected activity with ID: {activity_id}")

        # Generate report
        await self.page.get_by_role("link", name="Generate Report").click()
        
        # Wait for the report to be generated, then close it
        print("\nReport generated. Closing the report...")
        await self.page.locator('button[data-dismiss="modal"]:has-text("Close")').click()
        print("Report closed.")

async def run_scripted_actions():
    """Runs a predefined sequence of report generation actions."""
    async with ReportGenerator(headless=True) as report_generator:
        if await report_generator.login():
            await report_generator.navigate_to_reports()
            await report_generator.generate_user_volunteer_hours_report(activity_id=30212) # Parking Patrol 2025-2026
            await report_generator.generate_user_volunteer_hours_report(activity_id=0) # All Activities

async def run_interactive_mode():
    """Runs the original interactive report generation script."""
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

async def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description="Generate reports from OnVolunteers.")
    parser.add_argument('--scripted', action='store_true', help='Run in scripted mode.')
    args = parser.parse_args()

    if args.scripted:
        await run_scripted_actions()
    else:
        await run_interactive_mode()

if __name__ == "__main__":
    asyncio.run(main())