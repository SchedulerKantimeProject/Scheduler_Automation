# import os
# import pytest
# from PageObjects.AuthorizationPage import AuthorizationPage
# from Utilities.generalUtils import get_excel_test_data
# from conftest import setup_class,login
#
# @pytest.mark.usefixtures("setup_class")
# class TestSaveAuthNoLimitWithout_UtilizationLimt:
#     @pytest.fixture(scope="function")
#     def get_test_data(self):
#         # excel_file_path = os.path.abspath(os.path.join(os.curdir,'..', '..',  'TestData', 'SchedulerData.xlsx'))
#         # Get the absolute path to the directory where this script is located
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         # Construct the full path to the Excel file
#         relative_path = os.path.join(script_dir, '..', '..', 'TestData', 'SchedulerData.xlsx')
#         # Normalize the path
#         excel_file_path = os.path.normpath(relative_path)
#         # Print the absolute path for debugging purposes
#         print("Absolute path to Excel file:", excel_file_path)
#         return get_excel_test_data(excel_file_path, 'Authorization', 'CL_01')
#
#     @pytest.mark.usefixtures("login")
#     def test_login(self):
#         # The login fixture already handles the login process
#         self.logger.info("Login test completed successfully.")
#
#     @pytest.mark.usefixtures("get_test_data")
#     def test_TestSaveAuthNoLimitWithout_UtilizationLimt_page(self, get_test_data):
#         self.logger.info("*** Clinician Page start ***")
#         driver = self.utils.get_driver()
#         auth_page = AuthorizationPage(driver)
#         auth_page.Authorization_Page()
#         auth_page.Add_Auth_details(get_test_data)
