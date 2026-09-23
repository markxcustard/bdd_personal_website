"""Mobile layout steps. Scenarios tagged @mobile are resized in before_scenario."""

from behave import then, when
from selenium.webdriver.common.by import By

TOGGLE = (By.CSS_SELECTOR, ".header-toggle")
HEADER = (By.ID, "header")
NAV_LINKS = (By.CSS_SELECTOR, "#navmenu ul li a")


def _header_right_edge(context):
    return context.site.driver.execute_script(
        "return document.querySelector('#header').getBoundingClientRect().right;"
    )


def _header_classes(context):
    return context.site.find(HEADER).get_attribute("class")


@then("the navigation toggle should be offered")
def step_toggle_offered(context):
    assert context.site.wait_visible(TOGGLE).is_displayed()


@when("I tap the navigation toggle")
def step_tap_toggle(context):
    context.site.js_click(context.site.wait_visible(TOGGLE))


@then("the sidebar should be off-canvas")
def step_sidebar_off_canvas(context):
    # The sidebar slides on a CSS transition, so poll rather than read once.
    context.site.wait_until(
        lambda: "header-show" not in _header_classes(context),
        message="the header still carries .header-show",
    )
    context.site.wait_until(
        lambda: _header_right_edge(context) <= 0,
        message=f"the sidebar is still on screen (right edge {_header_right_edge(context)})",
    )


@then("the sidebar should be on screen")
def step_sidebar_on_screen(context):
    context.site.wait_until(
        lambda: "header-show" in _header_classes(context),
        message="tapping the toggle did not add .header-show",
    )
    context.site.wait_until(
        lambda: _header_right_edge(context) > 0,
        message="the sidebar never came on screen",
    )


@then("the menu should list {count:d} links")
def step_menu_link_count(context, count):
    assert len(context.site.find_all(NAV_LINKS)) == count


@then("the navigation toggle should report itself as collapsed")
def step_toggle_collapsed(context):
    assert context.site.find(TOGGLE).get_attribute("aria-expanded") == "false"


@then("the navigation toggle should report itself as expanded")
def step_toggle_expanded(context):
    context.site.wait_until(
        lambda: context.site.find(TOGGLE).get_attribute("aria-expanded") == "true",
        message="aria-expanded was not updated when the menu opened",
    )


@then("the page should not scroll horizontally")
def step_no_horizontal_scroll(context):
    overflow = context.site.driver.execute_script(
        "return document.documentElement.scrollWidth"
        " - document.documentElement.clientWidth;"
    )
    assert overflow <= 1, f"the page scrolls sideways by {overflow}px"
