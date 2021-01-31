import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class GoogleKeyworkScreenshoter:
    def __init__(self, keywords, max_page):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.keywords = keywords
        self.max_page = max_page

    def start(self):
        for keyword in self.keywords:
            self.driver.get("https://google.com")

            search_bar = self.driver.find_element_by_css_selector(".gLFyf")

            search_bar.send_keys(keyword)
            search_bar.send_keys(Keys.ENTER)

            self.screenshot(keyword)

    def screenshot(self, keyword):
        try:
            if not os.path.exists(f"./screenshots/google/{keyword}"):
                os.makedirs(f"./screenshots/google/{keyword}")

            element = WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, ".g-blk")
                )
            )

            self.driver.execute_script(
                """
            const [shitty] = arguments;
            shitty.parentElement.removeChild(shitty)
            """,
                element,
            )
        except Exception:
            pass

        search_results = self.driver.find_elements_by_css_selector("#rso .g")
        current_page = self.driver.find_element_by_css_selector(".YyVfkd")
        next_page = self.driver.find_element_by_css_selector("a#pnnext")

        for index, search_result in enumerate(search_results):
            title = search_result.find_element_by_css_selector("h3").text
            search_result.screenshot(f"screenshots/google/{keyword}/{title}.png")

        if int(current_page.text) < self.max_page and next_page:
            next_page.click()
            self.screenshot(keyword)

    def finish(self):
        self.driver.quit()


screenshoter = GoogleKeyworkScreenshoter(["buy domain", "python book"], 2)
screenshoter.start()
screenshoter.finish()
