"""Resume section steps, including the PDF download."""

import os

from behave import then, when


@then("the resume should list:")
def step_resume_lists(context):
    headings = context.site.resume_headings()
    for row in context.table:
        assert row["entry"] in headings, (
            f"{row['entry']!r} is not listed on the resume; got {headings}"
        )


@then('the resume download link should point at "{filename}"')
def step_resume_link(context, filename):
    href = context.site.resume_download_link().get_attribute("href")
    assert href.endswith(filename), f"download points at {href}"


@then('the download should be named "{filename}"')
def step_download_name(context, filename):
    assert context.site.resume_download_link().get_attribute("download") == filename


@when("I click the download resume button")
def step_click_download(context):
    context.site.js_click(context.site.resume_download_link())


@then("a PDF should be saved to disk")
def step_pdf_saved(context):
    if context.browser_name == "safari":
        context.scenario.skip("SafariDriver cannot use a custom download directory")
        return

    context.site.wait_until(
        lambda: any(f.endswith(".pdf") for f in os.listdir(context.download_dir)),
        timeout=30,
        message=f"no PDF appeared in {context.download_dir}",
    )
    saved = [f for f in os.listdir(context.download_dir) if f.endswith(".pdf")]
    assert saved, "resume PDF was not written to disk"
    assert os.path.getsize(os.path.join(context.download_dir, saved[0])) > 0
