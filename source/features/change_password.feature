Feature: Редактировать профиль
  Scenario: Успешное редактирование профилья
    Given Я захожу на страницу входа
    When Я ввожу "7771112233" в поле "username"
    And Я ввожу "TestPassword123" в поле "password"
    And Я нажимаю на кнопку "Войти"
    And Я должен переместиться на главную страницу
    And Я захожу на страницу Изменить пароль
    And Я ввожу "TestPassword123" в поле "old_password"
    And Я ввожу "NewPassword123" в поле "password"
    And Я ввожу "NewPassword123" в поле "password_confirm"
    And Я нажимаю на кнопку "Изменить"
    Then Я должен переместиться на страницу профиль