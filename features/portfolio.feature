Feature: Portfolio grid
  As a visitor
  I want to browse Mark's projects and filter them by discipline
  So that I can go straight to the code that interests me

  Background:
    Given I am on the portfolio home page
    When I open the portfolio grid

  @smoke
  Scenario: Every project is shown by default
    Then 4 projects should be visible
    And the projects should be:
      | title                       | tags                              |
      | Personal Website Automation | Selenium, Python, Automation      |
      | BDD Personal Website        | BDD, Gherkin, Selenium            |
      | Pandas Filtering Films      | Python, Pandas, Data Analysis     |
      | Films CRUD API              | API, SQLAlchemy, SQLite           |

  @smoke
  Scenario: Each project links to its repository
    Then the project links should be:
      | title                       | url                                                        |
      | Personal Website Automation | https://github.com/markxcustard/personal_website_automation |
      | BDD Personal Website        | https://github.com/markxcustard/bdd_personal_website        |
      | Pandas Filtering Films      | https://github.com/markxcustard/pandas_filtering_films      |
      | Films CRUD API              | https://github.com/markxcustard/database_crud               |

  Scenario: Repository links open safely in a new tab
    Then every project link should open in a new tab with rel="noopener"

  Scenario: The filters are offered
    Then the portfolio filters should be:
      | label      |
      | All        |
      | Automation |
      | BDD        |
      | API        |
      | Data       |

  Scenario Outline: Filtering narrows the grid to one project
    When I filter the portfolio by "<filter>" expecting 1 project
    Then only "<title>" should be visible
    And the "<filter>" filter should be marked active

    Examples: filters
      | filter     | title                       |
      | Automation | Personal Website Automation |
      | BDD        | BDD Personal Website        |
      | Data       | Pandas Filtering Films      |
      | API        | Films CRUD API              |

  Scenario: The All filter restores the full grid
    When I filter the portfolio by "Automation" expecting 1 project
    And I filter the portfolio by "All" expecting 4 projects
    Then 4 projects should be visible
