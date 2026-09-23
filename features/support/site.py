"""Page helpers shared by every step module.

The site under test is a single animated page, and three of its behaviours will
break naive Selenium code. All three are absorbed here so the step definitions
stay readable:

* AOS reveals elements on scroll, so anything below the fold reports
  ``is_displayed() == False`` and an empty ``.text`` until scrolled to.
* ``scroll-behavior: smooth`` means a nav click starts an animation that
  outlives the click, and scrollspy only marks the active menu item once it
  lands.
* Several elements are uppercased by CSS, so ``.text`` disagrees with the
  markup. Reading ``textContent`` gives the source text.
"""

import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 15

TITLE = "Mark Custard - QA & Automation Engineering Lead"

SECTIONS = (
    "hero",
    "about",
    "resume",
    "portfolio",
    "technical-skills",
    "skills",
    "testimonials",
    "contact",
)


class Site:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url.rstrip("/") + "/"

    # ----------------------------------------------------------------- loading
    def open(self):
        self.driver.get(self.base_url)
        self.wait_present((By.CSS_SELECTOR, "#portfolio .portfolio-item"))
        return self

    # ----------------------------------------------------------------- waiting
    def _wait(self, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(
            self.driver,
            timeout,
            ignored_exceptions=(StaleElementReferenceException,),
        )

    def wait_present(self, locator, timeout=DEFAULT_TIMEOUT):
        return self._wait(timeout).until(EC.presence_of_element_located(locator))

    def wait_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_until(self, predicate, timeout=DEFAULT_TIMEOUT, message=""):
        return self._wait(timeout).until(lambda _: predicate(), message)

    def wait_for_scroll_to_settle(self, timeout=DEFAULT_TIMEOUT):
        last, stable = None, 0
        deadline = time.time() + timeout
        while time.time() < deadline:
            current = self.driver.execute_script("return window.scrollY;")
            stable = stable + 1 if current == last else 0
            if stable >= 2:
                return current
            last = current
            time.sleep(0.1)
        return last

    # ---------------------------------------------------------------- querying
    def find(self, locator):
        return self.driver.find_element(*locator)

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def text_of(self, target):
        element = target if isinstance(target, WebElement) else self.find(target)
        return self.driver.execute_script(
            "return arguments[0].textContent.trim();", element
        )

    # --------------------------------------------------------------- revealing
    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
            element,
        )
        return element

    def reveal(self, locator, timeout=DEFAULT_TIMEOUT):
        elements = self.find_all(locator)
        if not elements:
            raise AssertionError(f"No elements matched {locator}")
        for element in elements:
            self.scroll_into_view(element)
        self._wait(timeout).until(
            lambda _: all(e.is_displayed() for e in self.find_all(locator)),
            f"Elements matching {locator} never became visible",
        )
        return self.find_all(locator)

    def reveal_one(self, locator, timeout=DEFAULT_TIMEOUT):
        self.scroll_into_view(self.wait_present(locator, timeout))
        return self.wait_visible(locator, timeout)

    # ---------------------------------------------------------------- actions
    def js_click(self, element):
        self.scroll_into_view(element)
        self.driver.execute_script("arguments[0].click();", element)

    # -------------------------------------------------------------- navigation
    def go_to_section(self, section):
        self.js_click(self.find((By.CSS_SELECTOR, f"#navmenu a[href='#{section}']")))
        self.wait_visible((By.ID, section))
        self.wait_for_scroll_to_settle()
        return self

    def section(self, section):
        return self.reveal_one((By.ID, section))

    def section_heading(self, section):
        return self.text_of((By.CSS_SELECTOR, f"#{section} .section-title h2"))

    def active_nav_section(self):
        link = self.wait_visible((By.CSS_SELECTOR, "#navmenu ul li a.active"))
        return link.get_attribute("href").split("#")[-1]

    def menu_entries(self):
        return [
            {
                "section": link.get_attribute("href").split("#")[-1],
                "label": self.text_of(link),
            }
            for link in self.reveal((By.CSS_SELECTOR, "#navmenu ul li a"))
        ]

    # ------------------------------------------------------------------ content
    def about_facts(self):
        return self.driver.execute_script(
            """
            const out = {};
            document.querySelectorAll('#about .content ul li').forEach(li => {
              const k = li.querySelector('strong'), v = li.querySelector('span');
              if (k && v) out[k.textContent.trim().replace(/:$/, '')] = v.textContent.trim();
            });
            return out;
            """
        )

    def resume_headings(self):
        return self.driver.execute_script(
            "return Array.from(document.querySelectorAll('#resume .resume-item h4'))"
            ".map(e => e.textContent.trim());"
        )

    def resume_download_link(self):
        return self.reveal_one((By.CSS_SELECTOR, "#resume a.btn-download-resume"))

    def portfolio_cards(self):
        """Returned as an array: ChromeDriver alphabetises the keys of any
        object handed back from execute_script, which would lose card order."""
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#portfolio .portfolio-item')).map(i => ({
              title: i.querySelector('.portfolio-card-header h4').textContent.trim(),
              tags: Array.from(i.querySelectorAll('.portfolio-tags .tag')).map(t => t.textContent.trim()),
              url: i.querySelector('a.github-link').href,
              target: i.querySelector('a.github-link').target,
              rel: i.querySelector('a.github-link').rel,
            }));
            """
        )

    def visible_portfolio_titles(self):
        return [
            self.text_of(card.find_element(By.TAG_NAME, "h4"))
            for card in self.find_all((By.CSS_SELECTOR, "#portfolio .portfolio-card"))
            if card.is_displayed()
        ]

    def open_portfolio(self):
        self.go_to_section("portfolio")
        self.reveal((By.CSS_SELECTOR, "#portfolio .portfolio-filters li"))
        self.reveal((By.CSS_SELECTOR, "#portfolio .portfolio-item"))
        return self

    def filter_portfolio(self, label, expected_count):
        chips = self.reveal((By.CSS_SELECTOR, "#portfolio .portfolio-filters li"))
        chip = next(c for c in chips if self.text_of(c) == label)
        self.js_click(chip)
        self.wait_until(
            lambda: len(self.visible_portfolio_titles()) == expected_count,
            message=(
                f"Filter {label!r} settled on "
                f"{len(self.visible_portfolio_titles())} cards, expected {expected_count}"
            ),
        )
        return self

    def active_filter_label(self):
        return self.text_of(
            self.find((By.CSS_SELECTOR, "#portfolio .portfolio-filters li.filter-active"))
        )

    def technical_skill_groups(self):
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#technical-skills .service-item')).map(i => ({
              title: i.querySelector('h4.title').textContent.trim(),
              description: i.querySelector('p.description').textContent.trim(),
            }));
            """
        )

    def skills(self):
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#skills .progress')).map(r => ({
              name: r.querySelector('.skill > span').textContent.trim(),
              label: r.querySelector('.skill .val').textContent.trim(),
              value: Number(r.querySelector('.progress-bar').getAttribute('aria-valuenow')),
            }));
            """
        )

    def testimonials(self):
        """Read via textContent: Swiper only renders the active slides."""
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#testimonials .testimonial-item')).map(t => ({
              name: t.querySelector('h3').textContent.trim(),
              role: t.querySelector('h4').textContent.trim(),
              linkedin: t.querySelector('h3 a') ? t.querySelector('h3 a').href : null,
              quote: t.querySelector('p').textContent.trim(),
            }));
            """
        )

    def active_testimonial_name(self):
        return self.text_of(
            (By.CSS_SELECTOR, "#testimonials .swiper-slide-active .testimonial-item h3")
        )

    def testimonial_bullets(self):
        return self.find_all(
            (By.CSS_SELECTOR, "#testimonials .swiper-pagination-bullet")
        )

    def contact_info(self):
        return self.driver.execute_script(
            """
            return Array.from(document.querySelectorAll('#contact .info-item')).map(i => ({
              heading: i.querySelector('h3').textContent.trim(),
              lines: Array.from(i.querySelectorAll('p')).map(p => p.textContent.trim()),
            }));
            """
        )

    def form_is_valid(self):
        """Ask the browser, without posting anything to the live endpoint."""
        return self.driver.execute_script(
            "return document.querySelector('#contact form').checkValidity();"
        )
