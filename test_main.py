# Updated version of test_main.py

import os
import shutil
import subprocess
import concurrent.futures
import time
from Utilities.customLogger import LogGen
from Utilities.generalUtils import sleep, delete_old_screenshots

logger = LogGen.loggen()

def run_test(test_path):
    try:
        logger.info(f"Running: {test_path}")
        if not os.path.exists(test_path):
            logger.error(f"Test path does not exist: {test_path}")
            return

        result = subprocess.run(
            ['pytest', test_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            logger.info(f"Test passed: {test_path}")
        else:
            logger.error(f"Test failed: {test_path}")
            logger.error(result.stderr)

    except Exception as e:
        logger.error(f"Exception running test {test_path}: {e}")

def clear_old_reports():
    reports_dir = os.path.join(os.getcwd(), "reports")
    if os.path.exists(reports_dir):
        shutil.rmtree(reports_dir)
    os.makedirs(reports_dir)

def kill_stray_browsers():
    import platform
    import subprocess

    if platform.system() == "Windows":
        # Kill Edge and WebDriver processes
        subprocess.call("taskkill /f /im msedge.exe", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call("taskkill /f /im msedgedriver.exe", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def test_main():
    try:
        print("Starting test execution...")
        LogGen.clear_old_logs()
        clear_old_reports()
        delete_old_screenshots()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        test_paths = [
            os.path.join(base_dir, 'TestCases', 'CliniciansPage', 'test_001_ClinicianCalender_ManualOptimize_OptimizeRoute_RecomputeRoute.py'),
            os.path.join(base_dir, 'TestCases', 'CliniciansPage', 'test_002_ClinicianCalender_ManualOptimize_OptimzeRoute.py'),
            os.path.join(base_dir, 'TestCases', 'CliniciansPage',
                         'test_002_ClinicianCalender_ManualOptimize_OptimzeRoute.py'),
            os.path.join(base_dir, 'TestCases', 'AddAuth', 'test_003_ClinicianCalendar_ManualOptimize_PreferenceCheck.py')
        ]

        logger.info(f"Tests to execute: {test_paths}")

        with concurrent.futures.ProcessPoolExecutor(max_workers=len(test_paths)) as executor:
            futures = [executor.submit(run_test, test_path) for test_path in test_paths]
            concurrent.futures.wait(futures)

        print("All tests completed.")

    except Exception as e:
        logger.error(f"Exception in test_main: {e}")
    finally:
        sleep(3)
        kill_stray_browsers()
        LogGen.close_logger()

if __name__ == "__main__":
    test_main()
