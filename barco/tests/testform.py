import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

hostname = 'https://kannan.overture.barco.cloud/#/'

# def tearDown(self):
#     self.driver.quit()

# test utils

def login(driver, login="medialon", password="medialon"):
    driver.get('https://kannan.overture.barco.cloud/#/')
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.visibility_of_element_located((By.ID, 'username')))
    driver.find_element_by_id("username").send_keys(str(login))
    driver.find_element_by_id("password").send_keys(str(password))
    driver.find_element_by_id("kc-login").click()


def logout(driver):
    driver.find_element_by_id("endtoend-user").click()
    driver.find_element_by_id("endtoend-logout").click()



@pytest.mark.parametrize("login, password, result",
                             [("medialon1", "medialon1", False),
                                ("medialon", "medialon", True)
                              ])
def test_login(driver, login, password, result):
    driver.get(hostname)
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.visibility_of_element_located((By.ID, 'username')))

    login_field = driver.find_element_by_id("username")
    password_field = driver.find_element_by_id("password")
    submit_button = driver.find_element_by_id("kc-login")

    login_field.send_keys(login)
    password_field.send_keys(password)
    submit_button.click()
    try:
        if result:
            wait.until(EC.visibility_of_element_located((By.ID, 'endtoend-user')))
            assert driver.find_element_by_xpath("//*[contains(text(), '"+login+"')]") is not None
            logout(driver)
        else:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'alert-error')))
            assert driver.find_element_by_xpath("//*[contains(text(), 'Invalid username or password.')]") is not None
    finally:
        print ("Test login = "+login+" and pass = "+password)


def test_room(driver):
    wait = WebDriverWait(driver, 20)
    login(driver)
    try:
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'loader-container')))
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.landmark-text.ng-binding")))
        elem_room = driver.find_element_by_css_selector("span.landmark-text.ng-binding")
        elem_room.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span.landmark-text.ng-binding"), r"projector"))
        driver.find_element_by_xpath("//span[contains(text(), 'projector')]").click()
    finally:
        assert driver.find_element_by_css_selector("div.control-panel-title-text.ng-binding").is_displayed()
        print("Test room")
        logout(driver)

def test_magic_menu(driver):
    login(driver)
    window_before = driver.window_handles[0]
    print window_before
    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.ID, "endtoend-app_menu")))
    driver.find_element_by_id("endtoend-app_menu").click()

    wait.until(EC.visibility_of_element_located((By.ID, "endtoend-magic_menu_app")))
    driver.find_element_by_id("endtoend-magic_menu_app").click()
    time.sleep(5)
    window_after = driver.window_handles[1]
    driver.switch_to_window(window_after)
    print window_after
    assert "Overture Magic Menu" in driver.title
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.med-page-container")))
    driver.find_element_by_css_selector("div.med-page-container").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.med-display-label.ng-binding")))
    assert driver.find_element_by_css_selector('div.med-display-label.ng-binding').is_displayed()

@pytest.mark.test_depends_on(test_magic_menu, login)
def test_projector_panel(driver):
    driver.find_element_by_xpath("//*[contains(text(), 'Power On')]").click()
    time.sleep(1)
    assert driver.find_elements_by_css_selector("div.med-display-value.ng-binding").text == "On"
    driver.find_element_by_xpath("//*[contains(text(), 'Power Off')]").click()
    assert driver.find_elements_by_css_selector("div.med-display-value.ng-binding")[1].text == "Off"



