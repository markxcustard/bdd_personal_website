Feature: About section
  As a recruiter
  I want Mark's headline facts in one place
  So that I can judge fit without reading the whole page

  Background:
    Given I am on the portfolio home page
    When I open the "about" section from the menu

  @smoke
  Scenario: The About section leads with Mark's current role
    Then the about headline should be "QA & Automation Engineering Lead"

  Scenario: The fact list covers the essentials
    Then the about facts should be:
      | label          | value                       |
      | Degree         | Bachelor of Laws (LLB)      |
      | GitHub         | github.com/markxcustard     |
      | Phone          | (360) 771-0564              |
      | City           | Ridgefield, Washington      |
      | Experience     | 7+ Years                    |
      | Specialization | QA, Automation & Full-Stack |
      | Email          | mark.a.custard@gmail.com    |
      | Freelance      | Available                   |
