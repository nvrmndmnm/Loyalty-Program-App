# from behave import *
# import time
#
#
# @given("Я захожу на страницу регистраций")
# def step_impl(context):
#     context.browser.get(f"{context.base_url}/accounts/create/")
#     time.sleep(1)
#
#
# @when('Я ввожу "{text}" в поле "{field_name}"')
# def step_impl(context, text, field_name):
#     context.browser.find_element_by_name(field_name).send_keys(text)
#     time.sleep(1)
#
#
# @step('Я нажимаю на кнопку "{button_text}"')
# def step_impl(context, button_text):
#     context.browser.find_element_by_xpath(f"//button[text()='{button_text}']").click()
#     time.sleep(1)
#
#
# @step("Я должен переместиться на страницу логина")
# def step_impl(context):
#     print(f"{context.browser.current_url} == {context.base_url}")
#     assert context.browser.current_url == context.base_url + "/ru/accounts/login/"
#     time.sleep(1)
#
#
# @then("Я должен переместиться на главную страницу")
# def step_impl(context):
#     print(f"{context.browser.current_url} == {context.base_url}")
#     assert context.browser.current_url == context.base_url + "/ru/"
#     time.sleep(1)
#
# # Чтобы запустить тесты надо прописать команду ./manage.py behave
