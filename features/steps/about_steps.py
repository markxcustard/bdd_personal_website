"""About section steps."""

from behave import then
from selenium.webdriver.common.by import By


@then('the about headline should be "{expected}"')
def step_about_headline(context, expected):
    headline = context.site.reveal_one((By.CSS_SELECTOR, "#about .content h2"))
    assert context.site.text_of(headline) == expected


@then("the about facts should be:")
def step_about_facts(context):
    facts = context.site.about_facts()
    expected = {row["label"]: row["value"] for row in context.table}
    missing = [label for label in expected if label not in facts]
    assert not missing, f"missing facts: {missing}"
    for label, value in expected.items():
        assert facts[label] == value, (
            f"{label}: expected {value!r}, got {facts[label]!r}"
        )
    assert set(facts) == set(expected), (
        f"unexpected extra facts: {sorted(set(facts) - set(expected))}"
    )
