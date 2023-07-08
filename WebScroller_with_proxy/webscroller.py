
import os
import sys
import time
import random
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service


alphabet = 'qwertyuiopasdfghjklzxcvbnmЕWC""(),|-> '
pre_results = "".join([x.strip() for x in open("settings\\general_settings.txt", encoding="utf-8").read() if x not in alphabet])
results = pre_results[5:].split(";")

chain, proxy_status = results[1], results[2]

if proxy_status == "YES":
    pre_proxy_info = (" ".join([t.strip() for t in open("settings\\proxy_settings.txt", encoding="utf-8").read() if t not in alphabet])).split("  ")
    proxy_info = [y.replace(" ", "") for y in pre_proxy_info if y != ""]
    trash, login, password, ports = proxy_info[0].strip(), proxy_info[1].strip(), proxy_info[2].strip(), proxy_info[3].strip()
    current_ports = ports.split(";")

global_time = int(str(datetime.now().time())[:2])
if 4 <= global_time <= 11: print("\nWEBSCROLLER. GOOD MORNING =)")
if 12 <= global_time <= 16: print("\nWEBSCROLLER. GOOD AFTERNOON =)")
if 17 <= global_time <= 23: print("\nWEBSCROLLER. GOOD EVENING =)")
if 0 <= global_time <= 3: print("\nWEBSCROLLER. IS IT TIME TO SLEEP? =)")

circles = int(input("\nEnter the number of laps: "))
input_text = input("Enter your search term: ")
if chain == "YES": 
    organization_name = input("Enter the name of the chain of stores: ")
    organization_adress = input("Enter the address of the organization you need: ")
elif chain == "NO": 
    organization_name = input("Enter organization name: ")
    organization_adress = input("Enter the address of the organization you need, if it is not needed, press Enter: ")
else: 
    print("Wrong setting 'Whether your organization is a network' was set in the settings")
    sys.exit()


def instruments(proxy_options):

    """Required Tools"""

    url = "https://yandex.com/"
    driver_path = os.path.abspath("driver\\geckodriver.exe")
    location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

    service = Service(executable_path=driver_path, log_path='nul')

    options = webdriver.FirefoxOptions() 
    options.add_argument('--log-level=3')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.binary_location=location

    if proxy_options == -920: driver = webdriver.Firefox(options=options, service=service)
    else: driver = webdriver.Firefox(options=options, service=service, seleniumwire_options=proxy_options)
    return [driver, url]

def printer1(src1):
    print(f"\nTIME - [{str(datetime.now().time())[:8]}] Scroll № {src1} started")
    
def printer2(src2):
    print(f"TIME - [{str(datetime.now().time())[:8]}] Scroll № {src2} started")

def bye(driver):
    driver.close()
    driver.quit()

def pre_searcher(driver):

    """Bypass other search menu"""

    slide_button = driver.find_element(By.CSS_SELECTOR, "span.link:nth-child(2)")
    for _ in range(8): {slide_button.click(), time.sleep(0.5)}
    time.sleep(2)
    more_button = driver.find_element(By.CSS_SELECTOR, ".more-item")
    more_button.click()
    time.sleep(2)

def searcher_helper(driver, iter):

    """Checking an individual establishment"""

    text_string = ""
    text_arr = ["null"]
    try: arg = driver.find_element(By.CSS_SELECTOR, f"div.showcase__item:nth-child({iter})")
    except Exception as error: 
        print(f"\nAn error has occurred\nMost likely you made a mistake in the name of the organization or Yandex did not issue it this time\n")
        sys.exit()
    text_string = arg.text
    text_arr = [u.lower() for u in text_string.split("\n")]
    iter += 1
    return  [text_arr, arg]

def searcher(driver):

    """Search for the right institution"""

    flag = True
    iter, cnt = 2, 0
    search_arr = ["null"]
    slide = driver.find_element(By.CSS_SELECTOR, "span.link_theme_normal:nth-child(3)")
    
    while flag:

        if cnt > 6:
            if cnt % 10 == 0:
                try:
                    for _ in range(random.randint(7, 8)): {slide.click(), time.sleep(1.2)}
                except Exception: pass
                finally:
                    out = searcher_helper(driver=driver, iter=iter)
                    search_arr, iter, cnt = out[0], iter+1, cnt+1
                    if organization_adress != "":
                        if f"{organization_name}".lower() == search_arr[0].lower() and\
                                    any(organization_adress.lower() in it for it in search_arr):
                            flag = False
                            return [out[1], iter]
                    else:
                        if f"{organization_name}".lower() == search_arr[0].lower():
                            flag = False
                            return [out[1], iter]
            else:
                out = searcher_helper(driver=driver, iter=iter)
                search_arr, iter, cnt = out[0], iter+1, cnt+1
                if organization_adress != "":
                    if f"{organization_name}".lower() == search_arr[0].lower() and\
                                any(organization_adress.lower() in it for it in search_arr):
                        flag = False
                        return [out[1], iter]
                else:
                    if f"{organization_name}".lower() == search_arr[0].lower():
                        flag = False
                        return [out[1], iter]
        else:
            out = searcher_helper(driver=driver, iter=iter)
            search_arr, iter, cnt = out[0], iter+1, cnt+1
            if organization_adress != "":
                if f"{organization_name}".lower() == search_arr[0].lower() and\
                            any(organization_adress.lower() in it for it in search_arr):
                    flag = False
                    return [out[1], iter]
            else:
                if f"{organization_name}".lower() == search_arr[0].lower():
                    flag = False
                    return [out[1], iter]
        
        if cnt >= 200:
            return "The program has already visited 200 organizations. Check the correctness of the information entered =)"
      
