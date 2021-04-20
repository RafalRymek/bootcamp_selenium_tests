import pytest
import time
from hamcrest import assert_that, is_, is_not, none, not_none, equal_to, starts_with, equal_to_ignoring_case, has_string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


class TestSelenium:
    BASE_URL = "http://automationpractice.com/index.php"
    SEARCH_INPUT = "Printed dress"
    DRESS_INPUT = "Dress"
    USER_EMAIL = "test" + str(time.time() * 1000) + "@test.com"

    # search_selectors
    search_field = (By.XPATH, "//input[@class='search_query form-control ac_input']")
    submit_button = (By.XPATH, "//button[@type='submit']")
    product_container = (By.XPATH, "//div[@class='product-container']")

    # register_selectors
    sign_in_button = (By.XPATH, "//a[@class='login']")
    email_field = (By.XPATH, "//input[@class='is_required validate account_input form-control']")
    create_submit_button = (By.XPATH, "//button[@class='btn btn-default button button-medium exclusive']")
    create_account_page = (By.XPATH, "//h1[contains(text(),'Create an account')]")
    first_name = (By.XPATH, "//input[@id='customer_firstname']")
    last_name = (By.XPATH, "//input[@id='customer_lastname']")
    password = (By.XPATH, "//input[@type='password']")
    address_first_name = (By.XPATH, "//input[@id='firstname']")
    address_last_name = (By.XPATH, "//input[@id='lastname']")
    address_input = (By.XPATH, "//input[@id='address1']")
    city_input = (By.XPATH, "//input[@id='city']")
    state_picker = (By.XPATH, "//select[@id='id_state']/option[text()='Alaska']")
    zip_code = (By.XPATH, "//input[@id='postcode']")
    country_picker = (By.XPATH, "//select[@id='id_country']/option[text()='United States']")
    phone_number = (By.XPATH, "//input[@id='phone_mobile']")
    alias_input = (By.XPATH, "//input[@id='alias']")
    register_button = (By.XPATH, "//button[@id='submitAccount']")
    account_information = (By.XPATH, "//p[@class='info-account']")

    # add_to_cart_selectors
    add_to_cart = (By.XPATH, "//a[@class='button ajax_add_to_cart_button btn btn-default']")
    success_added_icon = (By.XPATH, "//i[@class='icon-ok']")
    success_header = (By.XPATH, "//h2")
    close_pop_up = (By.XPATH, "//span[@title='Close window']")
    shopping_cart = (By.XPATH, "//a[@title='View my shopping cart']")
    button_order_cart = (By.XPATH, "//a[@id='button_order_cart']")
    quantity = (By.XPATH, "//span[@class='quantity-formated']")
    order_summary_quantity = (By.XPATH, "//input[@name='quantity_5_19_0_0_hidden']")

    def setup(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
        self.driver.implicitly_wait(2)
        self.driver.set_window_size(1440, 900)
        self.driver.get(self.BASE_URL)

    def test_search(self):
        self.driver.find_element(*self.search_field).send_keys(self.SEARCH_INPUT)
        self.driver.find_element(*self.submit_button).click()
        self.driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
        search_result = self.driver.find_elements(*self.product_container)
        assert_that(search_result, is_(not_none()), reason="Result is empty")
        assert_that(len(search_result), is_(equal_to(0)), reason="Wrong amount of products")

    def test_registration(self):
        self.driver.find_element(*self.sign_in_button).click()
        self.driver.find_element(*self.email_field).send_keys(self.USER_EMAIL)
        self.driver.find_element(*self.create_submit_button).click()
        self.driver.find_element(*self.create_account_page)
        self.driver.implicitly_wait(2)
        assert_that(*self.create_account_page, starts_with("Create"))
        self.driver.find_element(*self.first_name).send_keys("Tester")
        self.driver.find_element(*self.last_name).send_keys("Testers")
        assert_that(*self.address_first_name, is_not(none()))
        assert_that(*self.address_last_name, is_not(none()))
        self.driver.find_element(*self.password).send_keys("123456")
        self.driver.find_element(*self.address_input).send_keys("Brain street")
        self.driver.find_element(*self.city_input).send_keys("Cracow")
        self.driver.find_element(*self.state_picker).click()
        self.driver.find_element(*self.zip_code).send_keys("00000")
        assert_that(*self.zip_code, has_string("00000"))
        self.driver.find_element(*self.country_picker)
        assert_that(*self.country_picker, is_not(none()))
        self.driver.find_element(*self.phone_number).send_keys("111222333")
        self.driver.find_element(*self.alias_input).clear()
        self.driver.find_element(*self.alias_input).send_keys("test@test.com")
        self.driver.find_element(*self.register_button).click()
        self.driver.find_element(*self.account_information)
        assert_that(*self.account_information, starts_with("Welcome"))

    def test_add_to_cart(self):
        self.driver.find_element(*self.search_field).send_keys(self.DRESS_INPUT)
        self.driver.find_element(*self.submit_button).click()
        search_result = self.driver.find_elements(*self.product_container)
        assert_that(search_result, is_(not_none()))
        first_dress = self.driver.find_elements(*self.product_container)[0]
        self.driver.execute_script("window.scrollTo(10, document.body.scrollHeight);")
        ActionChains(self.driver).move_to_element(first_dress).perform()
        assert_that(*self.add_to_cart, equal_to_ignoring_case("Add to cart"))
        self.driver.find_element(*self.add_to_cart).click()
        self.driver.implicitly_wait(2)
        self.driver.find_element(*self.close_pop_up).click()
        cart_icon = self.driver.find_element(*self.shopping_cart)
        ActionChains(self.driver).move_to_element(cart_icon).perform()
        self.driver.find_element(*self.quantity)
        assert_that(*self.quantity, has_string("1"))
        self.driver.find_element(*self.button_order_cart).click()
        self.driver.find_element(*self.order_summary_quantity)
        assert_that(*self.order_summary_quantity, has_string("1"))

    def teardown(self):
        self.driver.quit()
