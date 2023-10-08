
from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def open_page():
    url: str = 'https://yandex.ru/maps/213/moscow/chain/bank_vtb_otdelenya/6002211/filter/chain_id/6002211/?ll=37.821379%2C55.762458&sctx=ZAAAAAgBEAAaKAoSCZ5eKcsQz0JAEdOgaB7A4EtAEhIJA137Anqh8j8RmPxP%2Fu4d7D8iBgABAgMEBSgAOABAAUgBYipjb2xsZWN0aW9uc19yYW5raW5nX21vZGVsPWNvbGxlY3Rpb25zX2Rzc21qAnJ1ggEQY2hhaW5faWQ6NjAwMjIxMZ0BzcxMPaABAKgBAL0BK7Ps5MIBiAHu04vKBIfVgNfSBP7dyo4EreGfmgXE%2FLSegQL85ZvrlgWUkM%2BCBKvN8PUE6sWv74ACqo%2F%2B5QPtuNzuBLj3v44Fs%2FHr%2BQPM0Z3%2BA8j6m4m2Bqmbjv6bBIqlx4lR1PGUvJUDjbfwgrADzNjkgqkFhOvI8%2FoE2PXcxNgB%2FPjcyAXah%2BjlA9%2FD%2BfgE6gEA8gEA%2BAEAggIQY2hhaW5faWQ6NjAwMjIxMYoCAJICAJoCDGRlc2t0b3AtbWFwc6oCnAE2MDAyMjExLDYwMDM2MTIsNjAwMzM5OSw2MDAyMTU3LDYwMDM1MjksNzcxMTU4MDUxLDYxOTQyNzI2MSw2MDAxOTQ3LDE5MjQxMzgwOTU1NCw2MDAyNDA1LDMxODQyNjI0NCw2MDAyMjA2LDE5MzYxMDg3MzI1LDgwNTU1MDk1Myw2MDAyMTI0LDgzMDg5MTkxMiwxODg2MTIxODawAgE%3D&sll=37.821379%2C55.762458&sspn=0.953064%2C0.326754&z=11 '
    opts = webdriver.ChromeOptions()
    # opts.add_argument('headless')
    # opts.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=opts)
    parser = Parser(driver)
    driver.get(url)
    time.sleep(5)

    return parser

class Parser:
    def __init__(self, driver):
        self.driver = driver

    def scroll_to_bottom(self, elem, driver) -> None:
        """
        Скроллим список до последнего отзыва
        :param elem: Последний отзыв в списке
        :param driver: Драйвер undetected_chromedriver
        :return: None
        """
        driver.execute_script(
            "arguments[0].scrollIntoView();",
            elem
        )
        time.sleep(3)  # увеличено время ожидания
        new_elem = driver.find_elements(By.CLASS_NAME, "search-snippet-view")[-1]
        if elem == new_elem:
            return
        self.scroll_to_bottom(new_elem, driver)
    def get_data_reviews(self) -> list:
        reviews = []
        elements = self.driver.find_elements(By.CLASS_NAME, "search-snippet-view")
        print(len(elements))
        if len(elements) > 1:
            self.scroll_to_bottom(elements[-1], self.driver)
            elements = self.driver.find_elements(By.CLASS_NAME, "search-snippet-view")
            # print(streat)
            for elem in elements:
                locations  = elem.find_element(By.CLASS_NAME, "_type_business")

                categories = elem.find_element(By.CLASS_NAME, "search-business-snippet-view__categories").text
                addres = elem.find_element(By.CLASS_NAME, "search-business-snippet-view__address").text
                rating = elem.find_element(By.CLASS_NAME, "business-rating-badge-view__rating-text _size_m").text


                # Выводим координаты и размер в консоль
                print('Location: ', location)
                print('Size: ', size)
                print(categories,addres,rating)

                # print(elem)
                # reviews.append(self.get_data_item(elem))
        return reviews

parser = open_page()
parser.get_data_reviews()