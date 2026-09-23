Feature: Navigating the portfolio
  As a visitor to Mark's portfolio
  I want to move between sections from the menu
  So that I can find his experience, projects and contact details

  Background:
    Given I am on the portfolio home page

  @smoke
  Scenario: The page identifies itself
    Then the page title should be "Mark Custard - QA & Automation Engineering Lead"
    And the site name should be "Mark Custard"
    And a profile photo should be shown

  Scenario: The menu links to every section in order
    Then the navigation menu should be:
      | section          | label            |
      | hero             | Home             |
      | about            | About            |
      | resume           | Resume           |
      | portfolio        | Portfolio        |
      | technical-skills | Technical Skills |
      | skills           | Skills           |
      | testimonials     | Testimonials     |
      | contact          | Contact          |

  @smoke
  Scenario Outline: Every section can be opened from the menu
    When I open the "<section>" section from the menu
    Then the "<section>" section should be visible

    Examples: sections
      | section          |
      | hero             |
      | about            |
      | resume           |
      | portfolio        |
      | technical-skills |
      | skills           |
      | testimonials     |
      | contact          |

  Scenario Outline: The menu highlights whichever section is in view
    When I open the "<section>" section from the menu
    Then the "<section>" menu item should be highlighted

    Examples: sections with a scrollspy target
      | section          |
      | about            |
      | resume           |
      | portfolio        |
      | technical-skills |
      | skills           |
      | testimonials     |
      | contact          |

  Scenario Outline: Each section announces itself with a heading
    When I open the "<section>" section from the menu
    Then the section heading should be "<heading>"

    Examples: headings
      | section          | heading          |
      | about            | About            |
      | resume           | Resume           |
      | portfolio        | Portfolio        |
      | technical-skills | Technical Skills |
      | skills           | Skills           |
      | testimonials     | Testimonials     |
      | contact          | Contact          |

  Scenario: The header links out to Mark's profiles
    Then the header social links should be:
      | url                                       |
      | https://github.com/markxcustard           |
      | https://www.linkedin.com/in/mark-custard/ |

  Scenario: The hero introduces Mark and the roles he covers
    When I open the "hero" section from the menu
    Then the hero heading should be "Mark Custard"
    And the hero should rotate through the roles:
      | role                      |
      | QA & Automation Lead      |
      | Test Automation Engineer  |
      | Full-Stack Engineer       |
      | API Testing Specialist    |
      | Test Strategy Owner       |

  Scenario: The footer is reachable
    Then the footer should be visible
