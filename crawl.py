import time
import cryptocode
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

class Linkedin:
    
    def __init__(self):
        
        self.binary = FirefoxBinary('/usr/bin/firefox')
        self.driver = webdriver.Firefox(firefox_binary=self.binary,executable_path='/home/britto/gecko/geckodriver')
        self.jobname = "Data Scientist"
        self.location = "India"
        
        self.creds = {}
        self.read_creds()
        
    def read_creds(self):
        
        with open('cred.txt','r') as credentials:
            for line in credentials.readlines():
                strip = line.split(":")
                self.creds[strip[0]] = strip[1].strip()
                
        self.creds['pass'] = cryptocode.decrypt(self.creds['pass'],self.creds['user'])
        
    def Login(self):
        
        time.sleep(4)
        
        self.driver.get('https://www.linkedin.com/login')
        
        username = self.driver.find_element_by_xpath("//*[@id='username']")
        password = self.driver.find_element_by_xpath("//*[@id='password']")
        
        username.send_keys(self.creds['user'])        
        password.send_keys(self.creds['pass'])
        
        time.sleep(7)
        
        self.driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
        
        print("Logged In")
        
    def search_jobs(self):
        
        time.sleep(10)
        
        self.driver.find_element_by_xpath('//*[@id="ember24"]').click()
        
        time.sleep(8)
        
        # jobname  = self.driver.find_element_by_xpath('//*[@placeholder="Search by title, skill, or company"]')
        # location = self.driver.find_element_by_xpath('//*[@placeholder="City, state, or zip code"]')
        
        jobname.send_keys(self.jobname)
        location.send_keys(self.location)
        
        time.sleep(4)
        
        self.driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/section/section[1]/div/div[2]/button[1]').click()
        
        print("Job Searched")
        
    def run(self):
        
        self.Login()
        # self.search_jobs()


def main():

    L = Linkedin()
    L.run()

if __name__ == "__main__":
    main()