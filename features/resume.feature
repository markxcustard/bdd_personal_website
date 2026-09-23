Feature: Resume section
  As a hiring manager
  I want to read Mark's history and take the PDF away with me
  So that I can share it with my team

  Background:
    Given I am on the portfolio home page
    When I open the "resume" section from the menu

  Scenario: Every role is listed
    Then the resume should list:
      | entry                               |
      | Lead Engineer, Full Stack & Quality |
      | QA Analyst — Manual \| Automation   |
      | Senior QA Engineer                  |
      | QA Analyst                          |
      | QA Engineer                         |
      | Software QA Analyst                 |
      | Junior Application Developer        |

  Scenario: Education is listed
    Then the resume should list:
      | entry                                  |
      | Web Development Certification          |
      | Bachelor of Laws (LLB) in Business Law |

  @smoke
  Scenario: The download button offers the current resume
    Then the resume download link should point at "mark_custard_resume_09_2026.pdf"
    And the download should be named "Mark_Custard_Resume.pdf"

  @download
  Scenario: Downloading the resume saves a PDF
    When I click the download resume button
    Then a PDF should be saved to disk
