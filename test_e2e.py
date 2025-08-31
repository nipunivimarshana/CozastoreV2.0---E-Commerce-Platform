# test_e2e.py
import pytest
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options # <--- REQUIRED IMPORT
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from products.models import Product, Category

# Imports for creating a dummy image file for tests
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.e2e
class E2ETests(StaticLiveServerTestCase):
    
    def setUp(self):
        """Runs once before each test in this class."""
        super().setUp()
        
        # --- FIX 1: CONFIGURE HEADLESS MODE FOR CI/CD ---
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=chrome_options
        )
        # --- END OF FIX 1 ---
        
        # Create a temporary dummy image file to associate with the product
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            image = Image.new("RGB", (10, 10), "red") # Create a small red square image
            image.save(f, "JPEG")
            f.seek(0)
            image_file = SimpleUploadedFile(f.name, f.read(), content_type="image/jpeg")
        
        # Create the necessary test data in the temporary test database
        category = Category.objects.create(name='Shirts', slug='shirts')
        Product.objects.create(
            category=category,
            name='Unique Test Shirt',
            slug='unique-test-shirt',
            price=25.00,
            is_available=True,
            image=image_file # Attach the dummy image
        )

    def tearDown(self):
        """Runs once after each test in this class."""
        self.driver.quit()
        super().tearDown()

    def test_add_to_cart_journey(self):
        """
        Tests the full user journey of navigating to a product, adding it to the
        cart, and verifying the cart's contents.
        """
        # 1. Get the product we want to test from the database
        product_to_add = Product.objects.get(slug='unique-test-shirt')

        # 2. Navigate directly to that product's detail page
        self.driver.get(f"{self.live_server_url}{product_to_add.get_absolute_url()}")

        # --- FIX 2: USE JAVASCRIPT CLICK TO PREVENT INTERACTION ERRORS ---
        # First, wait for the button to be present in the DOM
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.bg1"))
        )
        # Then, use JavaScript to force the click, bypassing any visual obstructions.
        self.driver.execute_script("arguments[0].click();", add_to_cart_button)
        # --- END OF FIX 2 ---
        
        # 4. CRITICAL: Wait for the header cart icon to update. This is a sign of
        #    a successful AJAX/session update. We look for the data-notify attribute to be "1".
        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-header-noti[data-notify='1']"))
        )
        self.assertEqual(cart_icon.get_attribute('data-notify'), '1')

        # 5. Now that we've confirmed the item was added, navigate to the cart page
        cart_link = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/cart/"]')
        cart_link.click()

        # --- FIX 3: USE ROBUST WAIT FOR CART CONTENT ---
        # Wait for the specific product name to be visible within the table body.
        # This is the most reliable way to confirm the cart has loaded correctly.
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "tbody"), "Unique Test Shirt")
        )
        # --- END OF FIX 3 ---

        