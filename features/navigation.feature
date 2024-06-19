Feature: Navigation menu

  @about
  Scenario: Navigate to About section
    Given I open the website "https://markxcustard.github.io/"
    When I click on the About link
    Then the About section should be visible

  @portfolio
  Scenario: Navigate to Portfolio section
    Given I open the website "https://markxcustard.github.io/"
    When I click on the Portfolio link
    Then the Portfolio section should be visible

  @testimonials
  Scenario: Navigate to Testimonials section
    Given I open the website "https://markxcustard.github.io/"
    When I click on the Testimonials link
    Then the Testimonials section should be visible

  @contact
  Scenario: Navigate to Contact section
    Given I open the website "https://markxcustard.github.io/"
    When I click on the Contact link
    Then the Contact section should be visible

  @homepage
  Scenario: Verify homepage content
    Given I open the website "https://markxcustard.github.io/"
    Then the homepage should display the correct title

  @github_personal_website_automation
  Scenario: Redirect to GitHub repository
    Given I open the website "https://markxcustard.github.io/"
    When I click on the GitHub link
    Then I should be directed to "https://github.com/markxcustard/personal_website_automation"

  @resume
  Scenario: Download resume
    Given I open the website "https://markxcustard.github.io/"
    When I click on the download resume button
    Then I should be able to download the resume

  @stake
  Scenario: Expand QA Analyst card
    Given I open the website "https://markxcustard.github.io/"
    When I click on QA Analyst at Stake (Fintech Industry)
    Then the card expands and user can view my duties and experiences at Stake

  @stake_close
  Scenario: Close QA Analyst card
    Given I open the website "https://markxcustard.github.io/"
    When I click on QA Analyst at Stake (Fintech Industry)
    And I close the QA Analyst at Stake (Fintech Industry) card
    Then the Stake card should be collapsed

  @csc
  Scenario: Expand CSC Generation card
    Given I open the website "https://markxcustard.github.io/"
    When I click on QA Engineer at CSC Generation
    Then the card expands and user can view my duties and experiences at CSC Generation

  @csc_close
  Scenario: Close CSC Generation card
    Given I open the website "https://markxcustard.github.io/"
    When I click on QA Engineer at CSC Generation
    And I close the QA Engineer at CSC Generation card
    Then the CSC Generation card should be collapsed

  @kemper
  Scenario: Expand Software QA Analyst at Kemper card
    Given I open the website "https://markxcustard.github.io/"
    When I click on Software QA Analyst at Kemper Insurance
    Then the card expands and user can view my duties and experiences at Kemper Insurance

  @kemper_close
  Scenario: Close Software QA Analyst at Kemper card
    Given I open the website "https://markxcustard.github.io/"
    When I click on Software QA Analyst at Kemper Insurance
    And I close the Software QA Analyst at Kemper Insurance card
    Then the Kemper Insurance card should be collapsed

  @aacc_qa
  Scenario: Expand Software QA Analyst at American Access Casualty card
    Given I open the website "https://markxcustard.github.io/"
    When I click on Software QA Analyst at AACC
    Then the card expands and user can view my duties and experiences at AACC

  @aacc_qa_close
  Scenario: Close Software QA Analyst at American Access Casualty card
    Given I open the website "https://markxcustard.github.io/"
    When I click on Software QA Analyst at AACC
    And I close the Software QA Analyst at AACC card
    Then the AACC card should be collapsed

  @aacc_jad
  Scenario: Expand Junior Application Developer at American Access Casualty card
    Given I open the website "https://markxcustard.github.io/"
    When I click on Junior Application Developer at AACC
    Then the card expands and user can view my duties and experiences as a Junior Application Developer at AACC

  @aacc_jad_close
  Scenario: Close Junior Application Developer at American Access Casualty card
    Given I open the website "https://markxcustard.github.io/"
    When I click on Junior Application Developer at AACC
    And I close the Junior Application Developer at AACC card
    Then the Junior Application Developer card should be collapsed

  @tech
  Scenario: Expand Technical Skills card
    Given I open the website "https://markxcustard.github.io/"
    When I click on Technical Skills
    Then the card expands and user can view my technical skills

  @tech_close
  Scenario: Close Technical Skills card
    Given I open the website "https://markxcustard.github.io/"
    When I click on Technical Skills
    And I close the Technical Skills card
    Then the Technical Skills card should be collapsed

  @email
  Scenario: Open email page
    Given I open the website "https://markxcustard.github.io/"
    When I tap on my email link
    Then the email page should open

  @github
  Scenario: Redirect to GitHub profile
    Given I open the website "https://markxcustard.github.io/"
    When I tap on the GitHub button
    Then the user is directed to "https://github.com/markxcustard"

  @linkedin
  Scenario: Redirect to LinkedIn profile
    Given I open the website "https://markxcustard.github.io/"
    When I tap on the LinkedIn button
    Then the user is directed to "https://www.linkedin.com/in/mark-custard/"