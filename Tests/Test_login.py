from playwright.sync_api import sync_playwright
import pytest
import allure
import os
from Pages.Login import login


@allure.title("Login to IMS Application")
@allure.description("This test logs into the IMS application using valid credentials and verifies the dashboard.")
def test_login_to_ims():

   with sync_playwright() as p:

      # Use headless=True for CI/CD environments (Jenkins), headless=False for local
      headless_mode = os.getenv("HEADLESS", "false").lower() in ["true", "1", "yes"]
      browser = p.chromium.launch(headless=headless_mode)
      page = browser.new_page()

      login_page = login(page)

      login_page.perform_login("Saga", "Ims@1234")

      print("Login process completed.")

      page.locator("xpath=//input[@id='Date']").wait_for(
         state="visible",
         timeout=30000
      )

      print("Dashboard page loaded successfully!")

      assert page.locator("xpath=//input[@id='Date']"), "Date input not found"

      browser.close()