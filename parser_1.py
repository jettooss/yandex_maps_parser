
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
from selenium.common.exceptions import NoSuchElementException
from typing import Union


class Parser:
    def __init__(self, driver):
        # Инициализация парсера с указанным драйвером

        self.driver = driver

    def scroll_to_bottom(self, elem, scr,key) -> None:
        # Метод выполняет прокрутку до конца страницы

        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            elem
        )  # скрипт прокрутки
        time.sleep(1)  # increased waiting time
        new_elem = self.driver.find_elements(By.CLASS_NAME, scr)[-1]
        if elem == new_elem:
            return
        self.scroll_to_bottom(new_elem, scr)


    def scroll_to_bottom1(self, elem) -> None:
        # Метод выполняет прокрутку до конца страницы

        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            elem
        )  # скрипт прокрутки

        new_elem = self.driver.find_elements(By.CLASS_NAME, "business-card-view__section")[-1]
        if elem == new_elem:
            return

    def get_data_reviews(self) :

        reviews_list = []
        elements = self.driver.find_elements(By.CLASS_NAME, "search-snippet-view")
        # scrolling goes to the end
        if elements:
            self.scroll_to_bottom(elements[-1], "search-snippet-view")

        elements = self.driver.find_elements(By.CLASS_NAME, "search-snippet-view")
        print(len(elements))
        for index in range(len(elements)):
            # Цикл для прохождения по всем элементам

            elem = elements[index]

            # Click on the element
            try:
                elem.find_element(By.XPATH, "div/div/div/div/div[2]/div[1]/span").click()
            except Exception:
                continue
            html = self.driver.page_source

            soup = BeautifulSoup(html, 'html.parser')
            opening_hours_list = [meta.get('content') for meta in soup.find_all('meta', itemprop="openingHours")]
            # print(opening_hours_list)

            daily_data = {}
            days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

            for i in range(1, 8):
                try:
                    button = self.driver.find_element(By.XPATH, f"/ html / body / div[1] / div[2] / div[8] / div / div[1] / div[1] / div / div[1] / div / div / div[3] / \
                                                   div[5] / div / div[3] / div / div / div[1] / div[9] / div / div[2] / div[2] / div[{i}]").click()

                    bars = soup.find_all('div', attrs={'class': 'business-attendance-view__bar'})
                    data = []

                    for bar in bars:
                        timee = bar['data-time']
                        height = int(bar['style'].split(':')[1].replace('%;', ''))
                        data.append((timee, height))

                    daily_data[days_of_week[i - 1]] = data

                except Exception:
                    daily_data = " "
            business_card = self.driver.find_elements(By.CLASS_NAME, 'business-card-view__section')
            if business_card:
                self.scroll_to_bottom1(business_card[-1])
            time.sleep(1.5)
            user_comments = {}
            try:
                button_comments = self.driver.find_element(By.XPATH,
                                                           "/html/body/div[1]/div[2]/div[8]/div/div[1]/div[1]/div/div[1]/div/div/div[3]/div[5]/div/div[3]/div/div/div[1]/div[11]/div/div/div[2]/div/div[2]/div[5]/div/div").click()

                business_reviews = self.driver.find_elements(By.CLASS_NAME, 'business-reviews-card-view__review')
                if business_card:
                    self.scroll_to_bottom(business_reviews[-1], 'business-reviews-card-view__review')
                time.sleep(2)
                business_reviews = self.driver.find_elements(By.CLASS_NAME, 'business-reviews-card-view__review')

                print(len(business_reviews))

                for i in business_reviews:
                    stars = i.find_elements(By.XPATH, ".//div[@class='business-rating-badge-view__stars']/span")
                    stars = self.get_count_star(stars)
                    try:
                        name = (i.find_element(By.XPATH, 'div / div /   div[1] / div[1] / a').text)
                    except NoSuchElementException:
                        name = ""
                    try:
                        text = (i.find_element(By.XPATH, 'div / div / div[3] / span[2] / div / span / span').text)
                    except NoSuchElementException:
                        text = ""
                    user_comments[name] = {
                        'stars': stars,
                        'text': text
                    }
            except Exception:
                continue

            elements = self.driver.find_elements(By.CLASS_NAME, "search-snippet-view")
            elem = elements[index]
            try:
                categories = elem.find_element(By.CLASS_NAME, "search-business-snippet-view__categories").text
            except Exception:
                categories = ""
            try:
                address = elem.find_element(By.CLASS_NAME, "search-business-snippet-view__address").text
            except Exception:
                address = ""
            try:
                estimation = elem.find_element(By.XPATH,
                                               "div / div / div / div / div[4] / a / div / div[1] / div[2] / span[2]").text
            except Exception:
                estimation = ""
            try:
                review_count = elem.find_element(By.XPATH, "div / div / div / div / div[4] / a / div / span[1]").text
            except Exception:
                review_count = ""
            try:
                geo = elem.find_element(By.XPATH, "div ")
                coordinates = geo.get_attribute('data-coordinates')
            except Exception:
                coordinates = ""

            try:
                fiz = elem.find_element(By.XPATH,
                                        "/html/body/div[1]/div[2]/div[8]/div[1]/div[1]/div[1]/div/div[1]/div/div/div[3]/div[5]/div/div[3]/div/div/div[1]/div[7]/div/div[2]/div[1]/div[2]/div/div[2]").text
                is_physical_entity = True
            except NoSuchElementException:
                is_physical_entity = False
            try:
                ur = elem.find_element(By.XPATH,
                                       " / html / body / div[1] / div[2] / div[8] / div / div[1] / div[1] / div / div[1] / div / div / div[ 3] / div[5] / div / div[3] / div / div / div[1] / div[7] / div / div[2] / div[2] / div / div / div[2]").text
                is_corporate_entity = True

            except NoSuchElementException:
                is_corporate_entity = False
            review = {
                "coordinates": coordinates,
                "estimation": estimation,
                "categories": categories,
                "review_count": review_count,
                "address": address,
                "time": daily_data,
                "physical": is_physical_entity,
                "entity": is_corporate_entity,
                "opening_hours_list": opening_hours_list,
                "user_comments": user_comments

            }
            reviews_list.append(review)
            print(review)


        self.save_to_file(reviews_list, 'Furious11.json')

    @staticmethod
    def save_to_file(data, filename):

        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    @staticmethod
    def get_count_star(review_stars: list) -> Union[float, int]:

        star_count: float = 0
        for review_star in review_stars:
            if '_empty' in review_star.get_attribute('class'):
                continue
            if '_half' in review_star.get_attribute('class'):
                star_count = star_count + 0.5
                continue
            star_count = star_count + 1
        return star_count


