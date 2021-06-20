import time
import cryptocode
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

class Linkedin:
    
    def __init__(self,job,location,encrypt=True):
        
        self.binary = FirefoxBinary('/usr/bin/firefox')
        self.driver = webdriver.Firefox(firefox_binary=self.binary,executable_path='/home/britto/gecko/geckodriver')
        self.jobname = job
        self.location = location
        self.encrypt = encrypt
        self.number_of_pages_to_fetch = 10
        
        self.job_details = {}
        self.creds = {}
        self.read_creds()
        
    def read_creds(self):
        
        with open('cred.txt','r') as credentials:
            for line in credentials.readlines():
                strip = line.split(":")
                self.creds[strip[0]] = strip[1].strip()
        
        if self.encrypt:
            self.creds['pass'] = cryptocode.decrypt(self.creds['pass'],self.creds['user'])
        
    def Login(self):
        
        time.sleep(4)
        
        self.driver.get('https://www.linkedin.com/login')
        
        time.sleep(6)
        
        username = self.driver.find_element_by_xpath("//*[@id='username']")
        password = self.driver.find_element_by_xpath("//*[@id='password']")
        
        username.send_keys(self.creds['user'])
        password.send_keys(self.creds['pass'])
        
        time.sleep(2)
        
        self.driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
        
        print("Logged In")
        
    def search_jobs(self):
        
        time.sleep(10)
        
        self.driver.find_element_by_xpath('/html/body/div[6]/aside/div[1]/header/section[1]').click()
        self.driver.find_element_by_xpath('//*[@data-test-global-nav-link="jobs"]').click()
        
        time.sleep(8)
        
        jobname  = self.driver.find_element_by_xpath('//*[contains(@id,"jobs-search-box-keyword-id-ember")]')
        location = self.driver.find_element_by_xpath('//*[contains(@id,"jobs-search-box-location-id-ember")]')
        
        jobname.send_keys(self.jobname)
        location.send_keys(self.location)
        
        time.sleep(4)
        
        self.driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/section/section[1]/div/div[2]/button[1]').click()
        
        print("Job Searched")
        
    
    def scroll_and_get_all_jobs(self):
    
        total_jobs_found_in_page  = 0
        all_jobs = self.driver.find_elements_by_xpath('//div[@class="flex-grow-1 artdeco-entity-lockup__content ember-view"]')
        
        while total_jobs_found_in_page!=len(all_jobs):
            
            total_jobs_found_in_page = len(all_jobs)
            all_jobs[-1].click()
            all_jobs = self.driver.find_elements_by_xpath('//div[@class="flex-grow-1 artdeco-entity-lockup__content ember-view"]')
            
        return all_jobs
        
    def get_all_job_details(self,all_jobs,page):
    
        for i,job in enumerate(all_jobs):
            
            i = (page*100)+i
            
            time.sleep(5)
            print(job.text)
            job.click()
            self.job_details[i] = {}
            
            job_brief = job.text.split("\n")
            self.job_details[i]["Position"] = job_brief[0]
            self.job_details[i]["Company"] = job_brief[1]
            self.job_details[i]["Location"] = job_brief[2]
            
            job_d = self.driver.find_element_by_xpath('//*[@id="job-details"]')
            description = job_d.find_element_by_xpath('.//span[*]').text
            
            self.job_details[i]['JD'] = description
            
    def go_to_next_page(self):
    
        current_page = int(self.driver.find_element_by_xpath('//button[contains(@aria-current,"true")]').text)
        next_p = self.driver.find_element_by_xpath('//button[@aria-label="Page {}"]'.format(str(current_page+1)))
        next_p.click()
        
        return current_page

    def run(self):
        
        self.Login()
        self.search_jobs()

        time.sleep(10)

        current_p = 0

        while current_p < self.number_of_pages_to_fetch:

            all_jobs = self.scroll_and_get_all_jobs()
            self.get_all_job_details(all_jobs,current_p)
            current_p = self.go_to_next_page()

        print(self.job_details)

def main():

    L = Linkedin("Data Scientist",'India',encrypt=False)
    L.run()

if __name__ == "__main__":
    main()