from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import time
import dateparser
import datetime
import pandas as pd
import numpy as np


class FBScraper:
    def __init__(self, driver):
        self.driver = driver
        self.df_url = []
        self.url = []
        
        self.user_names=[]
        self.user_comments=[]
        self.comments_date=[]
        self.url_list = []
        self.bank_list = []
        self.platform = []

    def login(self,link,email,password):
        self.driver.get(link) # Runing the url with the driver
        # self.driver.maximize_window()

        driver.find_element(By.NAME,'email').send_keys(email)
        time.sleep(5)
        driver.find_element(By.NAME,"pass").send_keys(password)
        time.sleep(5)
        driver.find_element(By.NAME,'login').click()
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR,'input.bp').click()

    def get_fb_url(self,Facebook_account: str, cutoff_awal: datetime.date,cutoff_akhir: datetime.date, max_post: int=100):
    
    
        posts_url = []
        post_dates_list = []


        self.driver.get(f"https://mbasic.facebook.com/{Facebook_account}")
        time.sleep(2)
        try:
            try:
                Foto = self.driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[4]/div/a')
                Foto.click()
            except:
                Foto = self.driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div[1]/div[1]/div[4]/a[2]')
                Foto.click()
        except:
            try:
                Foto = self.driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[5]/div/a/table/tbody/tr/td[1]')
                Foto.click()
            except:
                Foto = self.driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[6]/div/a/table/tbody/tr/td[1]')
                Foto.click()
        time.sleep(3)
        # Click See all
        try:
            self.driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/table/tbody/tr/td/div[1]/div/div[1]/section/a').click()
        except:
            self.driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div[2]/div[1]/section/a').click()
        Page = 0
        for i in range(50):
            time.sleep(3)
            for x in range(1,13):
                time.sleep(3)
                print(f'post number {x}')

                click = self.driver.find_element(By.XPATH,f'/html/body/div/div/div/div/table/tbody/tr/td/div/a[{x}]')
                time.sleep(3)
                click.click()

                post_time = self.driver.find_element(By.TAG_NAME,'abbr').text
                # if '2022' in post_time:
                #     post_time = driver.find_element(By.TAG_NAME,'abbr').text
                post_date = dateparser.parse(post_time)

                Link = self.driver.find_element(By.XPATH,'/html/head/link[1]').get_attribute('href')

                if post_date == None :
                    print(post_time,';',Link)  
                    post_time = 'Kemarin lusa pukul 07.00'
                    post_date = dateparser.parse(post_time)
                                    
                if post_date.date() > cutoff_akhir:
                    print('post date more than cutoff akhir')
                    time.sleep(3)
                    self.driver.back()
                    # for i in range(3):
                    #     time.sleep(3)
                    #     driver.back()

                if post_date.date() < cutoff_awal:
                    print('post date less than cutoff awal')
                    break
                
                try:
                    if post_date.date() <= cutoff_akhir:
                        print(1)
                        time.sleep(1)
                        posts_url.append(Link)
                        post_dates_list.append(post_date.date())
                        time.sleep(1)
                        print(Link)
                        print(post_date.date())
                        time.sleep(3)
                        print(2)
                        self.driver.back()
                except:
                    print('date > cutoff akhir')
                    pass


                    
                if len(posts_url) > max_post:
                    print('len of post url more than max post')
                    break 
                


            Page += 1
            print(Page)
            if post_date.date() < cutoff_awal:
                    print('post date less than cutoff awal (II)')
                    break
            time.sleep(3)
            self.driver.find_element(By.XPATH,'/html/body/div/div/div/div/table/tbody/tr/td/div/span/div/a').click()

        return posts_url, post_dates_list
    

    def get_urls(self, banks):
        banks_url = []
        url_date = []
        bank_name = []
        for b in banks:
            fb_post_url = scraper.get_fb_url(Facebook_account= b, cutoff_awal= tanggal_awal ,cutoff_akhir = tanggal_akhir, max_post=100)
            link_list = []
            date_link_list = []
            link_list.append(fb_post_url[0])
            date_link_list.append(fb_post_url[1])
            for x in link_list:
                banks_url.append(x)
            for i in date_link_list:
                url_date.append(i)

        Links = []
        date_url = []
        for i in banks_url:
            for x in i:
                Links.append(x)
                bank_name.append(b)

        for j in url_date:
            for z in j:
                date_url.append(z)


        # self.df_url = pd.DataFrame(list(zip(Links,date_url,bank_name)), columns=['URL','Post_Date','Bank_Name'])
        # self.url = self.df_url.iloc[:,0]
        # print(self.url,"URL URL123")
        # print(self.df_url)
        self.get_comments(Links,date_url,bank_name)

    def get_comments(self,Links,date_url,bank_name):
        # loop = (Links,date_url,bank_name)
        for i in range(len(Links)):
            # print(n,'MASUKKKKKKKKKKKKKKKKKKKKKKK')
            time.sleep(2)
            print(Links[i])
            try:
                driver.get(Links[i])
                time.sleep(4)
                print('hore 1')
                segments = self.driver.find_element(By.XPATH('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/div'))
                # /html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/div[2]
                # /html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/div[4]
                # /html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/div[3]
                # /html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/div[4]
                /html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/div[3]
                /html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/div[5]
                # div.x1pi30zi:nth-child(4) > div:nth-child(3)
                # div.x1pi30zi:nth-child(4) > div:nth-child(4)
                # div.x1pi30zi:nth-child(4) > div:nth-child(5)
                # 'div.x1pi30zi:nth-child(4) > div:nth-child'
                time.sleep(4)
                print('hore hore',segments)
                # for segment in segments:
                try:
                    print('hore 2')
                    name = segments.find_element(By.XPATH,'/div/h3/a').text
                    content = segments.find_element(By.XPATH,'/div/div[1]').text
                    try:
                        emot = segments.find_element(By.XPATH,f'/span')
                        for emo in emot:
                            content+=emo.find_element(By.XPATH,'/span').text
                    except:
                        print("No more emot")
                        break
                    print(name, content, "   YAY")
                    self.url_list.append(driver.current_url)
                    self.user_names.append(name)
                    self.user_comments.append(content)
                    # self.comments_date.append(com_date)
                    # /html/body/div/div/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div/div[4]/div[1]/div/div[3]/abbr
                    self.bank_list.append(bank_name[i])
                    self.platform.append('Facebook')
                    # print(driver.current_url,';',name,';',content,';',com_date,';',account_name)
                    self.driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div/div[4]/div[11]/a').click()
                except:
                    print("No More Comments")
            #     while True:

            #         try:
            #             self.driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div[12]/a').click()
            #         except:
            #             print("No More Comments")
            #             break                        
                
            #     /html/body/div/div/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div/div[4]/div[3]/div/h3/a
            #     /html/body/div/div/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div/div[4]/div[1]/div/h3/a
            #     /html/body/div/div/div[2]/div/div[1]/div/div/div[3]/div[2]/div/div/div[4]/div[2]/div/h3/a
            #     /html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div[6]/div/h3/a
            #     /html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div[9]/div/h3/a
            #     /html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div[5]/div/h3/a
            #     /html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div[11]/div/h3/a
            #     /html/body/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div[11]/div/h3/a
            #     self.url_list.append(driver.current_url)
            #     self.user_names.append(name)
            #     self.user_comments.append(content)
            #     self.comments_date.append(com_date)
            #     self.bank_list.append(bank_name[i])
            #     self.platform.append('Facebook')
            #     print(driver.current_url,';',name,';',content,';',com_date,';',account_name)
            except:
                print('pass',';',driver.current_url)
                pass

    def save_excel(self,tanggal):
        print('MASUK SAVE')
        df = pd.DataFrame(list(zip(self.url_list,self.user_names, self.user_comments, self.comments_date,self.bank_list,self.platform)), columns=["url","Name", "Comments", "Comments_Date","Bank","platform"])
        df1 = df.copy()
        df1 = pd.merge(df,self.df_url, left_on="url", right_on="URL", how = 'left' )
        df_final = df1[['url','Post_Date','Name','Comments','Comments_Date','Bank','platform']]
        df_final.to_excel(f'D:/scrap_fb_{tanggal}.xlsx')

if __name__ == "__main__":
    f_service = Service("C:\geckodriver.exe")
    driver = webdriver.Firefox(service=f_service)
    link = "https://mbasic.facebook.com/"
    email = 'modelcoba@gmail.com'
    password = 'skripsi2024!'

    # banks = ["bankocbcnisp","dbsdigibankID","PermataBank","CIMBIndonesia"] ## Masukan nama nama account FB yang ingin di scrap ke dalam list
    # banks = ["bankneocommerce","jeniusconnect","JadiJagoOfficial","blubybcadigital"] ## Masukan nama nama account FB yang ingin di scrap ke dalam list
    # banks = ["SeaBankIndonesia"]
    # banks = ["BRIofficialpage"]s
    # banks = ["BNI"]
    # banks = ["bankmandiri"]
    # banks = ["BankBCA"]
    banks = ["BankMegaID"]

    tanggal_akhir = datetime.date.today()
    tanggal_awal = tanggal_akhir - datetime.timedelta(days=7)
    
    # print( Tanggal_awal , Tanggal_akhir)

    
    scraper = FBScraper(driver)
    scraper.login(link,email,password)
    scraper.get_urls(banks)
    scraper.save_excel(tanggal_akhir)


    