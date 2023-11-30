from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import time
import csv
options = Options() 
options.add_argument('--headless')
# options.add_argument('--no-sandbox')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver', options=options)
driver.get('https://nj.betamerica.com/sports/golf/')
oddsdata = []
def getdata(eventurl,event):
    global oddsdata
    
    print(event)
    driver.get(eventurl)
    league = driver.find_element_by_id('league-view')
    league.find_element_by_class_name('tab-switch-btns-holder').find_elements_by_tag_name('li')[1].click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME ,"rj-instant-collapsible")))
    betdata = driver.find_elements_by_class_name('rj-instant-collapsible')
    for tmp in betdata:
        tmpbet = tmp.find_element_by_class_name('rj-instant-collapsible__trigger').get_attribute('textContent')
        print(tmpbet)
        tmpbet = tmpbet.split('|')[-2]
        print(tmpbet)
        tmpbet = tmpbet.split('-')[1]
        actions = ActionChains(driver)
        actions.move_to_element(tmp)
        actions.perform()
        # time.sleep(3)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME ,"rj-ev-list__prelive-outright__button-holder")))
        oddlist = tmp.find_elements_by_class_name('rj-ev-list__prelive-outright__button-holder')
        print(oddlist)
        for tmpodd in oddlist:
            data = {}
            data['bet'] = tmpbet
            data['event'] = event
            data['who'] = tmpodd.find_element_by_class_name('rj-ev-list__bet-btn__text').get_attribute('textContent')
            data['odds'] = tmpodd.find_element_by_class_name('rj-ev-list__bet-btn__odd').get_attribute('textContent')
            print(data['who'])
            print(data)
            oddsdata.append(data)
def main():
    evenlisturl = []
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME ,"rj-league-list__item-link")))
    driver.find_element_by_tag_name
    evenlist = driver.find_elements_by_class_name('rj-league-list__item-link')
    for tmp in evenlist:
        evenlisturl.append(tmp.get_attribute('href'))
    for tmp in evenlisturl:
        getdata(tmp,tmp.split('/')[-2])
    f = open("betamerica.csv", "w", encoding="utf-8-sig", newline='')
    fieldnames = ['event','bet','who','odds']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for tmp in oddsdata:
        writer.writerow(tmp)
    f.close()
    print(evenlisturl)
main()
print("*****************")
print(oddsdata)
driver.quit()
# responsive-block league-view-responsive-block full div
