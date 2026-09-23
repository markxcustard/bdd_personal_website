"""Behave hooks.

The browser is created once per run and the page is reloaded before each
scenario. Driver lifecycle belongs here, not in step definitions: a step that
quits the driver leaves every later step in that scenario with nothing to talk
to, and skipped or failing scenarios leak the process.
"""

import os
import shutil
import sys
import tempfile

from selenium import webdriver

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from support.site import Site  # noqa: E402  (needs the path above)

DEFAULT_BASE_URL = "https://markcustard.com/"
DESKTOP = (1600, 1000)  # wide enough for the sidebar nav to be expanded
MOBILE = (390, 844)


def _flag(context, name, default="false"):
    return str(context.config.userdata.get(name, default)).lower() in {
        "1",
        "true",
        "yes",
    }


def _chrome(headless, download_dir):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
        },
    )
    return webdriver.Chrome(options=options)


def _firefox(headless, download_dir):
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    options.set_preference("pdfjs.disabled", True)
    return webdriver.Firefox(options=options)


def _safari(_headless, _download_dir):
    return webdriver.Safari()


BUILDERS = {"chrome": _chrome, "firefox": _firefox, "safari": _safari}


def before_all(context):
    browser = context.config.userdata.get("browser", "chrome").lower()
    if browser not in BUILDERS:
        raise ValueError(
            f"Unsupported browser {browser!r}; choose from {sorted(BUILDERS)}"
        )

    context.base_url = context.config.userdata.get("base_url", DEFAULT_BASE_URL)
    context.browser_name = browser
    # Downloads land in a temporary directory so a test run never writes into
    # the developer's own ~/Downloads.
    context.download_dir = tempfile.mkdtemp(prefix="portfolio-downloads-")

    context.driver = BUILDERS[browser](_flag(context, "headless"), context.download_dir)
    context.driver.set_window_size(*DESKTOP)
    context.driver.implicitly_wait(0)  # explicit waits only


def before_scenario(context, scenario):
    if "mobile" in scenario.effective_tags:
        context.driver.set_window_size(*MOBILE)
    context.site = Site(context.driver, context.base_url).open()


def after_scenario(context, scenario):
    if "mobile" in scenario.effective_tags:
        context.driver.set_window_size(*DESKTOP)


def after_all(context):
    driver = getattr(context, "driver", None)
    if driver is not None:
        driver.quit()
    shutil.rmtree(getattr(context, "download_dir", ""), ignore_errors=True)
