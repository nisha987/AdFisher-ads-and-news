import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains    # to move mouse over
# import browser_unit
import google_search                                                # interacting with Google Search

# strip html

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()  

class GoogleAdsUnit(google_search.GoogleSearchUnit):

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
        google_search.GoogleSearchUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
#         browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)

    def collect_ads(self, reloads, delay, site, file_name=None):
        if file_name == None:
            file_name = self.log_file
        rel = 0
        while (rel < reloads):  # number of reloads on sites to capture all ads
            time.sleep(delay)
            try:
                s = datetime.now()
                if(site == 'toi'):
                    self.save_ads_toi(file_name)
                elif(site == 'bbc'):
                    self.save_ads_bbc(file_name)
                elif(site == 'monster'):
                    self.save_ads_monster(file_name)
                else:
                    raw_input("No such site found: %s!" % site)
                e = datetime.now()
                self.log('measurement', 'loadtime', str(e-s))
            except:
                self.log('error', 'collecting ads', 'Error')
            rel = rel + 1

    def save_ads_toi(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://timesofindia.indiatimes.com/international-home")
        time.sleep(10)
        driver.execute_script('window.stop()')
        tim = str(datetime.now())
        frame = driver.find_element_by_xpath(".//iframe[@id='ad-left-timeswidget']")
    
        def scroll_element_into_view(driver, element):
            """Scroll element into view"""
            y = element.location['y']
            driver.execute_script('window.scrollTo(0, {0})'.format(y))
    
        scroll_element_into_view(driver, frame)
        driver.switch_to.frame(frame)
        ads = driver.find_elements_by_css_selector("html body table tbody tr td table")
        for ad in ads:
            aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
            bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
            t = aa[0].get_attribute('innerHTML')
            l = aa[1].get_attribute('innerHTML')
            b = bb[0].get_attribute('innerHTML')
            ad = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
            self.log('measurement', 'ad', ad)
        driver.switch_to.default_content()  

    def save_ads_bbc(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("https://www.bbc.com/news/uk")
        tim = str(datetime.now())
	
	frame = driver.find_elements_by_id("aswift_0")
	#lf=len(frame)
	#self.log(lf)
	   
		


        def scroll_element_into_view(driver, element):
            """Scroll element into view"""
            y = element.location['y']
            driver.execute_script('window.scrollTo(0, {0})'.format(y))
    
        #scroll_element_into_view(driver, frame)
        



	frame2 = frame.find_elements_by_css_selector("iframe#google_ads_frame1")
	driver.switch_to.frame(frame2)


        ads = driver.find_elements_by_css_selector("div.ads>div")
        for ad in ads:
            aa = ad.find_elements_by_class_name("title").get_attribute('innerHTML').strip()
            bb = ad.find_elements_by_class_name("body").get_attribute('innerHTML').strip()
            cc = ad.find_elements_by_class_name("url").get_attribute('innerHTML').strip()
            ad = strip_tags(tim+"@|"+aa+"@|"+bb+"@|"+cc).encode("utf8")
            self.log('measurement', 'ad', ad)
        driver.switch_to.default_content()


    def save_ads_monster(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://jobsearch.monster.com/")
        tim = str(datetime.now())
        els = driver.find_elements_by_css_selector("#SearchResults>.card-content>div")
        for el in els:
            title = el.find_element_by_css_selector('h2.title').get_attribute('innerHTML').strip()
            company = el.find_element_by_class_name('company').get_attribute('innerHTML').strip()
            location = el.find_element_by_css_selector('div.location a').get_attribute('innerHTML').strip()
            ad = strip_tags(tim+"@|"+title+"@|"+company+"@|"+location).encode("utf8")
            self.log('measurement', 'ad', ad)







