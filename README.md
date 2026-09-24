# BDD Portfolio Tests (Behave + Selenium)

Behaviour-driven tests for [markcustard.com](https://markcustard.com/) — my
portfolio site — written in Gherkin and executed with Behave and Selenium
WebDriver.

**8 features, 91 scenarios, 307 steps.**

| Feature | Covers |
| --- | --- |
| `navigation.feature` | Title, menu contents and order, scrollspy highlighting, section headings, hero, footer |
| `about.feature` | Headline and the eight-item fact list |
| `resume.feature` | Every role and qualification, plus a real PDF download |
| `portfolio.feature` | Project cards, tags, repository links, Isotope filtering, keyboard-operable filters |
| `skills.feature` | The ten technical skill groups and the seven skill percentages |
| `testimonials.feature` | All five testimonials, profile links, carousel pagination |
| `contact.feature` | Contact blocks and form validation |
| `responsive.feature` | Off-canvas sidebar, toggle state, aria-expanded, horizontal overflow |

## The contact form is never submitted

The form posts to a live Formspree endpoint, so submitting it with valid data
would deliver a real email on every run. Validation is asserted by asking the
browser via `checkValidity()`, or by submitting the form **empty** so
browser-side validation blocks the request. The "well-formed enquiry" scenario
confirms a good entry *would* pass, and stops there.

## Why the step definitions look the way they do

The site is a single page on an animated Bootstrap template. Four of its
behaviours break naive Selenium code, and all four are absorbed in
[`features/support/site.py`](features/support/site.py) so the steps stay
readable:

| Behaviour | How it's handled |
| --- | --- |
| **AOS reveal animations** — elements exist in the DOM but report `is_displayed() == False` and empty `.text` until scrolled to | `Site.reveal()` scrolls each match into view and waits for it to render |
| **`scroll-behavior: smooth`** — a nav click starts an animation that outlives the click, and scrollspy only sets the active item once it lands | `Site.wait_for_scroll_to_settle()` polls `window.scrollY` until it stops changing |
| **`text-transform: uppercase`** — `.text` returns `"AUTOMATION"` where the markup says `"Automation"` | `Site.text_of()` reads `textContent` instead |
| **Swiper carousel** — only active slides are rendered, so off-screen testimonials come back blank | Testimonials are read via `textContent` for all five |

One more trap worth naming: **ChromeDriver returns JS objects with their keys
alphabetised**, which silently destroys document order. Anything order-sensitive
returns an array, never an object.

## Driver lifecycle lives in `environment.py`

The browser is created once in `before_all` and the page is reloaded in
`before_scenario`. Step definitions never touch driver lifecycle — a step that
calls `driver.quit()` leaves every later step in that scenario with nothing to
talk to, and leaks the process whenever a scenario fails or is skipped.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

No driver binaries needed: Selenium Manager (built into Selenium 4.6+) resolves
chromedriver and geckodriver automatically.

## Running

```bash
behave                                       # Chrome, visible
behave -D headless=true                      # Chrome, headless
behave -D browser=firefox -D headless=true   # Firefox
behave --tags=@smoke                         # the quick pass
behave --tags=@mobile                        # mobile viewport only
behave --tags=~@download                     # skip the file-download scenario
behave -D base_url=http://localhost:8000/    # a local copy
behave features/portfolio.feature            # one feature
```

| Setting | Default | Purpose |
| --- | --- | --- |
| `-D browser` | `chrome` | `chrome`, `firefox` or `safari` |
| `-D headless` | `false` | Ignored for Safari, which has no headless mode |
| `-D base_url` | `https://markcustard.com/` | Point the suite at a local or staging copy |

Defaults also live in [`behave.ini`](behave.ini). A full Chrome run takes about
100 seconds.

## Tags

| Tag | Meaning |
| --- | --- |
| `@smoke` | 15 scenarios worth running on every deploy (~20s) |
| `@mobile` | Resized to 390×844 by `before_scenario`, restored afterwards |
| `@download` | Writes a real PDF to a temporary directory |

## Layout

```
behave.ini                          default browser, headless and base_url
features/environment.py             driver lifecycle, viewport, download dir
features/support/site.py            waits, reveal helpers, section accessors
features/*.feature                  the scenarios
features/steps/*_steps.py           step definitions, grouped by section
```

## CI

[`.github/workflows/tests.yml`](.github/workflows/tests.yml) runs every scenario
against Chrome and Firefox on push, pull request and nightly at 07:30 UTC — the
suite tests the deployed site, so a scheduled run catches content drift even
when this repository hasn't changed. JUnit results are uploaded per browser.

## License

[MIT](LICENSE)
