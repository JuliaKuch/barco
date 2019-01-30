import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.yield_fixture(scope='session')
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.yield_fixture(scope='session')
def driver_open_connection():
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://kannan.overture.barco.cloud/#/')
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.visibility_of_element_located((By.ID, 'username')))

    driver.find_element_by_id("username").send_keys('medialon')
    driver.find_element_by_id("password").send_keys('medialon')
    driver.find_element_by_id("kc-login").click()

    wait.until(EC.visibility_of_element_located((By.ID, 'endtoend-user')))

    yield driver
    driver.close()