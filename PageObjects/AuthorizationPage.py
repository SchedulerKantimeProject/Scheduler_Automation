import traceback
from selenium.common import ElementNotInteractableException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Utilities.generalUtils import default_wait, GeneralUtils, _convert_date, sleep, capture_and_save_screenshot
from test_main import logger

class AuthorizationPage:
    lnk_authorizationIcon = "(//a[contains(@href, 'phx/sch/ui/scheduler/authorizations/list/all')])[1]"
    lnk_arrow = "//i[@class='fa fa-arrow-circle-o-right']"
    lnk_AddAuthorization_btm = "//span[text() = ' Add Authorization ']/.."
    lnk_search_client_btm = "//div[text()= 'Enter Client Name']/.."
    lnk_enter_client_name = "//div[text()= 'Enter Client Name']/following-sibling::div/input[@type='text']"
    select_client_name = "//div[@class ='ng-dropdown-panel-items scroll-host']/div/div"
    AuthorizationNo = "//input[@placeholder= 'Enter Authorization Number']"
    AuthReceivedDate = "//input[@id='authorization_received_date']"
    AuthStartDate = "//input[@id='start_date']"
    AuthEndDate = "//input[@id='end_date']"
    orderAllocations = "//input[@id='orderAllocations']"
    NPINo = "//input[@id='npiNumber']"
    discipline = "//select[@id='discipline']"
    authorizedquantity = "//input[@formcontrolname='authorized_quantity']"
    unitofmeasure = "//select[@id='unit-of-measure']"
    utilisationrule = "//select[@id='utilisation_rule']"

    def __init__(self, driver):
        self.driver = driver
        self.utils = GeneralUtils()

    def Authorization_Page(self):
        try:
            sleep(5)
            default_wait(self.driver, By.XPATH, self.lnk_authorizationIcon).click()
            default_wait(self.driver, By.XPATH, self.lnk_arrow).click()
            default_wait(self.driver, By.XPATH, self.lnk_AddAuthorization_btm).click()
            sleep(10)
            default_wait(self.driver, By.XPATH, self.lnk_search_client_btm).click()
        except (TimeoutException, ElementNotInteractableException, NoSuchElementException) as e:
            exc_type, exc_value, exc_tb = traceback.sys.exc_info()  # Get exception information
            lineno = exc_tb.tb_lineno  # Get the line number
            exception_details = f"An error occurred: {e}. Line number: {lineno}."
            traceback_str = traceback.format_exc()  # Full stack trace for more context
            logger.error(exception_details)
            logger.error(traceback_str)  # Optional: log the full traceback for detailed context

    def Add_Auth_details(self, test_file):
        try:
            logger.info(f'Starting Add_Auth_details {test_file}')
            default_wait(self.driver, By.XPATH, self.lnk_enter_client_name).send_keys(
                test_file['ClientName'] + Keys.RETURN)
            sleep(5)
            client_name_elements = default_wait(self.driver, By.XPATH, self.select_client_name)
            if client_name_elements is None:
                client_name_elements = []
            elif not isinstance(client_name_elements, list):
                client_name_elements = [client_name_elements]
            for element in client_name_elements:
                name = element.text
                name_parts = name.split("\n")
                cleaned_name = name_parts[0]
                if cleaned_name == test_file['ClientName']:
                    self.driver.execute_script("arguments[0].scrollIntoView();", element)
                    element.click()
                    break
            else:
                logger.warning(f"No client name matching '{test_file['ClientName']}' found")
                return
            sleep(5)
            default_wait(self.driver, By.XPATH, self.AuthorizationNo).send_keys(test_file['AuthorizationNo'])
            # Convert and input dates
            received_date = _convert_date(test_file['ReceivedDate'])
            start_date = _convert_date(test_file['StartDate'])
            end_date = _convert_date(test_file['EndDate'])
            default_wait(self.driver, By.XPATH, self.AuthReceivedDate).send_keys(received_date)
            default_wait(self.driver, By.XPATH, self.AuthStartDate).send_keys(start_date)
            default_wait(self.driver, By.XPATH, self.AuthEndDate).send_keys(end_date)
            default_wait(self.driver, By.XPATH, self.orderAllocations).send_keys(test_file['OrderAllocations'])
            default_wait(self.driver, By.XPATH, self.NPINo).send_keys(test_file['NPINumber'])
            default_wait(self.driver, By.XPATH, self.discipline).send_keys(test_file['Discipline'])
            default_wait(self.driver, By.XPATH, self.authorizedquantity).send_keys(test_file['Authorized'])
            default_wait(self.driver, By.XPATH, self.unitofmeasure).send_keys(test_file['UnitOfMeasure'])
            default_wait(self.driver, By.XPATH, self.utilisationrule).send_keys(test_file['UtilisationRule'])
            sleep(5)
        except Exception as e:
            logger.error(f"Exception during Add_Auth_details: {str(e)}")
            logger.error(traceback.format_exc())  # Log full traceback for detailed context
            print(f"An error occurred: {e}")
            capture_and_save_screenshot("Error_Occured_Add_Auth_details")

        finally:
            self.utils.close_browser()