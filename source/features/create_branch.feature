Feature: Создать заведение
  Scenario: Успешное создание заведение
    Given Я захожу на страницу входа
    When Я ввожу "7771112233" в поле "username"
    And Я ввожу "TestPassword123" в поле "password"
    And Я нажимаю на кнопку "Войти"
    And Я должен переместиться на главную страницу
    And Я нажимаю на ссылку "Заведения"
    And Я должен переместиться на страницу Заведений
    And Я нажимаю на ссылку "Добавить точку"
    And Я должен переместиться на страницу Создать заведений
    And Я ввожу "1" в поле "code"
    And Я ввожу "TestName" в поле "name"
    And Я выбираю "merchant" в поле "merchant"
    And Я ввожу "TestDescription" в поле "description"
    And Я ввожу "TestStreet" в поле "street"
    And Я ввожу "TestBuilding" в поле "building"
    And Я ввожу "TestOffice" в поле "apartment"
    And Я ввожу "TestCity" в поле "city"
    And Я ввожу "https://2gis.kz/almaty" в поле "link2gis"
    And Я ввожу "123" в поле "latitude"
    And Я ввожу "123" в поле "longitude"
    And Я нажимаю на кнопку "Отправить"
    Then Я должен переместиться на страницу Заведений