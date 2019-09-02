from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class Webscraper():
    def __init__(self,item):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("user-data-dir={1}")
        self.driver = webdriver.Chrome(options = self.chrome_options)
        self.price_list = {}
        self.item = item

    def open_site(self, site):
        self.driver.get(site)

    def check_loaded(self, id):
        try:
            myElem = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, id)))
            print ("Page is ready!")
        except TimeoutException:
            print ("Loading took too much time!")

    def search(self, xpath):
        search_bar = self.driver.find_element_by_xpath(xpath)
        search_bar.clear()
        search_bar.send_keys(self.item)
        search_bar.send_keys(Keys.ENTER)

class Amazon(Webscraper):
    def __init__(self,item):
        super().__init__(item)

    def get_price(self):
        for i in range (0,5): #mehr ergebnisse, dafür übersichtlicher gestalten mit flask oder qt oder pygame
            try:
                item = self.driver.find_element_by_xpath("//div[@data-index='"+ str(i) +"']")
                product = item.find_element_by_xpath(".//span[@class='a-size-medium a-color-base a-text-normal']").text
                if self.item.lower() in product.lower(): #am besten self.item auseinander brechen und für jedes wort einzeln checken und nicht alles zusammen
                    price = item.find_element_by_xpath(".//span[@class='a-price-whole']")
                    new_price = price.text.replace(',','.')
                    link = item.find_element_by_xpath(".//a[@class = 'a-link-normal a-text-normal']").get_attribute('href')
                    self.price_list[link] = float(new_price)
            except NoSuchElementException:
                continue
        print(self.price_list)

    def run_Amazon(self):
        self.open_site('https://www.amazon.de')
        self.check_loaded('twotabsearchtextbox')
        self.search("//input[@id = 'twotabsearchtextbox']")
        self.check_loaded('twotabsearchtextbox')
        self.get_price()
        self.driver.quit()


if __name__ == '__main__':
    Amazon_Echo = Amazon('Echo Dot')
    Amazon_Echo.run_Amazon()
    iPhone_X_64GB_SpaceGrau = Amazon('iPhone X 64GB space grau') #kein Ergebniss, weil Suche nicht 100% übereinstimmt
    iPhone_X_64GB_SpaceGrau.run_Amazon()
