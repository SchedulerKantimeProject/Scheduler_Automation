import os
import pytest
from PageObjects.ClinicianCalendarPage import ClinicianPage
from PageObjects.LoginPage import Login
from PageObjects.ManualOptimizeRoute import ManualOptimizeRoute
from Utilities.generalUtils import get_excel_test_data
from conftest import setup_class,login


@pytest.mark.usefixtures("setup_class")
class TestClinicianCalendar_ManualOptimize_OptimizeRoute:
    @pytest.fixture(scope="function")
    def get_test_data(self):
        # excel_file_path = os.path.abspath(os.path.join(os.curdir,'..', '..',  'TestData', 'SchedulerData.xlsx'))
        # Get the absolute path to the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the Excel file
        relative_path = os.path.join(script_dir, '..', '..', 'TestData', 'SchedulerData.xlsx')
        # Normalize the path
        excel_file_path = os.path.normpath(relative_path)
        # Print the absolute path for debugging purposes
        print("Absolute path to Excel file:", excel_file_path)
        return get_excel_test_data(excel_file_path, 'OptimizeRoute', 'CL_01')

    @pytest.mark.usefixtures("login")
    def test_login(self):
        # The login fixture already handles the login process
        self.logger.info("Login test completed successfully.")

    @pytest.mark.usefixtures("get_test_data")
    def test_OptimizeRoutePage_optimize_page(self, get_test_data):
        self.logger.info("*** Clinician Page start ***")
        driver = self.utils.get_driver()
        ClinicianPage(driver).clinician_page()
        ManualOptimizeRoute(driver).Clinicain_calendar_week(get_test_data)
        ManualOptimizeRoute(driver).OptimizeRoutePage_optimize()
