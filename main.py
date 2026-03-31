import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from pages import UrbanRoutesPage
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_fare(self):

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.request_taxi()
        routes_page.select_comfort()

        comfort = self.driver.find_element(By.XPATH, "//div[text()='Comfort']")
        assert comfort.is_displayed()

    def test_fill_phone(self):

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_phone(data.phone_number)
        routes_page.confirm_phone_code()

        phone_button = self.driver.find_element(By.CLASS_NAME, "np-button")
        assert data.phone_number in phone_button.text

    def test_add_card(self):

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.open_payment_method()
        routes_page.add_card(data.card_number, data.card_code)
        routes_page.close_payment()

        payment_button = self.driver.find_element(By.CLASS_NAME, "pp-button")
        assert payment_button.is_displayed()

    def test_comment_for_driver(self):

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.write_message(data.message_for_driver)

        message = self.driver.find_element(By.ID, "comment")
        assert message.get_attribute("value") == data.message_for_driver

    def test_extra_requirements(self):

        routes_page = UrbanRoutesPage(self.driver)

        routes_page.add_blanket()
        routes_page.add_icecream()

        blanket_input = self.driver.find_element(
            By.XPATH,
            "//div[text()='Manta y pañuelos']/following::input[@type='checkbox'][1]"
        )

        assert blanket_input.is_selected()

        icecream_counter = self.driver.find_element(
            By.XPATH,
            "//div[text()='Helado']/..//div[@class='counter-value']"
        )

        assert icecream_counter.text == "2"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
