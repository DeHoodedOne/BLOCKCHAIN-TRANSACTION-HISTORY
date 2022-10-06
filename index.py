import selenium.webdriver as webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep


PAXFUL = "https://www.blockchain.com/btc/address/3665WBjeuTv3yVjR1K26zpaH9ysrt9h3Xa?page=1"

chrome_path = "C:\Development\chromedriver_win32\chromedriver.exe"
service = Service(chrome_path)
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options. add_argument("--incognito")


driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)
driver.get(PAXFUL)

driver.find_element(By.CSS_SELECTOR, ".dKFNB .egyuLV").click()
sleep(1)
driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[2]/div/div/div[1]/div/div[2]/div[3]/div/div[1]').click()
transactions = driver.find_elements(By.CSS_SELECTOR, ".ifDzmR")
print(len(transactions))

hash_IDs = []
send_receive = []
transaction_dates = []
withdrawal_addresses = []
for n in range(83):
    try:
        for i in range(len(transactions)):
            try:
                hash_ID = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div[{i + 2}]/div[2]/div[1]/div[2]/a')
                hash_IDs.append(hash_ID.text)
            except StaleElementReferenceException:
                driver.refresh()
                sleep(3)
                hash_ID = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div[{i + 2}]/div[2]/div[1]/div[2]/a')
                hash_IDs.append(hash_ID.text)
            try:
                sent_or_receive = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div[{i + 2}]/div[1]/div[2]/div[2]/div/div/span')
                send_receive.append(sent_or_receive.text)
            except StaleElementReferenceException:
                driver.refresh()
                sleep(3)
                sent_or_receive = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div[{i + 2}]/div[1]/div[2]/div[2]/div/div/span')
                send_receive.append(sent_or_receive.text)
            try:
                tranx_date = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div[{i + 2}]/div[2]/div[2]/div[2]/div/span')
                transaction_dates.append(tranx_date.text)
            except StaleElementReferenceException:
                driver.refresh()
                sleep(3)
                tranx_date = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div[{i + 2}]/div[2]/div[2]/div[2]/div/span')
                transaction_dates.append(tranx_date.text)
            if "+" in sent_or_receive.text:
                w_address = "3665WBjeuTv3yVjR1K26zpaH9ysrt9h3Xa"
                withdrawal_addresses.append(w_address)
            elif "-" in sent_or_receive.text:
                try:
                    w_address = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div[{i + 2}]/div[3]/div[2]/div[2]/div/div[1]/div/a')
                    withdrawal_addresses.append(w_address.text)
                except StaleElementReferenceException:
                    driver.refresh()
                    sleep(3)
                    w_address = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[3]/div[2]/div/div/div[2]/div/div[2]/div/div[{i + 2}]/div[3]/div[2]/div[2]/div/div[1]/div/a')
                    withdrawal_addresses.append(w_address.text)
        sleep(1)
        try:
            driver.find_element(By.CSS_SELECTOR, '.lhGqdm .gXFlXe:last-child .coriBa').click()
        except ElementClickInterceptedException:
            driver.refresh()
            sleep(3)
            driver.find_element(By.CSS_SELECTOR, '.lhGqdm .gXFlXe:last-child .coriBa').click()
        print(f"Page {n + 1} complete")
        sleep(1)
    except NoSuchElementException:
        break

for q in range(len(hash_IDs)):
    if q == 0:
        with open("BLOCKCHAINUSD.txt", mode="a") as file:
            file.write(f"HASH ID|SEND - RECEIVE|WALLET ADDRESSES|TIMESTAMP\n")
    try:
        with open("BLOCKCHAINUSD.txt", mode="a") as file:
            file.write(f"{hash_IDs[q]}|{send_receive[q]}|{withdrawal_addresses[q]}|{transaction_dates[q]}\n")
    except UnicodeEncodeError:
        pass
    except IndexError:
        pass

print(hash_IDs)
print(send_receive)
print(transaction_dates)
print(withdrawal_addresses)
print(len(hash_IDs))
print(len(send_receive))
print(len(transaction_dates))
print(len(withdrawal_addresses))
