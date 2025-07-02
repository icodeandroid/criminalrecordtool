from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


class Command(BaseCommand):
    help = 'Simple Chrome test'

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Launching browser...")

        try:
            options = Options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--headless')  # Uncomment if needed

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            driver.get("https://www.google.com")
            print("✅ Google loaded successfully")
            time.sleep(5)
            driver.quit()

        except Exception as e:
            print(f"❌ Error: {e}")
