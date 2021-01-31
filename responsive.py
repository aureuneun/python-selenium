import time
import os
from math import ceil
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class ResposiveScreenshoter:
    def __init__(self, urls):
        self.urls = urls

    def start(self):
        for url in self.urls:
            self.screenshot(url)

    def screenshot(self, url):
        https, folder = url.split("//")
        if not os.path.exists(f"./screenshots/responsive/{folder}"):
            os.makedirs(f"./screenshots/responsive/{folder}")

        with webdriver.Chrome(ChromeDriverManager().install()) as driver:
            driver.get(url)
            driver.maximize_window()

            window_size = driver.get_window_size()
            window_max_width = window_size["width"]
            window_max_height = window_size["height"]

            sizes = [480, 768, 1024, window_max_width]

            for size in sizes:
                driver.set_window_size(size, window_max_height)
                driver.execute_script("window.scrollTo(0, 0)")
                time.sleep(1)
                scroll_height = driver.execute_script(
                    "return document.body.scrollHeight"
                )
                inner_height = driver.execute_script("return window.innerHeight")
                total_sections = ceil(scroll_height / inner_height)
                for section in range(total_sections):
                    driver.execute_script(
                        f"window.scrollTo(0, {section * inner_height})"
                    )
                    time.sleep(1)
                    driver.save_screenshot(
                        f"./screenshots/responsive/{folder}/{size}-{section}.png"
                    )


screenshoter = ResposiveScreenshoter(
    ["https://nomadcoders.co", "https://www.apple.com"]
)
screenshoter.start()
