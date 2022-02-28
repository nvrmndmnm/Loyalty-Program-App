from behave import *
import time
from accounts.factories.user_factory import UserFactory, MerchantFactory, CustomUserFactory


@given("Я захожу на страницу входа")
def step_impl(context):
    user = CustomUserFactory(phone="7079999999", is_superuser=False)
    user.set_password("TestPass123")
    user.save()
    admin = UserFactory(phone="7771112233", is_superuser=True)
    admin.set_password("TestPassword123")
    admin.save()
    merchant = MerchantFactory(name="test_M", code="1", category="test_C")
    # merchant.director.add(user.pk)
    # print(merchant.director)
    merchant.director.set(user.pk)
    merchant.save()
    print(f"mer: {merchant.id}")
    context.browser.get(f"{context.base_url}/accounts/login/")
    time.sleep(1)


@when('Я ввожу "{text}" в поле "{field_name}"')
def step_impl(context, text, field_name):
    context.browser.find_element_by_name(field_name).send_keys(text)
    time.sleep(1)


@step('Я нажимаю на ссылку "{link_text}"')
def step_impl(context, link_text):
    context.browser.find_element_by_xpath(f"//a[text()='{link_text}']").click()
    time.sleep(1)


@step('Я выбираю "merchant" в поле "merchant"')
def step_impl(context):
    context.browser.find_element_by_name("merchant").click()
    context.browser.find_element_by_xpath("//option[text()='merchant']").click()
    time.sleep(1)


@step('Я нажимаю на кнопку "{button_text}"')
def step_impl(context, button_text):
    context.browser.find_element_by_xpath(f"//button[text()='{button_text}']").click()
    time.sleep(1)


@step("Я должен переместиться на главную страницу")
def step_impl(context):
    assert context.browser.current_url == context.base_url + "/ru/"
    time.sleep(1)


@step("Я должен переместиться на страницу Заведений")
def step_impl(context):
    print(f"{context.browser.current_url} == {context.base_url}")
    assert context.browser.current_url == context.base_url + "/ru/branches/"
    time.sleep(1)


@step("Я должен переместиться на страницу Создать заведений")
def step_impl(context):
    print(f"{context.browser.current_url} == {context.base_url}")
    assert context.browser.current_url == context.base_url + "/ru/branches/create/"
    time.sleep(1)


# Чтобы запустить тесты надо прописать команду ./manage.py behave
