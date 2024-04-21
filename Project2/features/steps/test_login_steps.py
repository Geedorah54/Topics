from behave import given, when, then
from selenium import webdriver

@given('I am on the Google search page')
def step_impl(context):
    context.browser = webdriver.Chrome()
    context.browser.get("http://www.google.com")

@when('I search for "puppies"')
def step_impl(context):
    search_box = context.browser.find_element_by_name('q')
    search_box.send_keys('puppies')
    search_box.submit()

@then('the page title should contain "puppies"')
def step_impl(context):
    assert 'puppies' in context.browser.title
    context.browser.quit()
