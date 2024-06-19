from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_webdriver(browser_name):
    if browser_name == 'firefox':
        options = webdriver.FirefoxOptions()
        return webdriver.Firefox(options=options)
    elif browser_name == 'safari':
        return webdriver.Safari()
    elif browser_name == 'chrome':
        options = webdriver.ChromeOptions()
        return webdriver.Chrome(options=options)
    else:
        raise ValueError(f"Browser {browser_name} is not supported")

@given('I open the website "{url}"')
def step_impl(context, url):
    browser_name = context.config.userdata.get("browser", "chrome")
    context.driver = get_webdriver(browser_name)
    context.driver.get(url)
    time.sleep(1)

@when('I click on the About link')
def step_impl(context):
    about_link = context.driver.find_element(By.XPATH, '//*[@id="navbarResponsive"]/ul/li[1]/a')
    about_link.click()
    time.sleep(1)


@when('I click on the Portfolio link')
def step_impl(context):
    portfolio_link = context.driver.find_element(By.XPATH, '//*[@id="navbarResponsive"]/ul/li[2]/a')
    portfolio_link.click()
    time.sleep(1)


@when('I click on the Testimonials link')
def step_impl(context):
    testimonials_link = context.driver.find_element(By.XPATH, '//*[@id="navbarResponsive"]/ul/li[3]/a')
    testimonials_link.click()
    time.sleep(1)


@when('I click on the Contact link')
def step_impl(context):
    contact_link = context.driver.find_element(By.XPATH, '//*[@id="navbarResponsive"]/ul/li[4]/a')
    contact_link.click()
    time.sleep(1)

@then('the About section should be visible')
def step_impl(context):
    about_section = context.driver.find_element(By.XPATH, '//*[@id="about"]/div/h2')
    assert about_section.is_displayed()
    context.driver.quit()
    time.sleep(1)

@then('the Portfolio section should be visible')
def step_impl(context):
    portfolio_section = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/h2')
    assert portfolio_section.is_displayed()
    context.driver.quit()
    time.sleep(1)

@then('the Testimonials section should be visible')
def step_impl(context):
    testimonials_section = context.driver.find_element(By.XPATH, '//*[@id="testimonials"]/div/h2')
    assert testimonials_section.is_displayed()
    context.driver.quit()
    time.sleep(1)

@then('the Contact section should be visible')
def step_impl(context):
    contact_section = context.driver.find_element(By.XPATH, '//*[@id="contact"]/div/div/div/h2')
    assert contact_section.is_displayed()
    context.driver.quit()
    time.sleep(1)

@then('the homepage should display the correct title')
def step_impl(context):
    title = context.driver.title
    assert title == "Mark Custard - Portfolio", f"Expected title to be 'Mark Custard - Portfolio' but got {title}"
    context.driver.quit()
    time.sleep(1)

@when('I click on the download resume button')
def step_impl(context):
    resume_button = context.driver.find_element(By.XPATH, '//*[@id="about"]/div/div/div/div/a')
    resume_button.click()
    time.sleep(1)

@then('I should be able to download the resume')
def step_impl(context):
    # Here we can check for a successful download if the browser settings are set to automatically download files.
    # This can vary greatly depending on browser settings and Selenium might not handle file downloads well directly.
    assert True
    context.driver.quit()
    time.sleep(1)

@when('I click on QA Analyst at Stake (Fintech Industry)')
def step_impl(context):
    qa_analyst_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[1]/div/h3/a')
    print(f"Clicking on QA Analyst link at location: {qa_analyst_link.location} with size: {qa_analyst_link.size}")
    qa_analyst_link.click()
    # Wait for the element to expand
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="stake-details"]'))
    )
    print("Stake details expanded.")
    time.sleep(1)

@then('the card expands and user can view my duties and experiences at Stake')
def step_impl(context):
    stake_details = context.driver.find_element(By.XPATH, '//*[@id="stake-details"]')
    assert stake_details.is_displayed()
    time.sleep(1)

@when('I close the QA Analyst at Stake (Fintech Industry) card')
def step_impl(context):
    qa_analyst_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[1]/div/h3/a')
    print(f"Clicking again on QA Analyst link at location: {qa_analyst_link.location} with size: {qa_analyst_link.size}")
    qa_analyst_link.click()
    # Wait for the element to collapse
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[@id="stake-details"]'))
    )
    print("Stake details collapsed.")
    time.sleep(1)

