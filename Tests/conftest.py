from datetime import datetime

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from Config.config import TestData
from Pages.AudiencePage import Audience
from Pages.Campaign import Campaign
from Pages.DashboardPage import Dashboard
from Pages.LoginPage import Login
from Pages.Recordings import Recording
from Tests.test_base import BaseTest
from py.xml import html

# driver = webdriver.Chrome(ChromeDriverManager().install())


@pytest.fixture(params=["chrome"], scope="class")
def driver_init(request):
    # if request.param == "chrome":
    #     driver = webdriver.Chrome(ChromeDriverManager().install())
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # if request.param == "edge":
    #     driver = webdriver.Edge(executable_path= GeckoDriverManager().install())
    # if request.param == "chrome":
    #     driver = webdriver.Chrome(executable_path= TestData.DRIVER_PATH)
    # if request.param == "edge":
    #     driver = webdriver.Edge(executable_path = TestData.EDGE_PATH)
    request.cls.driver = driver
    yield
    driver.close()


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)

    
 
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        # if (report.failed and xfail) or (report.failed and not xfail):
        print(report.nodeid)
        file_name = report.nodeid.replace("::", "_") + ".png"
        _capture_screenshot(file_name)
        if file_name:
            html = '<div><img src="%s" alt="screenshot" style="width:204px;height:128px;" ' \
                   'onclick="window.open(this.src)" align="right"/></div>' % file_name
            extra.append(pytest_html.extras.html(html))
        report.extra = extra
 

# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     """
#     Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
#     :param item:
#     """
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])

#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             file_name = report.nodeid.replace("::", "_") + ".png"
#             _capture_screenshot(file_name)
#             if file_name:
#                 html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % file_name
#                 extra.append(pytest_html.extras.html(html))
#         report.extra = extra


class Test_BasicTest(BaseTest):
    # @pytest.fixture(autouse=True)
    def setup(self):
        self.login_page = Login(self.driver)
        self.dashboard_page = Dashboard(self.driver)
        self.audience_page = Audience(self.driver)
        self.campaign_page = Campaign(self.driver)
        self.recording_page = Recording(self.driver)


def pytest_html_report_title(report):
    report.title = "VODEX UI"


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    ''' modifying the summary in pytest environment'''

    # prefix.extend([html.h1("Auto Selecting Trip.")])
    summary.extend([html.h3("VODEX UI TESTING USING PYTEST FRAMEWORK")])
    # postfix.extend([html.h3("")])


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    del cells[4]


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    custom_description = getattr(report, "custom_description", "")
    cells.insert(2, html.td(custom_description))


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    ''' modifying the summary in pytest environment'''
    from py.xml import html
    prefix.extend([html.h3("Adding prefix message")])
    summary.extend([html.h3("Adding summary message")])
    postfix.extend([html.h3("Adding postfix message")])

# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     """
#     Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
#     :param item:
#     """
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])

#     if report.when == 'call' or report.when == "setup":
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             file_name = report.nodeid.replace("::", "_") + ".png"
#             _capture_screenshot(file_name)
#             if file_name:
#                 html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
#                        'onclick="window.open(this.src)" align="right"/></div>' % file_name
#                 extra.append(pytest_html.extras.html(html))
#         report.extra = extra


# def _capture_screenshot(name):
#     driver.get_screenshot_as_file(name)



# def pytest_html_report_title(report):
#     ''' modifying the title  of html report'''
#     report.title = "Custom Ti"

# @pytest.mark.optionalhook
# def pytest_html_results_summary(prefix, summary, postfix):
#     ''' modifying the summary in pytest environment'''
#     from py.xml import html
#     prefix.extend([html.h3("Adding prefix message")])
#     summary.extend([html.h3("Adding summary message")])
#     postfix.extend([html.h3("Adding postfix message")])

