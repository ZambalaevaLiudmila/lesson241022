import time
import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from nose.tools import assert_equal, assert_true


def createDriver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.tutu.ru/')
    driver.maximize_window()
    return driver


def test_main_page():
    global listNonStop
    driver = createDriver()
    waitElement = wait.WebDriverWait(driver, 10)
    department = driver.find_element(By.XPATH, '//input[@name="city_from"]')
    department.click()
    department.send_keys('Москва (Россия)')
    waitElement.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="name_city"]')))
    arrow = driver.find_element(By.XPATH, '//input[@name="city_to"]')
    arrow.click()
    arrow.send_keys('Дубай (ОАЭ)')
    time.sleep(2)
    arrowCity = [driver.find_element(By.XPATH, '//span[@class="iata_code t-txt-s t-spacing"]')]
    if 'DXB' in arrowCity:
        arrowCity.click()
    dataDep = driver.find_element(By.XPATH, '//input[@name="date_from"]')
    dataDep.click()
    dataDep.send_keys('02.11.2022')
    dataBack = driver.find_element(By.XPATH, '//input[@name="date_back"]')
    dataBack.click()

    try:
        dataBack.send_keys('01.11.2022')
        driver.find_element(By.XPATH, '//button[@class="b-button__arrow__button j-button j-button-submit _blue _title j-submit_button"]').click()
        time.sleep(3)
        el = driver.find_element(By.XPATH, '//div[@id="qtip-3-content"]')
        assert_true(el, "Некорректная дата вылета. Проверьте, пожалуйста, и укажите правильную дату")
        s = 'Некорректная дата вылета. Проверьте, пожалуйста, и укажите правильную дату'
        if s == el.text:
            print('Некорректная дата вылета.')
        print(el)
    except Exception:
        print('except Exception')
    finally:
        dataBack.click()
        dataBack.send_keys('08.11.2022')
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[@class="b-button__arrow__button j-button j-button-submit _blue _title j-submit_button"]').click()
    time.sleep(3)

    SCROLL_PAUSE_TIME = 0.5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    listAll = []
    listOffer = waitElement.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@data-ti="route_main_line"]')))
    for search in listOffer:
        if "1 пересадка" == search.text:
            listAll.append(search.text)
            # print(search.text)
        elif "2 пересадки" == search.text:
            listAll.append(search.text)
            # print(search.text)
        elif "Прямой" == search.text:
            listAll.append(search.text)
            # print(search.text)
        else:
            listAll.append(search.text)
            print('Not found')

    print(listAll)
    print('Всего ', len(listAll)//2, 'рейсов')
    time.sleep(3)
    newList = []
    i = 0
    while i != (len(listAll)/2 + 1):
        newList.append([listAll[0], listAll[1]])
        del listAll[:2]
        i =+ 1

    # print(listAll)
    # print(len(listAll))
    print(newList)
    print(len(newList))

    listNonStop = []
    for i in range(len(newList)):
        if newList[i-1][0] == newList[i-1][1] == 'Прямой':
            listNonStop.append(newList[i-1])
            # print(newList[i-1])
        else:
            continue
            # print('нет совпадений')
    print(listNonStop)
    print('Количество прямых рейсов: ', len(listNonStop))
    print('Обратные рейсы: ')
    listBack = []
    for i in range(len(newList)):
        listBack.append(newList[i-1][1])
    print(listBack)


if __name__ == '__main__':
    test_main_page()