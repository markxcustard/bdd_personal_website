@mobile
Feature: Mobile layout
  As a visitor on a phone
  I want the navigation and content to work at phone width
  So that the site is usable away from a desktop

  # Below the xl breakpoint the template slides the sidebar off-canvas with
  # `.header { left: -100% }` and brings it back by adding `.header-show`. It is
  # never display:none, so asserting on visibility would pass whether the menu
  # opened or not. These scenarios assert the state class and the real position.

  Background:
    Given I am on the portfolio home page

  Scenario: The sidebar starts collapsed off-canvas
    Then the navigation toggle should be offered
    And the sidebar should be off-canvas

  Scenario: Tapping the toggle slides the sidebar in
    When I tap the navigation toggle
    Then the sidebar should be on screen
    And the menu should list 8 links

  Scenario: Tapping the toggle twice slides the sidebar away again
    When I tap the navigation toggle
    And I tap the navigation toggle
    Then the sidebar should be off-canvas

  Scenario: The toggle reports its state to assistive technology
    Then the navigation toggle should report itself as collapsed
    When I tap the navigation toggle
    Then the navigation toggle should report itself as expanded

  Scenario: The page does not scroll sideways
    When I open the portfolio grid
    Then the page should not scroll horizontally
