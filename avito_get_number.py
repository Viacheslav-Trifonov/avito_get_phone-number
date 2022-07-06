import time
import pytesseract
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from PIL import Image
import base64
import os

print('Укажите расположение файла tesseract.exe:')
tess_path = str(input())
pytesseract.pytesseract.tesseract_cmd = tess_path

print('Введите ссылку на объявление: ')
link = str(input())
print('Получение номера...')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options = options)
browser.get(link)

def main():
    try:
        button_num = browser.find_element(By.XPATH, "//button[@data-marker='item-phone-button/card']")
        button_num.click()
        time.sleep(2)
        image_num = browser.find_element(By.XPATH, "//img[@data-marker='phone-popup/phone-image']")
        code_img = image_num.get_attribute('src')[22:]
        decode_img = base64.b64decode(code_img)
        with open('phone_number.png', 'wb') as f:
            f.write(decode_img)
        img = Image.open('phone_number.png')
        cconfig = '--oem 3 --psm 13'
        text_number = pytesseract.image_to_string(img, config=cconfig)
        print(f'НОМЕР ТЕЛЕФОНА ДЛЯ СВЯЗИ: {text_number}')
        os.remove('phone_number.png')

    except NoSuchElementException:
        print('НЕОБХОДИМО ВОЙТИ НА САЙТ ИЛИ ЗАРЕГЕСТРИРОВАТЬСЯ')

    finally:
        time.sleep(2)
        browser.quit()

if __name__ == '__main__':
    main()
