"""Page-level and navigation steps."""

from behave import given, then, when
from selenium.webdriver.common.by import By

from support.site import TITLE


@given("I am on the portfolio home page")
def step_on_home_page(context):
    """The page is loaded in ``before_scenario``; this asserts it arrived.

    Deliberately does not assert that the menu is *visible*: below the xl
    breakpoint it is collapsed behind the hamburger toggle, which the @mobile
    scenarios rely on.
    """
    assert context.site.driver.current_url.startswith("http")
    assert context.site.find((By.ID, "header")).is_displayed()
    assert context.site.find((By.ID, "navmenu")) is not None


@when('I open the "{section}" section from the menu')
def step_open_section(context, section):
    context.site.go_to_section(section)
    context.current_section = section


@then('the page title should be "{expected}"')
def step_page_title(context, expected):
    assert context.site.driver.title == expected, (
        f"expected title {expected!r}, got {context.site.driver.title!r}"
    )
    assert expected == TITLE


@then('the site name should be "{expected}"')
def step_site_name(context, expected):
    assert context.site.text_of((By.CSS_SELECTOR, "#header .sitename")) == expected


@then("a profile photo should be shown")
def step_profile_photo(context):
    image = context.site.find((By.CSS_SELECTOR, "#header .profile-img img"))
    assert image.get_attribute("src").endswith("my-profile-img.jpg")


@then("the navigation menu should be:")
def step_navigation_menu(context):
    expected = [
        {"section": row["section"], "label": row["label"]} for row in context.table
    ]
    assert context.site.menu_entries() == expected


@then('the "{section}" section should be visible')
def step_section_visible(context, section):
    assert context.site.section(section).is_displayed()


@then('the "{section}" menu item should be highlighted')
def step_menu_highlighted(context, section):
    assert context.site.active_nav_section() == section


@then('the section heading should be "{expected}"')
def step_section_heading(context, expected):
    assert context.site.section_heading(context.current_section) == expected


@then("the header social links should be:")
def step_header_social_links(context):
    actual = [
        link.get_attribute("href")
        for link in context.site.reveal(
            (By.CSS_SELECTOR, "#header .social-links a")
        )
    ]
    assert actual == [row["url"] for row in context.table]


@then('the hero heading should be "{expected}"')
def step_hero_heading(context, expected):
    assert context.site.text_of(context.site.reveal_one((By.CSS_SELECTOR, "#hero h2"))) == expected


@then("the hero should rotate through the roles:")
def step_hero_roles(context):
    typed = context.site.find((By.CSS_SELECTOR, "#hero .typed"))
    actual = [r.strip() for r in typed.get_attribute("data-typed-items").split(",")]
    assert actual == [row["role"] for row in context.table]


@then("the footer should be visible")
def step_footer_visible(context):
    assert context.site.reveal_one((By.ID, "footer")).is_displayed()


@then("every hero role should begin with an article")
def step_roles_articled(context):
    bad = [
        role
        for role in context.site.hero_typed_items()
        if not (role.startswith("a ") or role.startswith("an "))
    ]
    assert not bad, f"roles without an article: {bad}"


@then('the hero roles should include "{role}"')
def step_roles_include(context, role):
    items = context.site.hero_typed_items()
    assert role in items, f"{role!r} not among {items}"


@then("the hero line should read cleanly once a full role is typed")
def step_hero_line_clean(context):
    roles = context.site.hero_typed_items()
    captured = {}

    def a_complete_role_is_showing():
        snapshot = context.site.hero_snapshot()
        if snapshot["role"] in roles:
            captured.update(snapshot)
            return True
        return False

    context.site.wait_until(
        a_complete_role_is_showing,
        timeout=30,
        message="Typed.js never settled on a complete role",
    )

    assert "  " not in captured["line"], repr(captured["line"])
    assert captured["line"].startswith(f"I'm {captured['role']}")