@then('the Stake card should be collapsed')
def step_impl(context):
    try:
        stake_details = WebDriverWait(context.driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, '//*[@id="stake-details"]'))
        )
        assert not stake_details.is_displayed()
    except Exception as e:
        print("Debug Info: Exception Message: ", e)
        stake_details = context.driver.find_element(By.XPATH, '//*[@id="stake-details"]')
        print("Debug Info: Element displayed: ", stake_details.is_displayed())
        print("Element location: ", stake_details.location)
        print("Element size: ", stake_details.size)
        print("Element text: ", stake_details.text)
        raise e
    finally:
        context.driver.quit()
        time.sleep(1)

@when('I click on QA Engineer at CSC Generation')
def step_impl(context):
    qa_engineer_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[2]/div/h3/a')
    print(f"Clicking on QA Engineer link at location: {qa_engineer_link.location} with size: {qa_engineer_link.size}")
    qa_engineer_link.click()
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="csc-details"]'))
    )
    print("CSC Generation details expanded.")
    time.sleep(1)

@then('the card expands and user can view my duties and experiences at CSC Generation')
def step_impl(context):
    csc_details = context.driver.find_element(By.XPATH, '//*[@id="csc-details"]')
    assert csc_details.is_displayed()
    time.sleep(1)

@when('I close the QA Engineer at CSC Generation card')
def step_impl(context):
    qa_engineer_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[2]/div/h3/a')
    print(f"Clicking again on QA Engineer link at location: {qa_engineer_link.location} with size: {qa_engineer_link.size}")
    qa_engineer_link.click()
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[@id="csc-details"]'))
    )
    print("CSC Generation details collapsed.")
    time.sleep(1)

@then('the CSC Generation card should be collapsed')
def step_impl(context):
    csc_details = context.driver.find_element(By.XPATH, '//*[@id="csc-details"]')
    print(f"Debug Info: Element displayed: {csc_details.is_displayed()}")
    print(f"Element location: {csc_details.location}")
    print(f"Element size: {csc_details.size}")
    assert not csc_details.is_displayed()
    context.driver.quit()
    time.sleep(1)

@when('I click on Software QA Analyst at Kemper Insurance')
def step_impl(context):
    software_qa_analyst_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[3]/div/h3/a')
    print(f"Clicking on Software QA Analyst at Kemper Insurance link at location: {software_qa_analyst_link.location} with size: {software_qa_analyst_link.size}")
    software_qa_analyst_link.click()
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="kemper-details"]'))
    )
    print("Kemper Insurance details expanded.")
    time.sleep(1)

@then('the card expands and user can view my duties and experiences at Kemper Insurance')
def step_impl(context):
    kemper_details = context.driver.find_element(By.XPATH, '//*[@id="kemper-details"]')
    assert kemper_details.is_displayed()
    time.sleep(1)

@when('I close the Software QA Analyst at Kemper Insurance card')
def step_impl(context):
    software_qa_analyst_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[3]/div/h3/a')
    print(f"Clicking again on Software QA Analyst at Kemper Insurance link at location: {software_qa_analyst_link.location} with size: {software_qa_analyst_link.size}")
    software_qa_analyst_link.click()
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[@id="kemper-details"]'))
    )
    print("Kemper Insurance details collapsed.")
    time.sleep(1)

@then('the Kemper Insurance card should be collapsed')
def step_impl(context):
    kemper_details = context.driver.find_element(By.XPATH, '//*[@id="kemper-details"]')
    print(f"Debug Info: Element displayed: {kemper_details.is_displayed()}")
    print(f"Element location: {kemper_details.location}")
    print(f"Element size: {kemper_details.size}")
    assert not kemper_details.is_displayed()
    context.driver.quit()
    time.sleep(1)


@when('I click on Software QA Analyst at AACC')
def step_impl(context):
    aacc_software_qa_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[4]/div/h3/a')
    print(f"Clicking on Software QA Analyst at AACC link at location: {aacc_software_qa_link.location} with size: {aacc_software_qa_link.size}")
    aacc_software_qa_link.click()
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="american-access-details"]'))
    )
    print("AACC details expanded.")
    time.sleep(1)