def comru(url, driver):

    if "yandex.ru" in url:
        pass
    else:
        __src = str(driver.current_url).replace("com", "ru", 1)
        driver.execute_script(f"window.open('{__src}')"), time.sleep(1), driver.close(), time.sleep(1)
        driver.switch_to.window(driver.window_handles[0]), time.sleep(3)

def root(url, driver, root_kount): 

    """Main function"""
    try:

        driver.get(url=url)
        time.sleep(2)
        
        search = driver.find_element(By.CSS_SELECTOR, "#text")
        search.send_keys(input_text)
        time.sleep(1)
        
        search_button = driver.find_element(By.CSS_SELECTOR, ".search3__button")
        search_button.click(), time.sleep(2)

        time.sleep(1)

        if chain == "YES":
            
            try: pre_searcher(driver=driver)
            except Exception as error: pass
            finally:
                time.sleep(1)
                comru(url=url, driver=driver)
                chain_button = driver.find_element(By.CSS_SELECTOR, ".select2_theme_default")
                chain_button.click()
                if chain_button.text != "Сети":
                    print("\nFor this request, Yandex does not allow you to select a specific chain of stores\nChange the settings in the settings or enter a different request\n")
                    return -100
                menu_test = driver.find_elements(By.CLASS_NAME, "menu__text")
                time.sleep(1)
                for ch in menu_test:
                    if organization_name.lower() == (ch.text).lower():
                        ch.click()
                time.sleep(1)
                args = searcher(driver=driver)
                if type(args[0]) == str: 
                    print(args[0])
                    return - 100

        elif chain == "NO":

            try: pre_searcher(driver=driver)
            except Exception as error: pass
            finally:
                comru(url=url, driver=driver)
                args = searcher(driver=driver)
                if type(args[0]) == str: 
                    print(args[0])
                    return - 100

        time.sleep(1)
        args[0].click()
        time.sleep(1)
        
        driver.refresh()
        time.sleep(1)
        bigi_buttons = driver.find_elements(By.CLASS_NAME, "tabs-menu__title")
        try:
            for i in "321": {bigi_buttons[int(i)].click(), time.sleep(4)}
        except IndexError: 
            for i in "21": {bigi_buttons[int(i)].click(), time.sleep(4)}
            
        mini_buttons = driver.find_elements(By.CLASS_NAME, "TabsMenu-Tab")
        try: 
            for j in range(6): {mini_buttons[j].click(), time.sleep(2)}
            srcs = [0, 1, 2]
            for _ in range(3):
                _arg = random.choice(srcs)
                mini_buttons[_arg].click()
                srcs.remove(_arg)
                time.sleep(3)

        except IndexError: time.sleep(3)

        mini_exit = driver.find_element(By.CSS_SELECTOR, ".Button2_view_clear")
        mini_exit.click()
        time.sleep(3)
        bigi_buttons[0].click()
        time.sleep(2)

        map_button = driver.find_element(By.XPATH, "/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/article/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div/div[1]/div/div/div")
        map_button.click()
        time.sleep(1)

        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)
        
        buttons_args = []
        buttons_selectors = ["._name_overview", "._name_gallery", "._name_reviews"]
        for itr1 in range(len(buttons_selectors)): 
            __arg = driver.find_element(By.CSS_SELECTOR, buttons_selectors[itr1])
            buttons_args.append(__arg)
        for itr2 in range(len(buttons_args)):
            buttons_args[itr2].click()
            time.sleep(5.5)

        driver.close()

        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()

        return args[1]
    
    finally:

        time.sleep(1), driver.refresh, time.sleep(1)
        bye(driver=driver)
        printer2(root_kount)

def start():

    """Initial function"""
    
    if proxy_status == "YES":
        proxy_kount = -1
        proxy_trigger = len(current_ports)
    for iter in range(1, circles+1):

        if proxy_status == "NO":
            printer1(iter)
            proxy_options = -920
            driver, url = instruments(proxy_options=proxy_options)
            
        elif proxy_status == "YES":
            proxy_kount += 1

            if proxy_kount == proxy_trigger:
                random.shuffle(current_ports)
                proxy_kount = 0

            proxy_options = {
                "proxy": {
                    "https": f"https://{login}:{password}@{current_ports[proxy_kount]}"
                }
            }
            printer1(iter)
            driver, url = instruments(proxy_options=proxy_options)
            
        else:
            printer1(iter)
            proxy_options = -920
            driver, url = instruments(proxy_options=proxy_options)
            
        __src = root(url=url, driver=driver, root_kount=iter)
        if __src == -100: 
            print(f"\nProgram exited by traversing {iter-1} circle(s)")
            break
        
    if __src != -100: 

        if chain == "YES":
            end = input(f"\nThe program ended after traversing the {iter} circle(s)\n"\
                                 f"The organization is currently in place numbered {__src-2} among other organizations in the same network\nPress Enter to end the program:")
            
        elif chain == "NO":   
            end = input(f"\nProgram terminated by traversing {iter} circle(s)\n"\
                                 f"The organization is currently located at the location number {__src-2}\nPress Enter to end the program:") 
        else: sys.exit()
        if end == "": sys.exit()
   
if __name__ == "__main__":
    start()

