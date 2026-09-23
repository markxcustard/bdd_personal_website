Feature: Skills and technical skills
  As a technical interviewer
  I want to see which tools Mark claims and at what level
  So that I know what to probe in an interview

  Background:
    Given I am on the portfolio home page

  Scenario: The technical skill groups are all present
    When I open the "technical-skills" section from the menu
    Then the technical skill groups should be:
      | group                            |
      | Programming Languages            |
      | Testing Tools                    |
      | Types of Testing                 |
      | Test Practices & Methodologies   |
      | Frameworks & Libraries           |
      | Project Management & Agile       |
      | Version Control & CI/CD          |
      | Cloud & Databases                |
      | Developer Tools & Integrations   |
      | Platform Testing                 |

  Scenario Outline: Key tools stay listed under the right group
    When I open the "technical-skills" section from the menu
    Then the "<group>" group should mention "<tool>"

    Examples: tools worth failing a build over
      | group                          | tool                 |
      | Programming Languages          | Python               |
      | Programming Languages          | TypeScript           |
      | Testing Tools                  | Playwright           |
      | Testing Tools                  | pytest               |
      | Testing Tools                  | Selenium             |
      | Frameworks & Libraries         | Behave               |
      | Test Practices & Methodologies | Page Object Model    |
      | Version Control & CI/CD        | GitHub Actions       |

  Scenario: Every group carries a description
    When I open the "technical-skills" section from the menu
    Then every technical skill group should have a description

  Scenario: Skill levels are published
    When I open the "skills" section from the menu
    Then the skill levels should be:
      | skill                                                 | percentage |
      | Test Automation (Playwright, pytest, Vitest)           | 95         |
      | Manual & Exploratory Testing                           | 95         |
      | Test Strategy & Coverage Design                        | 90         |
      | Python, JavaScript & SQL                               | 90         |
      | API & Integration Testing (Postman, ChaiJS)            | 90         |
      | CI/CD & Release Gating (GitHub Actions, Azure DevOps)  | 90         |
      | Salesforce & Data Validation                           | 85         |

  Scenario: The visible percentage matches the accessible one
    When I open the "skills" section from the menu
    Then every skill label should match its aria-valuenow