vtb_bank_url: str = 'https://yandex.ru/maps/213/moscow/chain/bank_vtb_otdelenya/6002211/filter/chain_id/6002211/?ll=37.618171%2C55.845814&sctx=ZAAAAAgBEAAaKAoSCZ5eKcsQz0JAEdOgaB7A4EtAEhIJA137Anqh8j8RmPxP%2Fu4d7D8iBgABAgMEBSgAOABAAUgBYipjb2xsZWN0aW9uc19yYW5raW5nX21vZGVsPWNvbGxlY3Rpb25zX2Rzc21qAnJ1ggEQY2hhaW5faWQ6NjAwMjIxMZ0BzcxMPaABAKgBAL0BK7Ps5MIBhwGx09%2FQBNX28ocEhZbrqgX967C0Be6v07WPBd6d9KR4wojU9sAEqKWKxQTZucPcBYT%2F4uG7A4238IKwA9qH6OUDyKHiowWJp7uOuQO1%2Fqn68gG2yrCMBauq6NGCBtD29Plu8NnBpr4E1PGUvJUD7PvmpwT4neWGBuiehvgDtPTc3akDuZKvzQTqAQDyAQD4AQCCAhBjaGFpbl9pZDo2MDAyMjExigIAkgIAmgIMZGVza3RvcC1tYXBzqgKXATYwMDIyMTEsNjE5NDI3MjYxLDYwMDE5NDcsNjAwMjQwNSw2MDAzNTI5LDc3MTE1ODA1MSw2MDAyMTU3LDgwNTU1MDk1Myw2MDAyMjU0LDgzMDg5MTkxMiwzMTg0MjYyNDQsMTkzNjEwODczMjUsMTg4NjEyMTg2LDYwMDE5OTMsNjAwMjM1Miw2MDAzMzk5LDYwMDIxMjSwAgE%3D&sll=37.618171%2C55.845814&sspn=0.604997%2C0.550648&z=10.57'

opts = webdriver.ChromeOptions()
opts.add_argument('headless')
opts.add_argument('--disable-gpu')
opts.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36')
driver = webdriver.Chrome(options=opts)
driver.get(vtb_bank_url)

# Открывает веб-страницу в полноэкранном режиме
driver.maximize_window()

parser = Parser(driver)
parser.get_data_reviews()
