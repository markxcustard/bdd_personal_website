Feature: Portfolio grid
  As a visitor
  I want to browse Mark's projects and filter them by discipline
  So that I can go straight to the code that interests me

  Background:
    Given I am on the portfolio home page
    When I open the portfolio grid

  @smoke
  Scenario: Every project is shown by default
    Then 6 projects should be visible
    And the projects should be:
      | title                       | tags                          |
      | Personal Website Automation | Selenium, pytest, Page Objects |
      | BDD Personal Website        | BDD, Gherkin, Behave          |
      | Cypress Portfolio Tests     | Cypress, JavaScript, E2E      |
      | Flight Delay Notifier       | pytest, Mocking, Fixtures     |
      | Pandas Filtering Films      | Python, Pandas, pytest        |
      | Films CRUD                  | SQLAlchemy, SQLite, pytest    |

  @smoke
  Scenario: Each project links to its repository
    Then the project links should be:
      | title                       | url                                                        |
      | Personal Website Automation | https://github.com/markxcustard/personal_website_automation |
      | BDD Personal Website        | https://github.com/markxcustard/bdd_personal_website        |
      | Cypress Portfolio Tests     | https://github.com/markxcustard/cypress_personal_website    |
      | Flight Delay Notifier       | https://github.com/markxcustard/flight_delay_notifier       |
      | Pandas Filtering Films      | https://github.com/markxcustard/pandas_filtering_films      |
      | Films CRUD                  | https://github.com/markxcustard/database_crud               |

  Scenario: Repository links open safely in a new tab
    Then every project link should open in a new tab with rel="noopener"

  Scenario: The filters are offered
    Then the portfolio filters should be:
      | label      |
      | All        |
      | Automation |
      | BDD        |
      | Unit       |
      | Data       |
      | Database   |

  Scenario Outline: Filtering narrows the grid
    When I filter the portfolio by "<filter>" expecting <count> projects
    Then the "<filter>" filter should be marked active

    Examples: filters
      | filter     | count |
      | All        | 6     |
      | Automation | 2     |
      | BDD        | 1     |
      | Unit       | 1     |
      | Data       | 1     |
      | Database   | 1     |

  Scenario: The Automation filter keeps both browser suites
    When I filter the portfolio by "Automation" expecting 2 projects
    Then the visible projects should be:
      | title                       |
      | Personal Website Automation |
      | Cypress Portfolio Tests     |

  Scenario Outline: Each single-project filter keeps the right one
    When I filter the portfolio by "<filter>" expecting 1 project
    Then only "<title>" should be visible

    Examples: filters
      | filter   | title                  |
      | BDD      | BDD Personal Website   |
      | Unit     | Flight Delay Notifier  |
      | Data     | Pandas Filtering Films |
      | Database | Films CRUD             |

  Scenario: The All filter restores the full grid
    When I filter the portfolio by "Automation" expecting 2 projects
    And I filter the portfolio by "All" expecting 6 projects
    Then 6 projects should be visible

  # The template shipped these filters as bare <li> elements with click
  # handlers, so they could not be reached or operated by keyboard at all.
  Scenario: The filters can be reached by keyboard
    Then every filter should be focusable
    And every filter should expose a button role

  Scenario: Only the active filter reports itself as pressed
    Then the "All" filter should report itself as pressed
    When I filter the portfolio by "BDD" expecting 1 project
    Then the "BDD" filter should report itself as pressed
    And the "All" filter should not report itself as pressed

  Scenario Outline: A filter can be activated with the keyboard
    When I focus the "Automation" filter and press "<key>"
    Then 2 projects should be visible
    And the "Automation" filter should be marked active

    Examples: keys
      | key   |
      | Enter |
      | Space |

  Scenario: Each repository link has a distinct accessible name
    Then every project link should have its own accessible name

  Scenario: Heading levels do not skip
    Then the portfolio headings should run h2 then h3

  # The cards were 441px tall for three lines of text — about one phone screen
  # each. They are one padded container now, and lead with a number.
  Scenario: Each project advertises its headline number
    Then the project metrics should be:
      | title                       | metric       |
      | Personal Website Automation | 174 tests    |
      | BDD Personal Website        | 91 scenarios |
      | Cypress Portfolio Tests     | 170 tests    |
      | Flight Delay Notifier       | 91 tests     |
      | Pandas Filtering Films      | 54 tests     |
      | Films CRUD                  | 60 tests     |

  Scenario: No description is cut off by the three-line clamp
    Then no project description should be clipped

  Scenario: The whole card is a click target
    Then clicking the middle of each card should open its repository

  # The filters were bare 14px-tall text, far below a usable tap size.
  Scenario: The filters are large enough to tap
    Then every filter should be at least 44 by 44 pixels