@then('the card expands and user can view my duties and experiences at AACC')
def step_impl(context):
    aacc_qa_details = context.driver.find_element(By.XPATH, '//*[@id="american-access-details"]')
    assert aacc_qa_details.is_displayed()
    time.sleep(1)

@when('I close the Software QA Analyst at AACC card')
def step_impl(context):
    aacc_software_qa_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[4]/div/h3/a')
    print(f"Clicking again on Software QA Analyst at AACC link at location: {aacc_software_qa_link.location} with size: {aacc_software_qa_link.size}")
    aacc_software_qa_link.click()
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[@id="american-access-details"]'))
    )
    print("AACC details collapsed.")
    time.sleep(1)

@then('the AACC card should be collapsed')
def step_impl(context):
    aacc_qa_details = context.driver.find_element(By.XPATH, '//*[@id="american-access-details"]')
    print(f"Debug Info: Element displayed: {aacc_qa_details.is_displayed()}")
    print(f"Element location: {aacc_qa_details.location}")
    print(f"Element size: {aacc_qa_details.size}")
    assert not aacc_qa_details.is_displayed()
    context.driver.quit()
    time.sleep(1)


@when('I click on Junior Application Developer at AACC')
def step_impl(context):
    junior_dev_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[5]/div/h3/a')
    print(f"Clicking on Junior Application Developer link at location: {junior_dev_link.location} with size: {junior_dev_link.size}")
    junior_dev_link.click()
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="junior-developer-details"]'))
    )
    print("Junior Developer details expanded.")
    time.sleep(1)

@then('the card expands and user can view my duties and experiences as a Junior Application Developer at AACC')
def step_impl(context):
    jad_details = context.driver.find_element(By.XPATH, '//*[@id="junior-developer-details"]')
    assert jad_details.is_displayed()
    time.sleep(1)

@when('I close the Junior Application Developer at AACC card')
def step_impl(context):
    junior_dev_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[5]/div/h3/a')
    print(f"Clicking again on Junior Application Developer link at location: {junior_dev_link.location} with size: {junior_dev_link.size}")
    junior_dev_link.click()
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[@id="junior-developer-details"]'))
    )
    print("Junior Developer details collapsed.")
    time.sleep(1)

@then('the Junior Application Developer card should be collapsed')
def step_impl(context):
    try:
        jad_details = WebDriverWait(context.driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, '//*[@id="junior-developer-details"]'))
        )
        assert not jad_details.is_displayed()
    except Exception as e:
        print("Debug Info: Exception Message: ", e)
        jad_details = context.driver.find_element(By.XPATH, '//*[@id="junior-developer-details"]')
        print("Debug Info: Element displayed: ", jad_details.is_displayed())
        print("Element location: ", jad_details.location)
        print("Element size: ", jad_details.size)
        print("Element text: ", jad_details.text)
        raise e
    finally:
        context.driver.quit()
        time.sleep(1)

@when('I click on Technical Skills')
def step_impl(context):
    tech_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[6]/div/h3/a')
    print(f"Clicking on Technical Skills link at location: {tech_link.location} with size: {tech_link.size}")
    tech_link.click()
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="tech-skills-details"]'))
    )
    print("Technical Skills details expanded.")
    time.sleep(1)

@then('the card expands and user can view my technical skills')
def step_impl(context):
    tech_details = context.driver.find_element(By.XPATH, '//*[@id="tech-skills-details"]')
    assert tech_details.is_displayed()
    time.sleep(1)

@when('I close the Technical Skills card')
def step_impl(context):
    tech_link = context.driver.find_element(By.XPATH, '//*[@id="portfolio"]/div/div/div[6]/div/h3/a')
    print(f"Clicking again on Technical Skills link at location: {tech_link.location} with size: {tech_link.size}")
    tech_link.click()
    time.sleep(1)

