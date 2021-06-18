from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import smtplib
from email.message import EmailMessage


email_address = ""
password = ""
birthday = ""

urlbiotech = f"https://termin.samedi.de/b/ambulantes-centrum-berlin/biontech/schnellster-termin/covid-impfung?birthday={birthday}"
urljj = f"https://termin.samedi.de/b/ambulantes-centrum-berlin/1/schnellster-termin/johnson-johnson-covid-impfung?birthday={birthday}"


def send_notification(vaccine_type, url):
    msg = EmailMessage()
    msg.set_content(url)
    msg['Subject'] = f'VAX AVAILABLE {vaccine_type}'
    msg['From'] = email_address
    msg['To'] = email_address
    mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    mail_server.login(email_address,password)
    mail_server.send_message(msg)
    mail_server.quit()
    print(f"Email sent to {email_address} for vaccine {vaccine_type}")


def check_availability(vaccine, url, driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "calendar")))
    try:
        elem = driver.find_element_by_xpath("*//div[contains(text(),'Datum und Uhrzeit')]")
    except NoSuchElementException:
        printf("FOUND AN APPOINTMENT!")
        send_notification(vaccine, url)
        return True
    print(f"no availability for {vaccine}....")
    return False


chrome_opts = Options()
# chrome_opts.add_argument("--headless")
chrome_opts.add_argument("--disable-extensions")
chrome_opts.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_opts)

found_biotech = False
found_jj = False
while True and not found_biotech and not found_jj:
    found_biotech = check_availability("biotech", urlbiotech, driver)
    found_jj = check_availability("johnson&johnson", urljj, driver)
    sleep(60)

driver.close()