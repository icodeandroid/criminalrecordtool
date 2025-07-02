from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
from django.core.management.base import BaseCommand, CommandError
from scraper.models import CriminalRecord
from datetime import datetime

class Command(BaseCommand):
    help = 'Scrape and login to eClerks LA website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            required=True,
            help='Email address for login'
        )
        parser.add_argument(
            '--password',
            required=True,
            help='Password for login'
        )

    def handle(self, *args, **options):
        EMAIL = options['email']
        PASSWORD = options['password']

        options_chrome = Options()
        options_chrome.add_argument("--start-maximized")
        # options_chrome.add_argument("--headless")  # Uncomment for headless mode

        service = Service()  # Make sure chromedriver is in PATH or provide path here
        driver = webdriver.Chrome(service=service, options=options_chrome)

        try:
            self.stdout.write("🚀 Opening eClerks LA homepage...")
            driver.get("https://www.eclerksla.com")

            self.stdout.write("⏳ Waiting for login modal to appear...")
            WebDriverWait(driver, 9999999).until(
                EC.presence_of_element_located((By.ID, "statewidePortalDecisionTree"))
            )

            self.stdout.write("⌨️ Waiting for email input field...")
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "UserEmail"))
            )

            self.stdout.write("✍️ Entering credentials...")
            email_input.send_keys(EMAIL)
            password_input = driver.find_element(By.ID, "UserPassword")
            password_input.send_keys(PASSWORD)

            try:
                token = driver.find_element(By.NAME, "__RequestVerificationToken").get_attribute("value")
                self.stdout.write(f"🔑 Token grabbed: {token}")
            except NoSuchElementException:
                self.stdout.write("⚠️ Token not found — proceeding without it.")

            self.stdout.write("🔘 Clicking login button...")
            login_btn = driver.find_element(By.ID, "login")
            login_btn.click()

            self.stdout.write("⏳ Waiting for records page to load...")
            time.sleep(5)  # Replace with explicit wait if possible

            # === Begin scraping records from the page ===
            self.stdout.write("📋 Scraping records from the page...")

            # TODO: Replace this XPath with the actual XPath for the rows on the target page
            rows = driver.find_elements(By.XPATH, '//*[@id="gridcolumn-1013-textInnerEl"]')

            if not rows:
                self.stdout.write("⚠️ No records found with the given XPath selector.")
                return

            for row in rows[:20]:  # Limit to first 20 rows
                try:
                    name = row.find_element(By.XPATH, './/td[1]').text
                    case_number = row.find_element(By.XPATH, './/td[2]').text
                    date_str = row.find_element(By.XPATH, './/td[3]').text
                    status = row.find_element(By.XPATH, './/td[4]').text

                    # Adjust the date format if necessary
                    date = datetime.strptime(date_str, "%m/%d/%Y").date()

                    CriminalRecord.objects.create(
                        name=name,
                        case_number=case_number,
                        date=date,
                        status=status
                    )
                    self.stdout.write(f"✅ Saved record: {name} - {case_number}")

                except Exception as e:
                    self.stderr.write(f"❌ Failed to scrape/save one record: {str(e)}")

            self.stdout.write("✅ Scraping and saving complete.")

            # Optionally save current page source for debugging
            with open("last_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

        except (TimeoutException, WebDriverException) as e:
            self.stderr.write(f"❌ Error during automation:\n{str(e)}")

        finally:
            driver.quit()
