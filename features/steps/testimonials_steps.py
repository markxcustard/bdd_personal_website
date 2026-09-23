"""Testimonial carousel steps."""

from behave import then, when


@then("the testimonials should be:")
def step_testimonials(context):
    entries = context.site.testimonials()
    assert [e["name"] for e in entries] == [row["name"] for row in context.table]
    by_name = {e["name"]: e for e in entries}
    for row in context.table:
        assert by_name[row["name"]]["role"] == row["role"], (
            f"{row['name']}: role was {by_name[row['name']]['role']!r}"
        )


@then("the testimonial profile links should be:")
def step_testimonial_links(context):
    by_name = {e["name"]: e for e in context.site.testimonials()}
    for row in context.table:
        assert by_name[row["name"]]["linkedin"] == row["url"], (
            f"{row['name']} links to {by_name[row['name']]['linkedin']}"
        )


@then("every testimonial should quote at least {length:d} characters")
def step_quotes_present(context, length):
    short = [
        e["name"] for e in context.site.testimonials() if len(e["quote"]) < length
    ]
    assert not short, f"quotes look truncated or empty for: {short}"


@then("the carousel should offer {count:d} pagination bullets")
def step_bullets(context, count):
    actual = len(context.site.testimonial_bullets())
    assert actual == count, f"expected {count} bullets, found {actual}"


@then('the active testimonial should be "{name}"')
def step_active_testimonial(context, name):
    assert context.site.active_testimonial_name() == name


@when("I select pagination bullet {position:d}")
def step_select_bullet(context, position):
    context.previous_testimonial = context.site.active_testimonial_name()
    bullet = context.site.testimonial_bullets()[position - 1]
    context.site.js_click(bullet)


@then("the active testimonial should have changed")
def step_testimonial_changed(context):
    # Autoplay runs on a 5s delay, so assert that it moved rather than that it
    # landed on one specific name.
    context.site.wait_until(
        lambda: context.site.active_testimonial_name() != context.previous_testimonial,
        message="the carousel never moved off the previous testimonial",
    )
    assert context.site.active_testimonial_name() != context.previous_testimonial
