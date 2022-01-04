import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

GOOGLE_FORM = LINK TO YOUR GOOGLE FORM

#Example Zillow link to search for properties to rent in San Francisco, CA
ZILLOW_WEBSITE = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.66610182714844%2C%22east%22%3A-122.12639845800781%2C%22south%22%3A37.609407992296134%2C%22north%22%3A37.945135582461496%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

CHROME_DRIVER_PATH = PATH TO YOUR CHROME DRIVER

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,hu;q=0.7"
}

response = requests.get(ZILLOW_WEBSITE, headers=header)

zillow_page = response.text

soup = BeautifulSoup(zillow_page, "html.parser")

prices_div = soup.findAll(name="div", class_="list-card-price")
prices_list = [price.getText().split("/mo")[0] for price in prices_div]

addresses = soup.findAll(name="address", class_="list-card-addr")
address_list = [address.getText() for address in addresses]

links = soup.findAll(name="a", class_="list-card-img")
links_list = [link["href"] for link in links]

class FormFiller:
    def __init__(self, driver_path):
        self.serv = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.serv)

    def open_form(self, url):
        self.driver.get(url)
        sleep(1)

    def fill_up_form(self, address, price, link):
        sleep(1)
        address_input = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        address_input.send_keys(address)

        price_input = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price_input.send_keys(price)

        link_input = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link_input.send_keys(link)

        submit_button = self.driver.find_element(By.CLASS_NAME, 'appsMaterialWizButtonPaperbuttonContent.exportButtonContent')
        submit_button.click()

        submit_another = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        submit_another.click()


bot = FormFiller(CHROME_DRIVER_PATH)
bot.open_form(GOOGLE_FORM)


for n in range (len(address_list)):
    address_item = address_list[n]
    price_item = prices_list[n]
    link_item = links_list[n]
    bot.fill_up_form(address=address_item, price=price_item, link=link_item)
    print(address_item, price_item, link_item)

#
# header = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
#     "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,hu;q=0.7"
# }
#
# response = requests.get(
#     "https://www.zillow.com/homes/San-Francisco,-CA_rb/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.55177535009766%2C%22east%22%3A-122.31488264990234%2C%22south%22%3A37.69926912019228%2C%22north%22%3A37.851235694487485%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D",
#     headers=header)
#
# data = response.text
# soup = BeautifulSoup(data, "html.parser")
#
# all_link_elements = soup.select(".list-card-top a")
#
# all_links = []
# for link in all_link_elements:
#     href = link["href"]
#     print(href)
#     if "http" not in href:
#         all_links.append(f"https://www.zillow.com{href}")
#     else:
#         all_links.append(href)
#
# all_address_elements = soup.select(".list-card-info address")
# all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]
#
# all_price_elements = soup.select(".list-card-heading")
# all_prices = []
# for element in all_price_elements:
#     # Get the prices. Single and multiple listings have different tag & class structures
#     try:
#         # Price with only one listing
#         price = element.select(".list-card-price")[0].contents[0]
#     except IndexError:
#         print('Multiple listings for the card')
#         # Price with multiple listings
#         price = element.select(".list-card-details li")[0].contents[0]
#     finally:
#         all_prices.append(price)
#
#
# # Create Spreadsheet using Google Form
# # Substitute your own path here 👇
# driver_path = "C:\Development\chromedriver.exe"
# serv = Service(driver_path)
# driver = webdriver.Chrome(service=serv)
#
# for n in range(len(all_links)):
#     # Substitute your own Google Form URL here 👇
#     driver.get("https://docs.google.com/forms/d/e/1FAIpQLSddKZNklaXpG1359uRvCosMNltOZIv7Dk8qYpVdKBmob8Jweg/viewform?usp=sf_link")
#
#     time.sleep(2)
#     address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
#     price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
#     link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
#     submit_button = driver.driver.find_element(By.CLASS_NAME, 'appsMaterialWizButtonPaperbuttonContent.exportButtonContent')
#     address.send_keys(all_addresses[n])
#     price.send_keys(all_prices[n])
#     link.send_keys(all_links[n])
#     submit_button.click()

