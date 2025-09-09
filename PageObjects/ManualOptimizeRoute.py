import traceback
from datetime import datetime, timedelta

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
from Utilities.customLogger import LogGen
from Utilities.generalUtils import GeneralUtils, default_wait, sleep, capture_and_save_screenshot, default_wait_for_both
from Utilities.generalUtils import _convert_date


class ManualOptimizeRoute:
    send_caregiver_name = "//div[text() ='Search Clinician Name/ID']/ancestor::*[3]/div[1]/div/div[2]/input"
    visit_confirm = "(//button[text()=' Confirm visit(s) ' or text()=' Route Optimized '])"
    select_caregiver_name = "//div[@class ='ng-dropdown-panel-items scroll-host']/div/div"
    search_icon = "//img[@class='me-1 cursor-pointer']"
    btm_optimize = "//button[text()=' Cancel ']/../button[text()=' Optimize Route ']"
    optimized_msg = "//div[text()=' Successfully optimized ! ' or text()=' Failed to optimize ! ']"
    drag = "//div[@cdkdragboundary = '.drag-boundary']"
    drop = "//div[@class='d-flex align-items-center cursor-default']"
    RecomputeContinue_Yes = "//button[@class='swal2-confirm swal2-styled']"
    btm_Reoptimize = "//button[text()=' Re-Compute ']"
    Reoptimized_msg = "//div[text()=' Successfully Re-computed ! ' or text()=' Failed to Re-computed ! ']"
    before_drag_start_time = "(//div[@cdkdragboundary = '.drag-boundary']/div[2]/div/span/span[1])"
    before_drag_end_time = "(//div[@cdkdragboundary = '.drag-boundary']/div[2]/div/span/span[2])"
    first_visit_button = "//input[@id= 'first_visit_radio']"
    first_visit_time = "//input[@id='first_visit_radio']/following::input[@type='text'][1]"
    # Optimize_pop_load_check = "//p[text()=' Start My Day ']"

    def __init__(self, driver):
        self.driver = driver
        self.logger = LogGen.loggen()
        self.utils = GeneralUtils(driver)

    def visit_date_select(self, date):
        return f"//span[text()='({date}) ']/../preceding-sibling::div"

    def get_text_values(self, xpath_expression):
        elements = self.driver.find_elements(By.XPATH, xpath_expression)
        return [element.text for element in elements]

    def Clinicain_calendar_week(self, test_file):
            self.logger.info(f'Starting optimization and recomputation for {test_file}')
            default_wait(self.driver, By.XPATH, self.send_caregiver_name).send_keys(
                test_file['ClinicianName'] + Keys.RETURN)
            sleep(5)
            caregiver_name_elements = default_wait(self.driver, By.XPATH, self.select_caregiver_name)
            if caregiver_name_elements is None:
                caregiver_name_elements = []
            elif not isinstance(caregiver_name_elements, list):
                caregiver_name_elements = [caregiver_name_elements]
            for element in caregiver_name_elements:
                name = element.text
                name_parts = name.split("\n")
                cleaned_name = name_parts[0]
                if cleaned_name == test_file['ClinicianName']:
                    self.driver.execute_script("arguments[0].scrollIntoView();", element)
                    element.click()
                    break
            else:
                self.logger.warning(f"No caregiver name matching '{test_file['ClinicianName']}' found")
                return

            default_wait(self.driver, By.XPATH, self.search_icon).click()
            default_wait(self.driver, By.XPATH, self.visit_confirm, EC.presence_of_all_elements_located, multiple=True)
            current_date = datetime.now().strftime("%Y-%m-%d")
            # formatted_date = _convert_date(test_file['Date'])
            # tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            # yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

            formatted_date = _convert_date(current_date)
            self.logger.info(f"formatted_date: {formatted_date}")
            index = default_wait_for_both(self.driver, By.XPATH, self.visit_date_select(formatted_date))
            if index is None:
                index = []
            elif not isinstance(index, list):
                index = [index]

            if index is not None:
                current_index = len(index) + 1
                if current_index > 1:
                    compare_current_index = self.visit_confirm + f"[{current_index}]"
                    self.logger.info(f"Current index: {compare_current_index}")
                    default_wait(self.driver, By.XPATH, compare_current_index, EC.element_to_be_clickable).click()

                else:
                    compare_current_index = self.visit_confirm + "[1]"
                    self.logger.info(f"Current index: {compare_current_index}")
                    default_wait(self.driver, By.XPATH, compare_current_index, EC.element_to_be_clickable).click()

            new_window_handle = self.driver.window_handles[-1]
            self.driver.switch_to.window(new_window_handle)

    def OptimizeRoutePage_optimize(self):
        try:
            try:
                # default_wait(self.driver, By.XPATH, self.Optimize_pop_load_check, EC.presence_of_element_located)
                default_wait(self.driver, By.XPATH, self.btm_optimize, EC.presence_of_element_located).click()
                # after_msg_optimized = WebDriverWait(self.driver, 50).until(
                #     EC.visibility_of_element_located((By.XPATH, self.optimized_msg)))
                after_msg_optimized = default_wait(self.driver, By.XPATH, self.optimized_msg,
                                                   EC.visibility_of_element_located)
                msg_after_optimized = after_msg_optimized.text.strip()
                if 'Successfully optimized !' in msg_after_optimized:
                    self.logger.info("Successfully Optimized")
                    # Get the before drag start time values
                    before_drag_start_time_values = self.get_text_values(f"({self.before_drag_start_time})[1]")
                    self.logger.info(f"Before drag start time values: {before_drag_start_time_values}")
                    before_drag_end_time_values = self.get_text_values(f"({self.before_drag_end_time})[1]")
                    self.logger.info(f"Before drag end time values: {before_drag_end_time_values}")
                elif 'Failed to optimize !' in msg_after_optimized:
                    self.logger.error("Failed to optimize")
                    capture_and_save_screenshot("Failed to optimize")
            except Exception as e:
                self.logger.error(f"Exception during optimization: {str(e)}")
                capture_and_save_screenshot("Exception during optimization")

        finally:
            self.utils.close_browser()

    def OptimizeRoutePage_optimize_and_recompute(self):
        try:
            try:
                # default_wait(self.driver, By.XPATH, self.Optimize_pop_load_check, EC.presence_of_element_located)
                default_wait(self.driver, By.XPATH, self.btm_optimize, EC.presence_of_element_located).click()
                # after_msg_optimized = WebDriverWait(self.driver, 50).until(
                #     EC.visibility_of_element_located((By.XPATH, self.optimized_msg)))
                after_msg_optimized = default_wait(self.driver, By.XPATH, self.optimized_msg, EC.visibility_of_element_located)
                self.logger.info(f"after_msg_optimized: {after_msg_optimized}")
                msg_after_optimized = after_msg_optimized.text.strip()
                if 'Successfully optimized !' in msg_after_optimized:
                    self.logger.info("Successfully Optimized")
                    # Get the before drag start time values
                    before_drag_start_time_values = self.get_text_values(f"({self.before_drag_start_time})[1]")
                    self.logger.info(f"Before drag start time values: {before_drag_start_time_values}")
                    before_drag_end_time_values = self.get_text_values(f"({self.before_drag_end_time})[1]")
                    self.logger.info(f"Before drag end time values: {before_drag_end_time_values}")
                elif 'Failed to optimize !' in msg_after_optimized:
                    self.logger.error("Failed to optimize")
                    capture_and_save_screenshot("Failed to optimize")

                # Perform drag and drop operation
                index = default_wait_for_both(self.driver, By.XPATH, self.drag)
                if index is None:
                    index = []
                elif not isinstance(index, list):
                    index = [index]

                if len(index) >= 2:
                    target_xpath = f"({self.drop})[2]"
                    source_xpath = f"({self.drag})[1]"
                    source_element = default_wait(self.driver, By.XPATH, source_xpath)
                    target_element = default_wait(self.driver, By.XPATH, target_xpath)
                    action_chains = ActionChains(self.driver)
                    sleep(20)
                    action_chains.click_and_hold(source_element).move_to_element(target_element).release(
                        target_element).perform()
                    default_wait(self.driver, By.XPATH, self.btm_Reoptimize).click()
                    # after_msg_Reoptimized = WebDriverWait(self.driver, 50).until(
                    #     EC.visibility_of_element_located((By.XPATH, self.Reoptimized_msg)))
                    after_msg_Reoptimized = default_wait(self.driver, By.XPATH, self.Reoptimized_msg, EC.visibility_of_element_located)
                    after_drag_start_time_values = self.get_text_values(f"({self.before_drag_start_time}[2])")
                    self.logger.info(f"After drag start time values: {after_drag_start_time_values}")
                    after_drag_end_time_values = self.get_text_values(f"({self.before_drag_end_time}[2])")
                    self.logger.info(f"After drag end time values: {after_drag_end_time_values}")
                    if before_drag_start_time_values != after_drag_start_time_values and before_drag_start_time_values != before_drag_end_time_values:
                        self.logger.info("Re-compute is done correctly")
                        capture_and_save_screenshot("Re-compute is done correctly")
                    else:
                        self.logger.info("Re-compute is failed")
                    msg_after_reoptimized = after_msg_Reoptimized.text.strip()
                    if 'Successfully Re-computed !' in msg_after_reoptimized:
                        self.logger.info("Successfully Re-computed")
                        capture_and_save_screenshot("Re-compute is done correctly")
                    elif 'Failed to Re-computed !' in msg_after_reoptimized:
                        self.logger.error("Failed to Re-compute")
                        capture_and_save_screenshot("Failed to Re-compute")
                else:
                    self.logger.error("Drag and drop operation failed, Because if more than two schedules are there then only drag and drop able to do")
                    return

            except (TimeoutException, ElementNotInteractableException, NoSuchElementException) as e:
                self.logger.error(f"An error occurred: {str(e)}")
                self.logger.error(traceback.format_exc())  # Log full traceback for detailed context
                print(f"An error occurred: {e}")
                capture_and_save_screenshot("Error_Caused_by_ManualOptimizeRoute")

        finally:
            self.utils.close_browser()

    def OptimizeRoute_Prefer_Visit_RoutePreference_VisitClient(self, test_file):
        try:
            self.logger.info("Preference Verification")
            default_wait(self.driver, By.XPATH, self.first_visit_button, EC.presence_of_element_located).click()
            self.logger.info(f"test need to print : {test_file['FirstVisitTime']}")
            self.logger.info(f"test need to print : {test_file['FirstVisitTime'].strftime("%I:%M %p")}")
            default_wait(self.driver, By.XPATH, self.first_visit_time, EC.presence_of_element_located).send_keys(test_file['FirstVisitTime'].strftime("%I:%M %p"))
            sleep(10)


        finally:
            self.utils.close_browser()
