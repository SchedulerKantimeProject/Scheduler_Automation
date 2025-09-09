from datetime import datetime
import pytest
import os
from PageObjects.LoginPage import Login
from Utilities.customLogger import LogGen
from Utilities.generalUtils import GeneralUtils, read_ini_config
# This class will helpful to avoid everytime call for text case run
# the class will store the initial all setup call and every test case run time it will helpful to reduce the usage
"""explaination of using class here 
 If you don’t use a class fixture → every function-scoped fixture runs fresh for each test case, re-initializing all objects again and again (driver, utils, config, etc.).
 If you use a class fixture → those heavy objects are created only once per test class, kept in memory, and all test functions inside that class reuse them."""
@pytest.fixture(scope="class")
def setup_class(request):
    utils = GeneralUtils()  #No driver passed; initialized internally
    logger = LogGen.loggen()
    config_data = read_ini_config()

    request.cls.utils = utils
    request.cls.logger = logger
    request.cls.config_data = config_data


@pytest.fixture(scope="function")
def login(request):
    logger = request.cls.logger
    utils = request.cls.utils
    config_data = request.cls.config_data
    base_url = config_data.get("baseurl", "")
    utils.open_in_browser(base_url)
    driver = utils.get_driver()
    Login(driver).enter_usernamepassword(
        config_data.get('email', ""), config_data.get('password', "")
    )
    logger.info("Login successful")

def pytest_metadata(config, metadata):
    metadata['Project Name'] = 'SCHProject'
    metadata['Module Name'] = 'SchedulerTest'
    metadata['Tester'] = 'Pavithran'


@pytest.hookimpl(optionalhook=True)
def pytest_configure(config):
    config.option.htmlpath = os.path.abspath(os.curdir) + "\\reports\\" + datetime.now().strftime("%d-%m-%Y %H-%M-%S") + ".html"
