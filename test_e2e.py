# test_e2e.py
import pytest
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
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
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        
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

        # 3. Find and click the "Add to cart" button
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bg1"))
        )
        add_to_cart_button.click()
        
        # 4. CRITICAL: Wait for the header cart icon to update. This is a sign of
        #    a successful AJAX/session update. We look for the data-notify attribute to be "1".
        cart_icon = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-header-noti[data-notify='1']"))
        )
        # We can also explicitly assert this, though the wait itself is a strong test
        self.assertEqual(cart_icon.get_attribute('data-notify'), '1')

        # 5. Now that we've confirmed the item was added, navigate to the cart page
        #    We'll use the link from the header to be more realistic.
        cart_link = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/cart/"]')
        cart_link.click()

        # 6. On the cart page, wait for the specific product name to be visible within the table body.
        # This explicitly waits for the content to be loaded by JavaScript.
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "tbody"), "Unique Test Shirt")
        )
        # No explicit assert needed here, as the WebDriverWait itself will raise an exception if the text isn't found.
        # The test will pass if this line executes without error.


