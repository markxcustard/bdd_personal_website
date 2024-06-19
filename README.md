# bdd_personal_website

# BDD Testing Suite for Personal Website

This project uses BDD (Behavior-Driven Development) to test the functionality of my personal website using Python, Selenium, and Behave.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/markxcustard/bdd_personal_website.git
   cd bdd_personal_website
Install dependencies:

pip install -r requirements.txt
Ensure you have the required web drivers (ChromeDriver, GeckoDriver for Firefox, and SafariDriver) installed and properly configured.

Running Tests
To run the tests with a specific browser, use the --define browser=<browser_name> option.

Example:

behave --define browser=chrome
Features Tested
Navigation links
Portfolio section interactions
Contact section interactions
External links (GitHub, LinkedIn)
Email link
Project Structure
features/navigation.feature: Contains the Gherkin scenarios for testing navigation.
features/steps/steps.py: Contains the step definitions for the scenarios.
GitHub Repository
The repository can be found at: https://github.com/markxcustard/bdd_personal_website
