import time
import traceback
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from Utilities.generalUtils import *


class ClinicianPage:
    # XPATH Locators
    # lnk_clinicianIcon = "(//a[contains(@href, 'phx/sch/ui/scheduler/clinicians/list/all')])[1]"
    lnk_arrow = "//i[@class='fa fa-arrow-circle-o-right']"
    link_clinician_calendar = "//span[text() = ' Calendar ']/.."
    click_search_button = "//div[text() ='Search Clinician Name/ID']/ancestor::*[3]"
    # week_calender_button = "//li[text()=' Weekly ']"
    calendar_show_check = ("//span[starts-with(normalize-space(text()), 'Showing') and substring(normalize-space(text()),"
                           " string-length(normalize-space(text())) - string-length('clinician(s)') + 1) = 'clinician(s)']")
    # calendar_show_check = "//span[contains(text(), 'Showing')]"

    # Shadow DOM CSS Selectors
    shadow_host_selector = "auth-scheduler-menu"
    shadow_inner_img_clinician_icon = "img[alt='clinician']"

    shadow_inner_img_arrow_icon = "img[alt='Logo']"

    shadow_inner_tag = "div"
    shadow_inner_img_link_clinician_calendar = "Calendar"

    def __init__(self, driver):
        self.driver = driver
        self.utils = GeneralUtils()

    def get_shadow_element(self, host_selector: str, inner_selector: str) -> WebElement:
        """
        Returns an element inside a shadow DOM.

        :param host_selector: CSS selector for the shadow host
        :param inner_selector: CSS selector for the element inside the shadow root
        :return: WebElement inside the shadow DOM
        """

        def _get_element(driver):
            shadow_host = self.driver.find_element(By.CSS_SELECTOR, host_selector)
            shadow_root = self.driver.execute_script("return arguments[0].shadowRoot", shadow_host)
            return shadow_root.find_element(By.CSS_SELECTOR, inner_selector)

        return default_wait(self.driver, custom_lambda=_get_element)

    def get_shadow_element_by_text(self, host_selector: str, tag: str, text: str) -> WebElement:
        """
        Returns a shadow DOM element based on tag and exact text content.
        This mimics the JavaScript query using text match.
        """
        # Array.
        # from
        # (document.querySelector('auth-scheduler-menu')?.shadowRoot?.querySelectorAll('div'))
        # .find(el= > el.textContent.trim() == = "Optimize Route")

        def _get_element(driver):
            script = f'''
                const host = document.querySelector("{host_selector}");
                if (!host) return null;
                const root = host.shadowRoot;
                const elements = root.querySelectorAll("{tag}");
                return Array.from(elements).find(el => el.textContent.trim() === "{text}");
            '''
            return self.driver.execute_script(script)

        return default_wait(self.driver, custom_lambda=lambda driver: _get_element(driver))

    def clinician_page(self):
        try:
            # Click on the clinician image from shadow DOM
            clinician_img = self.get_shadow_element(self.shadow_host_selector, self.shadow_inner_img_clinician_icon)
            clinician_img.click()
            time.sleep(20)

            # Click Clinician icon
            # link_clinician_calendar = self.get_shadow_element_by_text(
            #     self.shadow_host_selector, self.shadow_inner_tag, self.shadow_inner_img_link_clinician_calendar
            # )
            # link_clinician_calendar.click()
            # Click Clinician calendar icon
            link_clinician_calendar = self.get_shadow_element_by_text(
                self.shadow_host_selector, self.shadow_inner_tag, self.shadow_inner_img_link_clinician_calendar
            )

            # Use JS click instead of Selenium click
            self.driver.execute_script("arguments[0].click();", link_clinician_calendar)

            # Wait until calendar page is loaded
            default_wait(self.driver, By.XPATH, self.calendar_show_check, EC.visibility_of_element_located)

            # default_wait(self.driver, By.XPATH, self.lnk_clinicianIcon, EC.visibility_of_element_located).click()

            # Click arrow
            # arrow_img = self.get_shadow_element(self.shadow_host_selector, self.shadow_inner_img_arrow_icon)
            # arrow_img.click()
            #default_wait(self.driver, By.XPATH, self.lnk_arrow, EC.element_to_be_clickable).click()

            # Click Calendar tab
            # default_wait(self.driver, By.XPATH, self.link_clinician_calendar, EC.element_to_be_clickable).click()

            # Wait until calendar load confirmation
            default_wait(self.driver, By.XPATH, self.calendar_show_check, EC.visibility_of_element_located)
            capture_and_save_screenshot("Cliniciancalendarpage_reached_or_not_checking")

            # Click Weekly button
            # default_wait(self.driver, By.XPATH, self.week_calender_button, EC.element_to_be_clickable).click()

            # Click Search button
            default_wait(self.driver, By.XPATH, self.click_search_button, EC.element_to_be_clickable).click()

        except (TimeoutException, ElementNotInteractableException, NoSuchElementException) as e:
            exc_type, exc_value, exc_tb = traceback.sys.exc_info()
            lineno = exc_tb.tb_lineno
            exception_details = f"An error occurred: {e}. Line number: {lineno}."
            traceback_str = traceback.format_exc()

            print(exception_details)
            print(traceback_str)
            capture_and_save_screenshot("Error_Occured_cliniciancalendar_page")
