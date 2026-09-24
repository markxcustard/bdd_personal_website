"""Portfolio grid steps."""

from behave import then, when


@when("I open the portfolio grid")
def step_open_portfolio(context):
    context.site.open_portfolio()
    context.current_section = "portfolio"


@then("{count:d} projects should be visible")
def step_visible_count(context, count):
    # Isotope animates cards in and out, so wait for the grid to settle rather
    # than reading it once.
    context.site.wait_until(
        lambda: len(context.site.visible_portfolio_titles()) == count,
        message=(
            f"expected {count} visible, got "
            f"{context.site.visible_portfolio_titles()}"
        ),
    )
    assert len(context.site.visible_portfolio_titles()) == count


@then("the projects should be:")
def step_projects(context):
    cards = {c["title"]: c for c in context.site.portfolio_cards()}
    order = [c["title"] for c in context.site.portfolio_cards()]
    expected_order = [row["title"] for row in context.table]
    assert order == expected_order, f"card order was {order}"
    for row in context.table:
        expected_tags = [t.strip() for t in row["tags"].split(",")]
        assert cards[row["title"]]["tags"] == expected_tags, (
            f"{row['title']}: tags were {cards[row['title']]['tags']}"
        )


@then("the project links should be:")
def step_project_links(context):
    cards = {c["title"]: c for c in context.site.portfolio_cards()}
    for row in context.table:
        assert cards[row["title"]]["url"] == row["url"], (
            f"{row['title']} links to {cards[row['title']]['url']}"
        )


@then('every project link should open in a new tab with rel="noopener"')
def step_links_open_safely(context):
    for card in context.site.portfolio_cards():
        assert card["target"] == "_blank", f"{card['title']} does not open in a new tab"
        # Without noopener the opened tab keeps a handle on window.opener.
        assert "noopener" in card["rel"], f"{card['title']} is missing rel=noopener"


@then("the portfolio filters should be:")
def step_filters(context):
    from selenium.webdriver.common.by import By

    actual = [
        context.site.text_of(chip)
        for chip in context.site.reveal(
            (By.CSS_SELECTOR, "#portfolio .portfolio-filters li")
        )
    ]
    assert actual == [row["label"] for row in context.table]


@when('I filter the portfolio by "{label}" expecting {count:d} project')
@when('I filter the portfolio by "{label}" expecting {count:d} projects')
def step_filter(context, label, count):
    context.site.filter_portfolio(label, count)


@then('only "{title}" should be visible')
def step_only_visible(context, title):
    context.site.wait_until(
        lambda: context.site.visible_portfolio_titles() == [title],
        message=f"visible: {context.site.visible_portfolio_titles()}",
    )
    assert context.site.visible_portfolio_titles() == [title]


@then('the "{label}" filter should be marked active')
def step_filter_active(context, label):
    context.site.wait_until(
        lambda: context.site.active_filter_label() == label,
        message=f"active filter is {context.site.active_filter_label()!r}",
    )
    assert context.site.active_filter_label() == label


@then("the visible projects should be:")
def step_visible_projects(context):
    expected = sorted(row["title"] for row in context.table)
    context.site.wait_until(
        lambda: sorted(context.site.visible_portfolio_titles()) == expected,
        message=f"visible: {context.site.visible_portfolio_titles()}",
    )
    assert sorted(context.site.visible_portfolio_titles()) == expected


@then("every filter should be focusable")
def step_filters_focusable(context):
    chips = context.site.filter_chips()
    assert chips, "no filter chips found"
    not_focusable = [c["label"] for c in chips if c["tabindex"] != 0]
    assert not not_focusable, f"not reachable by keyboard: {not_focusable}"


@then("every filter should expose a button role")
def step_filters_have_role(context):
    wrong = [c["label"] for c in context.site.filter_chips() if c["role"] != "button"]
    assert not wrong, f"missing role=button: {wrong}"


@then('the "{label}" filter should report itself as pressed')
def step_filter_pressed(context, label):
    chips = {c["label"]: c["pressed"] for c in context.site.filter_chips()}
    assert chips.get(label) == "true", f"{label} reports aria-pressed={chips.get(label)}"


@then('the "{label}" filter should not report itself as pressed')
def step_filter_not_pressed(context, label):
    chips = {c["label"]: c["pressed"] for c in context.site.filter_chips()}
    assert chips.get(label) == "false", f"{label} reports aria-pressed={chips.get(label)}"


@when('I focus the "{label}" filter and press "{key}"')
def step_keyboard_activate(context, label, key):
    context.site.press_filter_with_keyboard(label, key)


@then("every project link should have its own accessible name")
def step_links_have_names(context):
    labels = context.site.portfolio_link_labels()
    missing = [i for i, label in enumerate(labels) if not label]
    assert not missing, f"links without aria-label at positions {missing}"
    assert len(set(labels)) == len(labels), f"duplicate accessible names: {labels}"


@then("the portfolio headings should run h2 then h3")
def step_heading_levels(context):
    levels = context.site.portfolio_heading_levels()
    assert levels[0] == "H2", f"section heading is {levels[0]}"
    assert set(levels[1:]) == {"H3"}, f"card headings are {set(levels[1:])}"