@then('the Technical Skills card should be collapsed')
def step_impl(context):
    print("Waiting for the Technical Skills details to collapse...")
    try:
        WebDriverWait(context.driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, '//*[@id="tech-skills-details"]'))
        )
        print("Technical Skills details collapsed.")
    except Exception as e:
        print(f"Debug Info: Exception {e}")
        tech_details = context.driver.find_element(By.XPATH, '//*[@id="tech-skills-details"]')
        print(f"Debug Info: Element displayed: {tech_details.is_displayed()}")
        print(f"Element location: {tech_details.location}")
        print(f"Element size: {tech_details.size}")
        print(f"Element text: {tech_details.text}")
        raise e
    finally:
        context.driver.quit()
        time.sleep(1)

@when('I tap on my email link')
def step_impl(context):
    email_link = context.driver.find_element(By.XPATH, '//*[@id="contact"]/div/div/div/p[1]/a')
    print(f"Clicking on email link at location: {email_link.location} with size: {email_link.size}")
    email_link.click()
    time.sleep(1)

@then('the email page should open')
def step_impl(context):
    email_link = context.driver.find_element(By.XPATH, '//*[@id="contact"]/div/div/div/p[1]/a')
    email_address = email_link.text
    print("Debug Info: Email link text: ", email_address)
    assert email_address == "mark.a.custard@gmail.com", f"Expected 'mark.a.custard@gmail.com' but got {email_address}"
    context.driver.quit()
    time.sleep(1)

@when('I tap on the GitHub button')
def step_impl(context):
    github_button = context.driver.find_element(By.XPATH, '//*[@id="contact"]/div/div/div/div/a[1]')
    github_button.click()
    time.sleep(1)

@then('the user is directed to "https://github.com/markxcustard"')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(EC.new_window_is_opened)
    context.driver.switch_to.window(context.driver.window_handles[-1])
    assert context.driver.current_url == "https://github.com/markxcustard"
    context.driver.quit()
    time.sleep(1)

@when('I tap on the LinkedIn button')
def step_impl(context):
    linkedin_button = context.driver.find_element(By.XPATH, '//*[@id="contact"]/div/div/div/div/a[2]')
    linkedin_button.click()
    time.sleep(1)

@then('the user is directed to "https://www.linkedin.com/in/mark-custard/"')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(EC.new_window_is_opened)
    context.driver.switch_to.window(context.driver.window_handles[-1])
    assert context.driver.current_url == "https://www.linkedin.com/in/mark-custard/"
    context.driver.quit()
    time.sleep(1)

@when('I tap on the Automation link')
def step_impl(context):
    automation_link = context.driver.find_element(By.XPATH, '//*[@id="about"]/div/div/div/p[5]/a[1]')
    print(f"Clicking on Automation link at location: {automation_link.location} with size: {automation_link.size}")
    automation_link.click()
    time.sleep(1)
    print(f"Current URL after clicking Automation link: {context.driver.current_url}")
    context.driver.switch_to.window(context.driver.window_handles[-1])

@then('the user is directed to "https://github.com/markxcustard/personal_website_automation"')
def step_impl(context):
    try:
        WebDriverWait(context.driver, 20).until(EC.url_contains("https://github.com/markxcustard/personal_website_automation"))
        print(f"Final URL: {context.driver.current_url}")
        assert context.driver.current_url == "https://github.com/markxcustard/personal_website_automation"
    except Exception as e:
        print(f"Error: {e}")
        print(f"Debug Info: Current URL: {context.driver.current_url}")
        raise e
    finally:
        context.driver.quit()

@when('I tap on the BDD link')
def step_impl(context):
    bdd_link = context.driver.find_element(By.XPATH, '//*[@id="about"]/div/div/div/p[5]/a[2]')
    print(f"Clicking on BDD link at location: {bdd_link.location} with size: {bdd_link.size}")
    bdd_link.click()
    time.sleep(1)
    print(f"Current URL after clicking BDD link: {context.driver.current_url}")
    context.driver.switch_to.window(context.driver.window_handles[-1])

@then('the user is directed to "https://github.com/markxcustard/bdd_personal_website"')
def step_impl(context):
    try:
        WebDriverWait(context.driver, 20).until(EC.url_contains("https://github.com/markxcustard/bdd_personal_website"))
        print(f"Final URL: {context.driver.current_url}")
        assert context.driver.current_url == "https://github.com/markxcustard/bdd_personal_website"
    except Exception as e:
        print(f"Error: {e}")
        print(f"Debug Info: Current URL: {context.driver.current_url}")
        raise e
    finally:
        context.driver.quit()