from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from datetime import datetime
from colorama import Fore, Style
import requests
import os
import json
from clint.textui import colored
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

datapath = os.path.exists('data.json')

if datapath == False:
    open('data.json', 'x')
    with open('data.json', 'w') as data:
        info = {
            "amazon": {"sent": False, "timestamp": None, "silenced": False},
            "bestbuy": {"sent": False, "timestamp": None, "silenced": False},
            "target": {"sent": False, "timestamp": None, "silenced": False},
            "walmart": {"sent": False, "timestamp": None, "silenced": False},
            "gamestop": {"sent": False, "timestamp": None, "silenced": False}
        }
        json.dump(info, data, indent=2)
        print('Data file created.')


PATH = r"C:\Program Files (x86)\geckodriver.exe"

options = Options()
options.add_argument('--headless')

address = 'usa.eclipse.spaceproxies.com:12145:DigEsC7D:dDlahhCEbCyh5YA4KMKKZc3Va7gVcLMlLTRGjx705zcywWl3wzpr7WKF5NAFKdxXEZHHA-frnUjXbz9J'
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': address,
    'ftpProxy': address,
    'sslProxy': address
})


driver = webdriver.Firefox(executable_path=PATH, proxy=proxy)
driver.set_page_load_timeout(10)

webhookurl = 'https://discord.com/api/webhooks/800146160718577715/w2XEVDKR-lmqEIwgyMIhyBjnlWI42Zwlgx5x3JphmASg_Chxfcm_7ZJqNAFmxcOUlV5M'

onlinemess = {
    "content": "<@592001125511725075> StockChecker is now online!"
}

times =  1
while True:
    try:
        driver.get("https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp")
    except TimeoutException:
        driver.execute_script("window.stop();")
    title = driver.title
    window_before = driver.window_handles[0]
    try:
        driver.find_element_by_id("outOfStock")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'{current_time} [{title}]:' + colored.red(' OUT OF STOCK'))
    except NoSuchElementException:
        try:
            driver.get("https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp")
        except TimeoutException:
            driver.find_element_by_id('outOfStock')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time} [{title}]:' + colored.red(' OUT OF STOCK'))
        try:
            driver.find_element_by_id('outOfStock')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time} [{title}]:' + colored.red(' OUT OF STOCK'))
        except:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time} [{title}]:' + colored.green(' IN STOCK'))
            with open('data.json') as data:
                global i
                content = data.read()
                i = json.loads(content)
                data.close()
            timenow = time.time()
            if i['amazon']['sent'] == False and i['amazon']['silenced'] == False:
                message = {
                    "content": "<@592001125511725075> <@738177536873201696> [AMAZON]: IN STOCK [URL]: https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp"
                }
                requests.post(webhookurl, data=message)
                i['amazon']['sent'] = True
                i['amazon']['timestamp'] = timenow
                with open('data.json' , 'w') as data:
                    json.dump(i, data, indent=2)
            elif i['amazon']['sent'] == True and i['amazon']['silenced'] == False:
                if timenow - i['amazon']['timestamp'] >= 2:
                    message = {
                        "content": "<@592001125511725075> <@738177536873201696> [AMAZON]: IN STOCK [URL]: https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG?ref_=ast_sto_dp"
                    }
                    requests.post(webhookurl, data=message)
                    i['amazon']['timestamp'] = timenow
                    with open('data.json', 'w') as data:
                        json.dump(i, data, indent=2)
    driver.execute_script('window.open()')
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    try:
        driver.get("https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149")
    except TimeoutException:
        driver.execute_script("window.stop();")
    title = driver.title
    try:
        button = driver.find_element_by_id("fulfillment-add-to-cart-button-ad441ed6-7599-487f-b53f-605d2ea0490d")
        href_data = button.get_attribute('href')
        if href_data is None:
            is_clickable = False
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time} [{title}]:' + colored.red(' OUT OF STOCK'))
        else:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time} [{title}]:' + colored.green(' IN STOCK'))
            message = {
                "content": "<@738177536873201696> <@592001125511725075> [BEST BUY]: IN STOCK [URL]: https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149"
            }
            requests.post(webhookurl, data=message)
    except:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'{current_time} [{title}]:' + colored.red(' OUT OF STOCK'))
    driver.execute_script('window.open()')
    driver.switch_to_window(driver.window_handles[1])
    try:
        driver.get("https://www.target.com/p/playstation-5-console/-/A-81114595")
    except TimeoutException:
        driver.execute_script("window.stop();")
    title = driver.title
    driver.switch_to_window(driver.window_handles[0])
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    try:
        driver.find_element_by_xpath('/html/body/div[1]/div/div[5]/div/div[2]/div[3]/div[1]/div/div[1]/div')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'{current_time} [{title}]:' + colored.red(' OUT OF STOCK'))
    except NoSuchElementException:
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div[1]")
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time} [{title}]:' + colored.red(' OUT OF STOCK'))
        except NoSuchElementException:
            try:
                driver.get("https://www.target.com/p/playstation-5-console/-/A-81114595")
                driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/div[1]")
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(f'{current_time} [{title}]:' + colored.red(' OUT OF STOCK'))
            except NoSuchElementException:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(f'{current_time} [{title}]:' + colored.green(' IN STOCK'))
                message = {
                    "content": "<@592001125511725075> <@738177536873201696> [TARGET]: IN STOCK [URL]: https://www.target.com/p/playstation-5-console/-/A-81114595"
                }
                requests.post(webhookurl, data=message)
    
    driver.execute_script('window.open()')
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    if times == 3:
        try:
            driver.get('https://www.walmart.com/ip/PlayStation5-Console/363472942')
        except TimeoutException:
            driver.execute_script('window.stop()')
        title = 'Playsation 5: Walmart'
        tabname = driver.title
        if tabname == 'Error Page':
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time} [{title}]:' + colored.red(' OUT OF STOCK'))
        else:
            try:
                driver.find_element_by_xpath('/html/body/div[1]/div[3]/div')
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(f'{current_time} [{title}]:' + colored.red(' OUT OF STOCK'))
            except NoSuchElementException:
                try:
                    driver.find_element_by_id('recaptcha-anchor-label')
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print(f'{current_time} [{title}]:' + colored.yellow(' VERIFICATION ERROR'))
                except NoSuchElementException:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    print(f'{current_time} [{title}]:' + colored.green(' IN STOCK'))
                    message = {
                        "content": "<@592001125511725075> <@738177536873201696> [WALMART]: IN STOCK [URL]: https://www.walmart.com/ip/PlayStation5-Console/363472942"
                    }
            requests.post(webhookurl, data=message)
    driver.execute_script('window.open()')
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    try:
        driver.get('https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html')
    except TimeoutException:
        driver.execute_script('window.stop()')
    title = driver.title
    try:
        driver.find_element_by_xpath("//button[@class='add-to-cart btn btn-primary '][.='Add to Cart']")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'{current_time} [{title}]:' + colored.green(' IN STOCK'))
        message = {
            "content": "<@592001125511725075> <@738177536873201696> [GAMESTOP]: IN STOCK [URL]: https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html"
        }
        requests.post(webhookurl, data=message)
    except NoSuchElementException:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'{current_time} [{title}]:' + colored.red(' OUT OF STOCK'))
    if times != 3:
        times = times + 1
    else:
        times = 1
    time.sleep(4)
