import datetime
import openpyxl
import os
import random
import time
import pandas as pd
import traceback
# import arachnae
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import calendar
# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

class InstagramScraper:
    def __init__(self, driver, today=datetime.date.today()):
        self.driver = driver
        self.cutoff_awal = None 
        self.cutoff_akhir = None
        self.comment_awal = None
        self.comment_akhir = None
        self.today = today
        self.get_cutoff_comment_time(self.today)
         ## Save path
        # datepath = '2023-04-24'
        # \\OneDrive\\1_bankmega\\scraping_results\\
        self.savefilepath = f"D:{self.today.strftime('%Y-%m-%d')}"
        os.makedirs(self.savefilepath, exist_ok=True)
        self.path = f"D:/scrap_ig_{today}.xlsx"
        

    def get_cutoff_comment_time(self,today):
        # Get the current date
        today = datetime.date.today()

        # Calculate the current weekday
        current_weekday = today.weekday()

        # Calculate the first day of the last week
        first_day_of_last_week = today - datetime.timedelta(days=current_weekday + 7)

        # Calculate the last day of the last week
        last_day_of_last_week = first_day_of_last_week + datetime.timedelta(days=7 - 2)

        # Calculate the previous month and year
        current_month = today.month
        current_year = today.year
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_year = current_year - 1 if previous_month == 12 else current_year

        # Calculate the last day of the previous month
        last_day_of_previous_month = (datetime.date(current_year, current_month, 1) - datetime.timedelta(days=1)).day

        # Calculate the date that is one month before today plus 10 days
        one_month_before = datetime.date(previous_year, previous_month, min(today.day, last_day_of_previous_month)) + datetime.timedelta(days=8)

        print("One month before today + 10 days:", one_month_before)
        print("First day of last week - 1:", first_day_of_last_week - datetime.timedelta(days=1))
        print("Last day of last week - 1:", last_day_of_last_week - datetime.timedelta(days=1))


        self.cutoff_awal = datetime.datetime.combine(one_month_before, datetime.datetime.min.time()) 
        self.cutoff_akhir = datetime.datetime.combine(last_day_of_last_week, datetime.datetime.max.time())
        self.comment_awal = datetime.datetime.combine(first_day_of_last_week, datetime.datetime.min.time())
        self.comment_akhir = datetime.datetime.combine(last_day_of_last_week, datetime.datetime.max.time())
        print("self.cutoff_awal",self.cutoff_awal)
        print("self.cutoff_akhir",self.cutoff_akhir)
        print("self.comment_awal",self.comment_awal)
        print("self.comment_akhir",self.comment_akhir)
        return one_month_before, first_day_of_last_week, last_day_of_last_week

        


    def login(self, USERNAME, PASSWORD):
        ## Login
        self.driver.get("http://www.instagram.com")
        time.sleep(2.3)
        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
        username.clear()
        username.send_keys(USERNAME)
        time.sleep(2.12)
        password.clear()
        password.send_keys(PASSWORD)
        time.sleep(3.35)
        button = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        time.sleep(5.35)

    def get_comments(self,username: str):
        try:
            user_names = []
            comment_ids = []
            user_comments = []
            comment_date = []
            post_date = []
            post_url = []
            pinned_post_counter=0 #patience if post not in cutoff
            

            self.driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(1)

            # start from latest post then click next until cutoff (first block to be exact)
            latest_post = WebDriverWait(self.driver, timeout=40).until(lambda d: d.find_element(By.CLASS_NAME,"_aabd"))
            latest_post.click()
            while True:
                time.sleep(3.53)
                post_time = WebDriverWait(self.driver, timeout=40).until(lambda d: d.find_element(By.CLASS_NAME,"_aaqe"))
            
                if (datetime.datetime.strptime(post_time.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ") < self.cutoff_awal or datetime.datetime.strptime(post_time.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ") > self.cutoff_akhir) and pinned_post_counter <= 6:
                    print('masuk next')
                    pinned_post_counter +=1
                    time.sleep(0.72)
                    next_button = WebDriverWait(self.driver, timeout=40).until(lambda d: d.find_element(By.CLASS_NAME,"_aaqg"))
                    next_button.click()
            

                elif datetime.datetime.strptime(post_time.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ") <= self.cutoff_akhir and datetime.datetime.strptime(post_time.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ") >= self.cutoff_awal:
                    print('\n')
                    try:
                        #print(datetime.strptime(post_time.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ"))
                        time.sleep(3)
                        
                        # "Load more comments" until end
                        i=1
                        while True:
                            try:
                                WebDriverWait(self.driver, timeout=1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button"))).click()
                                # /html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button
                                # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button
                                # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button
                                # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button
                                # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button 
                                # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button
                                # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button       
                                # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button
                                # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button
                                # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button
                                # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button
                                # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/li/div/button
                                time.sleep(3)
                                print(f"'LOAD MORE COMMENTS' button is clicked. #{i}")
                                i+=1
                                
                            except:
                                print("No more 'LOAD MORE COMMENTS' button to be clicked\n")
                                break
                        

                        # "View Replies", wait until all located                
                        # view_reply_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'li > ul > li > div > button[class="_acan _acao _acas _aj1-"]')
                        view_reply_buttons = self.driver.find_elements(By.XPATH, '/html/body/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div/ul/li/ul/li/div/button')
                        # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[1]/ul/li/ul/li/div/button
                        # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[2]/ul/li/ul/li/div/button
                        # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[4]/ul/li/ul/li/div/button
                        # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[9]/ul/li/ul/li/div/button
                        # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[10]/ul/li/ul/li/div/button
                        # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[3]/ul/li/ul/li/div/button
                        # /html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[12]/ul/li/ul/li/div/button
                        # /html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[99]/ul/li/ul/li/div/button
                        print(len(view_reply_buttons))
                        j=1
                        for button in range(len(view_reply_buttons)):
                            view_reply_buttons[button].click()
                            print(f"'VIEW REPLIES' button is clicked. #{j}")
                            j+=1
                            time.sleep(1)
                        print("No more 'VIEW REPLIES' button to be clicked\n")
                        
                    except Exception as e:
                        print(e)
                        pass
                    
                    time.sleep(1)

                    comment = self.driver.find_elements(By.XPATH, '//ul[@class="_a9ym"]/div/li/div[@class="_a9zm"]')
                    
                    for i,c in enumerate(comment):
                        container = c.find_element(By.XPATH,'.//div[@class="_a9zr"]')
                        comment_time = c.find_element(By.XPATH,'.//a/time[contains(@class,"_a9ze _a9zf")]')

                        if  datetime.datetime.strptime(comment_time.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ") <= self.comment_akhir and datetime.datetime.strptime(comment_time.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ") >= self.comment_awal :  
                            name = container.find_element(By.CLASS_NAME,"_a9zc").text
                            content = container.find_elements(By.CLASS_NAME,"_a9zs")[0].text
                            content = content.replace("\n", " ").strip().rstrip()

                            commentid_xpath = ".//a[@role='link' and .//time[contains(@class,'_a9ze _a9zf')]]"
                            commentid = c.find_element(By.XPATH, commentid_xpath).get_attribute("href")

                            comments_date = datetime.datetime.strptime(comment_time.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ")
                            postdate = datetime.datetime.strptime(post_time.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ")

                            user_names.append(name)
                            comment_ids.append(commentid)
                            comment_date.append(comments_date)
                            user_comments.append(content)
                            post_date.append(postdate)
                            post_url.append(self.driver.current_url)

                            print(i+1,";",commentid,";",comments_date,";",name,";",content,";",postdate,";",self.driver.current_url)

                        else:
                            pass
                        

                elif datetime.datetime.strptime(post_time.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ") < self.cutoff_awal:
                    break  

                # click next button
                time.sleep(1)
                next_button = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element(By.CLASS_NAME,"_aaqg"))
                next_button.click()
        
            return user_names, comment_ids, user_comments, post_date, post_url, comment_date # comment_ids,

        except:
            print(f"Error: Saving current scraped comments for username: {username}\n")
            print(traceback.format_exc())
            # user_names = ['n/a']
            # comment_ids = ['n/a']
            # user_comments = ['n/a']
            # comment_date = ['1970-01-01 00:00:00']
            # post_date = ['n/a']
            # post_url = ['1970-01-01 00:00:00']
            return user_names, comment_ids, user_comments, post_date, post_url, comment_date # comment_ids,
            pass


    # Convert datetime format
    # dt > utc+7 > str
    def datetime_format(self,comment_date_column):
        """
        change datetime format and convert to UTC+7
        `comment_date_column`: column of comment_date
        """
        for i in range(len(comment_date_column)):
            comment_date_column[i] = (comment_date_column[i] + datetime.timedelta(hours=7)).strftime("%Y-%m-%d")
            
        return comment_date_column
    
    def scrape_save_excel(self,acc):
       
        user_names, comment_ids, user_comments, post_date, post_url, comment_date = self.get_comments(username=acc)
        # print(user_names, comment_ids, user_comments, post_date, post_url, comment_date)
        # df_mega = pd.DataFrame(list(zip(user_names, comment_ids, user_comments, post_date, post_url, comment_date)), columns=["name","comment_id","comments","post_date","post_url","comment_date"]) # "comment_id",
        df_mega = pd.DataFrame(list(zip(post_url, post_date, user_names, user_comments, comment_date)), columns=["post_url","post_date","username","comment","comment_date"]) # "comment_id",
        # print(df_mega)
        df_mega = df_mega[df_mega["username"] != f"{acc}\nVerified"]
        df_mega.reset_index(drop=True, inplace=True)
        df_mega["bank"] = acc
        df_mega["platfrom"] = "Instagram"
        df_mega["comment_date"] = self.datetime_format(df_mega["comment_date"])

        with pd.ExcelWriter(self.path, engine='openpyxl') as writer:
            df_mega.to_excel(writer, sheet_name=acc)
        print(f'scrape {acc} done')

if __name__ == "__main__":
    USERNAME="mizuki.zenith"
    PASSWORD='skripsi2024!'
    ## Selenium Config

    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("--disable-extensions")
    option.add_argument("USER AGENT")
    f_service = Service("C:\geckodriver.exe")
    driver = webdriver.Firefox(service=f_service)
    today = datetime.date.today()
    scraper = InstagramScraper(driver,today)
    scraper.login(USERNAME,PASSWORD)

    accounts = [
                "bankmegaid"
                # "ocbc_nisp",
                # "dbsbankid",
                # "permatabank",
                # "cimb_niaga",
                # "mydanamon",
                # "seabank.id"
                # "blubybcadigital",
                # "bankneocommerce",
                # "jeniusconnect",
                # "allobank"
                # "jadijago",
                # "bni46"
                # "goodlifebca",
                # "bankbri_id",
                # "bankmandiri"
                ]
    for acc in accounts:
        scraper.scrape_save_excel(acc)

    




    # ## Save path
    # datepath = datetime.date.today().strftime("%Y-%m-%d")
    # # datepath = '2023-04-24'
    # savefilepath = f"D:\\OneDrive\\1_bankmega\\scraping_results\\{datepath}"
    # os.makedirs(savefilepath, exist_ok=True)
    # path = f'{savefilepath}\\{datepath} Scraping Instagram All Banks.xlsx'

