Feature: Testimonials carousel
  As a visitor
  I want to read what Mark's colleagues say about him
  So that I have more than his own word for it

  Background:
    Given I am on the portfolio home page
    When I open the "testimonials" section from the menu

  Scenario: Every testimonial is carried
    Then the testimonials should be:
      | name                   | role                                                    |
      | Santiago Guerrero      | SR Software Development Engineer in Testing at Glassdoor |
      | Jon Kim                | iOS Developer at Stake                                  |
      | Julia Guimiot          | Back End Software Engineer at Stake                     |
      | Dominic Withers        | Managing Director & Co-Founder at Withers & Wagg        |
      | Kristian Andrews-Brown | Founder of TAG Parking                                  |

  Scenario: Each name links to the person's LinkedIn profile
    Then the testimonial profile links should be:
      | name                   | url                                                    |
      | Santiago Guerrero      | https://www.linkedin.com/in/sguerrero22/                |
      | Jon Kim                | https://www.linkedin.com/in/jonathanyjkim/              |
      | Julia Guimiot          | https://www.linkedin.com/in/juliaguimiot/               |
      | Dominic Withers        | https://www.linkedin.com/in/dominic-withers-221002100/  |
      | Kristian Andrews-Brown | https://www.linkedin.com/in/kristian-andrews-82543b109  |

  Scenario: Every testimonial carries a real quote
    Then every testimonial should quote at least 40 characters

  Scenario: The carousel offers one bullet per testimonial
    Then the carousel should offer 5 pagination bullets

  Scenario: The carousel starts on the first testimonial
    Then the active testimonial should be "Santiago Guerrero"

  Scenario: Pagination moves the carousel on
    When I select pagination bullet 3
    Then the active testimonial should have changed
