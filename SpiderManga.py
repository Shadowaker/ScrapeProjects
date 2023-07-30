"""
DISCLAIMER:

    this simple script was made to scrape the pdfs of the mangas inside this particular website (mangaworld.in)
    only for educational and exercise purposes.
    All the data obtained was delete instantly and not shared with others.
    This script worked until February 2023, the website may changed itself and the location of the target data.
"""


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random


TARGET = "https://www.mangaworld.in/"
DEBUG = True


def dprint(string):
    if DEBUG:
        print(string)


class Scraper:

    def __init__(self):
        self.options = Options()
        # self.options.headless = True
        self.driver = webdriver.Chrome("Drivers/chromedriver.exe", options=self.options)
        self.pool_1 = []
        self.VALS = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
        self.tmp_data = []
        self.read = 0

        # poor handmade way to elude anti-bot systems
        for x in range(10, 16):
            self.pool_1.append(x)
            for y in self.VALS:
                self.pool_1.append(x * y)
        self.pool_2 = []
        for x in range(1, 9):
            self.pool_2.append(x)
            for y in self.VALS:
                self.pool_2.append(x * y)

    def close(self):
        self.driver.close()

    def buildDataset(self):

        print("\nDataset Builder\n")

        self.driver.get(TARGET)

        self.driver.implicitly_wait(random.choice(self.pool_1))

        # accept their cookies and eat them with milk
        try:
            # usually they use all the same xpath, but sometimes you need to change it
            self.driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
            dprint("Cookies accepted.")
        except NoSuchElementException:
            # no cookies is strange, so take this implementation with a little salt
            pass

        self.driver.implicitly_wait(random.choice(self.pool_2))

        page = 1
        while True:
            try:
                self.scrapeArchivePage()
            except NoSuchElementException:
                if self.read == 0:
                    break
                self.read = 0
                page += 1
                self.driver.get(f"{TARGET}archive/?page={page}")
                self.driver.implicitly_wait(random.choice(self.pool_2))

    def scrapeArchivePage(self):
        x = 1
        while True:
            try:
                entry = self.driver.find_element(By.XPATH, f"/html/body/div[4]/div/div/div[2]/div[{x}]")

                thumb = entry.find_element(By.XPATH, f'/html/body/div[4]/div/div/div[2]/div[{x}]/a')
                url = thumb.get_attribute("href")
                img = thumb.find_element(By.XPATH, f'/html/body/div[4]/div/div/div[2]/div[{x}]/a/img').get_attribute(
                    "src")

                cont = entry.find_element(By.XPATH, f'/html/body/div[4]/div/div/div[2]/div[{x}]/div')
                name = cont.find_element(By.XPATH, f'/html/body/div[4]/div/div/div[2]/div[{x}]/div/p'
                                         ).find_element(By.XPATH,
                                                        f'/html/body/div[4]/div/div/div[2]/div[{x}]/div/p/a'
                                                        ).get_attribute("title")
                type_ = cont.find_element(By.XPATH, f'/html/body/div[4]/div/div/div[2]/div[{x}]/div/div[1]'
                                          ).find_element(By.XPATH,
                                                         f'/html/body/div[4]/div/div/div[2]/div[{x}]/div/div[1]/a'
                                                         ).text
                status = cont.find_element(By.XPATH, f'/html/body/div[4]/div/div/div[2]/div[{x}]/div/div[2]'
                                           ).find_element(By.XPATH,
                                                          f'/html/body/div[4]/div/div/div[2]/div[{x}]/div/div[2]/a'
                                                          ).text
                genres = self.scrapeGenres(cont, x)
                dprint("\n############################################################################\n")
                dprint(f"url: {url}\nimg: {img}\nname: {name}\ntype: {type_}\nstatus: {status}\ngenres: {genres}\n")
                self.tmp_data.append([len(self.tmp_data), url, img, name, type_, status, genres, "\n"])
                self.read += 1
            except NoSuchElementException:
                raise NoSuchElementException
            x += 1

    def getLatest(self):
        self.driver.get("https://www.mangaworld.in/")

        self.driver.implicitly_wait(random.choice(self.pool_1))

        # accept their cookies and eat them with milk
        try:
            self.driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
            dprint("Cookies accepted.")
        except NoSuchElementException:
            pass

    def getLatestInfo(self, x):
        self.driver.implicitly_wait(random.choice(self.pool_2))

        try:
            entry = self.driver.find_element(By.XPATH, f'/html/body/div[4]/div/div[1]/div[4]/div[{x}]')
        except Exception as e:
            raise e

        thumb = entry.find_element(By.XPATH, f'/html/body/div[4]/div/div[1]/div[4]/div[{x}]/a')
        url = thumb.get_attribute("href")
        img = thumb.find_element(By.XPATH, f'/html/body/div[4]/div/div[1]/div[4]/div[{x}]/a/img').get_attribute("src")

        cont = entry.find_element(By.XPATH, f'/html/body/div[4]/div/div[1]/div[4]/div[{x}]/div/p[1]')
        name = cont.find_element(By.XPATH, f'/html/body/div[4]/div/div[1]/div[4]/div[{x}]/div/p[1]'
                                 ).find_element(By.XPATH, f'/html/body/div[4]/div/div[1]/div[4]/div[{x}]/div/p[1]/a'
                                                ).get_attribute("title")
        genre = cont.find_element(By.XPATH, f'/html/body/div[4]/div/div[1]/div[4]/div[{x}]/div/div[1]'
                                  ).find_element(By.XPATH, f'/html/body/div[4]/div/div[1]/div[4]/div[{x}]/div/div[1]/a'
                                                 ).text
        status = cont.find_element(By.XPATH, f'/html/body/div[4]/div/div[1]/div[4]/div[{x}]/div/div[2]'
                                   ).find_element(By.XPATH, f'/html/body/div[4]/div/div[1]/div[4]/div[{x}]/div/div[2]/a'
                                                  ).text
        dprint("\n############################################################################\n")
        dprint(f"url: {url}\nimg: {img}\nname: {name}\ngenre: {genre}\nstatus: {status}")

    # STATIC UTILITY
    @staticmethod
    def scrapeGenres(cont, x):
        i = 1
        res = []
        base = cont.find_element(By.XPATH, f"/html/body/div[4]/div/div/div[2]/div[{x}]/div/div[5]")
        while True:
            try:
                gen = base.find_element(By.XPATH, f"/html/body/div[4]/div/div/div[2]/div[{x}]/div/div[5]/a[{i}]").text
                res.append(gen)
            except NoSuchElementException:
                break
            i += 1
        return res


def Main():
    start_time = time.time()

    print("Starting...  ")

    scrappy = Scraper()

    try:
        scrappy.getLatest()
        x = 1
        while x < 6:
            scrappy.getLatestInfo(x)
            x += 1
    except Exception as e:
        print("Error getting latest info.\n", str(e))
        return None

    try:
        scrappy.buildDataset()
    except Exception as e:
        print("Error building the dataset.\n", str(e))
        return None

    string = ""
    for x in scrappy.tmp_data:
        string += ", ".join(tuple(x))
    with open("tmp_data.csv", "w") as f:
        f.write(string)

    scrappy.close()
    print("--- %.2f seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    Main()
