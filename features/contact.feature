Feature: Contact section
  As someone who wants to hire Mark
  I want his contact details and a working enquiry form
  So that I can reach him

  # The form posts to a live Formspree endpoint, so no scenario here ever
  # submits it with valid data — that would deliver a real email on every run.
  # Validation is asserted by asking the browser, or by submitting it empty so
  # browser-side validation blocks the request.

  Background:
    Given I am on the portfolio home page
    When I open the "contact" section from the menu

  Scenario: The contact details are listed in order
    Then the contact details should be:
      | heading   | value                        |
      | Address   | Ridgefield, Washington, 98642 |
      | Call Me   | +1 (360) 771-0564            |
      | Email Me  | mark.a.custard@gmail.com     |
      | LinkedIn  | linkedin.com/in/mark-custard |
      | GitHub    | github.com/markxcustard      |

  @smoke
  Scenario: Both phone numbers are offered
    Then the "Call Me" block should include "+1 (360) 771-0564"
    And the "Call Me" block should include "+44 7441 343276"

  @smoke
  Scenario: The enquiry form offers every field
    Then the contact form should offer the fields:
      | field   |
      | name    |
      | email   |
      | subject |
      | message |
    And the submit button should read "Send Message"

  Scenario: Every field is required
    Then every contact form field should be required

  Scenario: The form posts to the expected endpoint
    Then the contact form should post to "https://formspree.io/f/mpwkzpjv"

  Scenario: An empty form is rejected
    Then the contact form should be invalid

  Scenario: Submitting an empty form does not leave the page
    When I submit the empty contact form
    Then the page should not have navigated away
    And the contact form should be invalid

  Scenario: A malformed email keeps the form invalid
    When I fill in the contact form with the email "not-an-email"
    Then the contact form should be invalid
    And the email field should report a type mismatch

  Scenario: A well-formed enquiry satisfies validation
    When I fill in the contact form with the email "runner@example.com"
    Then the contact form should be valid
