"""Contact section steps.

Nothing here submits the form with valid data: it posts to a live Formspree
endpoint and would deliver a real email on every run.
"""

from behave import then, when
from selenium.webdriver.common.by import By

FIELD_IDS = {
    "name": (By.ID, "name-field"),
    "email": (By.ID, "email-field"),
    "subject": (By.ID, "subject-field"),
    "message": (By.ID, "message-field"),
}
SUBMIT = (By.CSS_SELECTOR, "#contact form button[type='submit']")
FORM = (By.CSS_SELECTOR, "#contact form")


@then("the contact details should be:")
def step_contact_details(context):
    blocks = context.site.contact_info()
    assert [b["heading"] for b in blocks] == [row["heading"] for row in context.table]
    by_heading = {b["heading"]: b["lines"] for b in blocks}
    for row in context.table:
        lines = by_heading[row["heading"]]
        assert any(row["value"] in line for line in lines), (
            f"{row['heading']}: {row['value']!r} not found in {lines}"
        )


@then('the "{heading}" block should include "{value}"')
def step_block_includes(context, heading, value):
    by_heading = {b["heading"]: b["lines"] for b in context.site.contact_info()}
    assert heading in by_heading, f"no contact block called {heading!r}"
    assert any(value in line for line in by_heading[heading]), (
        f"{heading}: {value!r} not found in {by_heading[heading]}"
    )


@then("the contact form should offer the fields:")
def step_form_fields(context):
    context.site.reveal_one(FORM)
    for row in context.table:
        locator = FIELD_IDS[row["field"]]
        assert context.site.wait_visible(locator).is_displayed(), (
            f"the {row['field']} field is not visible"
        )


@then('the submit button should read "{label}"')
def step_submit_label(context, label):
    # CSS uppercases the button, so compare the source text, not the rendered text.
    assert context.site.text_of(context.site.wait_visible(SUBMIT)) == label


@then("every contact form field should be required")
def step_fields_required(context):
    required = context.site.driver.execute_script(
        "return Array.from(document.querySelectorAll('#contact form [required]'))"
        ".map(f => f.getAttribute('name'));"
    )
    assert sorted(required) == sorted(FIELD_IDS), f"required fields were {required}"


@then('the contact form should post to "{endpoint}"')
def step_form_action(context, endpoint):
    assert context.site.find(FORM).get_attribute("action") == endpoint


@then("the contact form should be invalid")
def step_form_invalid(context):
    assert context.site.form_is_valid() is False


@then("the contact form should be valid")
def step_form_valid(context):
    assert context.site.form_is_valid() is True
    # Deliberately no submit: the endpoint delivers real email.


@when("I submit the empty contact form")
def step_submit_empty(context):
    context.site.reveal_one(FORM)
    context.url_before_submit = context.site.driver.current_url
    context.site.js_click(context.site.find(SUBMIT))


@then("the page should not have navigated away")
def step_no_navigation(context):
    assert context.site.driver.current_url == context.url_before_submit


@when('I fill in the contact form with the email "{email}"')
def step_fill_form(context, email):
    context.site.reveal_one(FORM)
    context.site.find(FIELD_IDS["name"]).send_keys("Test Runner")
    context.site.find(FIELD_IDS["email"]).send_keys(email)
    context.site.find(FIELD_IDS["subject"]).send_keys("Automated check")
    context.site.find(FIELD_IDS["message"]).send_keys("Validation only — not submitted.")


@then("the email field should report a type mismatch")
def step_email_type_mismatch(context):
    assert context.site.driver.execute_script(
        "return arguments[0].validity.typeMismatch;",
        context.site.find(FIELD_IDS["email"]),
    ) is True
