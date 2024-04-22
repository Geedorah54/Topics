Feature: Google Searching
  Scenario: Simple Google Search
    Given I am on the Google search page
    When I search for "puppies"
    Then the page title should contain "puppies"
