from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.generalUtils import sleep, GeneralUtils, capture_and_save_screenshot


class Login:
    lnk_username = "LoginId"
    lnk_password = "txt_password"
    lnk_click = "btn_login"
    text_msg_conf_xpath = "//h6[text() = ' Demand Allocation ']"
    driver = webdriver
    def __init__(self, driver):
        self.driver = driver
        self.utils = GeneralUtils()

    def enter_usernamepassword(self, username,password):
            try:
                self.driver.find_element(By.NAME, self.lnk_username).send_keys(username)
                self.driver.find_element(By.ID, self.lnk_password).send_keys(password)
                self.driver.find_element(By.ID, self.lnk_click).click()
                return WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.XPATH, self.text_msg_conf_xpath))).text

            except Exception as e:
                print(f"An error occurred: {e}")
                capture_and_save_screenshot("Login_Error_Screenshot")
                self.utils.close_browser()