from playwright.sync_api import Page, expect

class login:
   def __init__(self, page: Page):
      self.page = page

      # locators (same XPath strategy as Selenium)
      self.username = "//input[@placeholder='Username']"
      self.password = "//input[@placeholder='Password']"
      self.login_button = "//button[contains(text(), 'Login')]"
      self.logout_button = "//button[contains(@class,'mat-flat-button') and .//span[normalize-space()='Sign out']]"

   def perform_login(self, username: str, password: str):

      # Open login page (same as Selenium)
      self.page.goto("http://stc21.webredirect.himshang.com.np")

      # Username
      username_box = self.page.locator(self.username)
      username_box.wait_for(state="visible", timeout=35000)
      username_box.fill(username)

      # Password
      password_box = self.page.locator(self.password)
      password_box.wait_for(state="visible", timeout=35000)
      password_box.fill(password)

      # Click login
      login_btn = self.page.locator(self.login_button)
      login_btn.wait_for(state="visible", timeout=35000)
      login_btn.click()

      print("Login button clicked!")

      # Handle "already logged in" popup
      try:
         popup_logout_btn = self.page.locator(self.logout_button)
         popup_logout_btn.wait_for(state="visible", timeout=20000)
         popup_logout_btn.click()

         print("Detected previous session popup and clicked Logout.")

         # retry login
         login_btn = self.page.locator(self.login_button)
         login_btn.wait_for(state="visible", timeout=20000)
         login_btn.click()

         print("Login button re clicked!")

      except:
         print("No previous session popup detected.")

   def verify_login(self):
      current_url = self.page.url

      if current_url == "https://stc21.webredirect.himshang.com.np/#/pages/dashboard":
         print(f"Test Successful, tested on {current_url}")

      elif current_url == "https://stc21.variantqa.himshang.com.np/#/pages/dashboard":
         print(f"Test Successful, tested on {current_url}")

      else:
         print(f"Login failed or unexpected URL: {current_url}")