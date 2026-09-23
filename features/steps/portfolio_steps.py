"""Portfolio grid steps."""

from behave import then, when


@when("I open the portfolio grid")
def step_open_portfolio(context):
    context.site.open_portfolio()
    context.current_section = "portfolio"


@then("{count:d} projects should be visible")
def step_visible_count(context, count):
    visible = context.site.visible_portfolio_titles()
    assert len(visible) == count, f"expected {count} visible, got {visible}"


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
    assert context.site.visible_portfolio_titles() == [title]


@then('the "{label}" filter should be marked active')
def step_filter_active(context, label):
    assert context.site.active_filter_label() == label
