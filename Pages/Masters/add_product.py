from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import time
import csv
import os


class Add_prod:
   def __init__(self, page: Page):
      self.page = page

      #self.item_code_input = page.get_by_role("textbox", name="Enter Item Code")

   def masters_click_test(self):
         self.page.get_by_title("Inventory Info").nth(1).click()
         self.page.get_by_role("link", name="Product Master").click()
         self.page.get_by_role("button", name="Add Product").click()
         self.page.locator("a").filter(has_text="Add Product").first.click()

   def add_prod_test(self,input_itemname: str,input_hscode: str,input_description: str,input_purchase_price: int,input_sales_price: int):

      item_group = self.page.get_by_role(
         "textbox",
         name="-- Press Enter For Item Group"
      )

      item_group.wait_for(state="visible", timeout=50000)
      item_group.press("Enter")

      # Wait for ng-select input
      ng_select_input = self.page.locator(".ng-input > input").first
      ng_select_input.wait_for(state="visible", timeout=50000)
      ng_select_input.click()
      print("ng-select box clicked")

      # Wait for option
      option = self.page.get_by_role("option", name="TESTTT")
      option.wait_for(state="visible", timeout=50000)
      option.click()
      print("option selected")

      ok_button = self.page.get_by_role("button", name="Ok")
      ok_button.wait_for(state="visible", timeout=50000)
      ok_button.click()
      print("OK button clicked")

      item_name = self.page.get_by_role(
         "textbox",
         name="Enter Item Name"
      )

      item_name.wait_for(state="visible", timeout=50000)
      item_name.fill(input_itemname)
      print("Item Name entered:", input_itemname)

      hs_code = self.page.get_by_role(
         "textbox",
         name="Enter HS Code"
      )

      hs_code.wait_for(state="visible", timeout=50000)
      hs_code.fill(input_hscode)
      print("HS Code entered:", input_hscode)

      unit_dropdown = self.page.locator("#unit")
      unit_dropdown.wait_for(state="visible", timeout=50000)
      unit_dropdown.select_option(label="Pkt.")

      print("Unit 'Pkt.' selected")

      description = self.page.get_by_role(
         "textbox",
         name="Enter Product Description"
      )

      description.wait_for(state="visible", timeout=50000)
      description.fill(input_description)
      print("Description entered:", input_description)

      short_name = self.page.get_by_role(
         "textbox",
         name="Enter Short Name"
      )

      short_name.wait_for(state="visible", timeout=50000)
      short_name.fill("TestProd")
      print("Short Name entered: TestProd")

      category_dropdown = self.page.locator("select[name=\"Category\"]")
      category_dropdown.wait_for(state="visible", timeout=50000)
      category_dropdown.select_option(label="ItemVariant")
      print("Category 'ItemVariant' selected")

      purchase_price = self.page.get_by_placeholder("Enter Purchase Price").nth(1)
      purchase_price.wait_for(state="visible", timeout=50000)
      purchase_price.fill(str(input_purchase_price))
      print("Purchase Price entered:", input_purchase_price)

      supplier_input = self.page.get_by_role("textbox",name="Press Enter to select").nth(0)
      supplier_input.wait_for(state="visible", timeout=30000)
      supplier_input.press("Enter")
      vendor = self.page.locator("//td[contains(normalize-space(),'11 QA Vendor')]")
      vendor.wait_for(state="visible", timeout=30000)
      vendor.dblclick()
      print("Supplier '11 QA Vendor' selected successfully!")

      sales_price = self.page.locator("input[type='number'][placeholder='0']").first
      sales_price.wait_for(state="visible", timeout=50000)
      sales_price.fill(str(input_sales_price))
      print("Sales Price entered successfully!")

   def save_button(self):
      self.page.locator("#save").click()

      try:
         dialog = self.page.wait_for_event("dialog", timeout=5000)
         dialog.accept()
      except:
         pass

      try:
         self.page.locator(
            "//button[normalize-space()='OK' or normalize-space()='Ok' or normalize-space()='Close']"
         ).click(timeout=10000)
      except:
         pass

      time.sleep(1)

   def save_product_to_csv(item_name,hs_code,description,purchase_price,sales_price,filename="product_details.csv"):
      file_exists = os.path.isfile(filename)
      with open(filename, mode="a", newline="", encoding="utf-8") as file:
         writer = csv.writer(file)
      if not file_exists:
         writer.writerow(["Item Name","HS Code","Description","Purchase Price","Sales Price"])
      writer.writerow([item_name,hs_code,description,purchase_price,sales_price])
      print(f"Product details saved to {filename}")
