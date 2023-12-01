import time 
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pandas as pd
from threading import Thread
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service

class YoutubeScraper:
    def __init__(self):
        f_service = Service("C:\geckodriver.exe")
        self.driver = webdriver.Firefox(service=f_service)
        self.links = []

    def login(self,bank):
        self.driver.get(f"https://www.youtube.com/{bank}/videos")
        self.driver.find_element_by_xpath("/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[2]/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[7]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[1]/div/ytd-rich-grid-media/div[1]/div[3]/div[1]/ytd-video-meta-block/div[1]/div[2]/span[2]")
        self.links.append()
    


if __name__ == "__main__":
    banks = ["SolusiBCA", "BankMegaID","BANK_BRI","OfficialBankMandiri","BankOCBCNISP","BNI1946"]
    scraper = YoutubeScraper()
    for bank in banks:
        scraper.login(bank)