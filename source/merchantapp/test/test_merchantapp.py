from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command


class TestMerchantPermissions(TestCase):
    def setUP(self):
        call_command("loaddata", "fixtures/tests/dump.json")
        self.client = Client()

    def test_permissions_home(self):
        response = self.client.get("/ru/")
        self.assertEqual(302, response.status_code)

    def test_permissions_programs(self):
        response = self.client.get("/ru/programs/")
        self.assertEqual(302, response.status_code)

    def test_permissions_programs_create(self):
        response = self.client.get("/ru/programs/create/")
        self.assertEqual(302, response.status_code)

    def test_permissions_branches(self):
        response = self.client.get("/ru/branches/")
        self.assertEqual(302, response.status_code)

    def test_permissions_branches_create(self):
        response = self.client.get("/ru/branches/create/")
        self.assertEqual(302, response.status_code)

    def test_permissions_employees(self):
        response = self.client.get("/ru/employees/")
        self.assertEqual(302, response.status_code)

    # Нужно исправить баг в пермишенах
    def test_permissions_employees_create(self):
        response = self.client.get("/ru/employees/add/")
        self.assertEqual(302, response.status_code)

    def test_permissions_customers(self):
        response = self.client.get("/ru/customers/")
        self.assertEqual(302, response.status_code)


class TestMerchantUrlExists(TestCase):
    def setUp(self):
        call_command("loaddata", "fixtures/tests/dump.json")
        self.client = Client()
        self.client.post('/ru/accounts/login/?next=/ru/', {'username': '77777777777', 'password': 'admin'})

    def test_url_home(self):
        response = self.client.get("/ru/")
        self.assertEqual(200, response.status_code)

    def test_url_programs(self):
        response = self.client.get("/ru/programs/")
        self.assertEqual(200, response.status_code)

    def test_url_exists(self):
        response = self.client.get("/ru/accounts/login/?next=/ru/")
        self.assertEqual(200, response.status_code)

    def test_url_programs_create(self):
        response = self.client.get("/ru/programs/create/")
        self.assertEqual(200, response.status_code)

    def test_url_branches(self):
        response = self.client.get("/ru/branches/")
        self.assertEqual(200, response.status_code)

    def test_url_branches_create(self):
        response = self.client.get("/ru/branches/create/")
        self.assertEqual(200, response.status_code)

    def test_purl_employees(self):
        response = self.client.get("/ru/employees/")
        self.assertEqual(200, response.status_code)

    def test_url_employees_create(self):
        response = self.client.get("/ru/employees/add/")
        self.assertEqual(200, response.status_code)

    def test_url_customers(self):
        response = self.client.get("/ru/customers/")
        self.assertEqual(200, response.status_code)


class TestMerchantAccessByName(TestCase):
    def setUp(self):
        call_command("loaddata", "fixtures/tests/dump.json")
        self.client = Client()
        self.client.post('/ru/accounts/login/?next=/ru/', {'username': '77777777777', 'password': 'admin'})

    def test_url_access_by_name_index(self):
        response = self.client.get(reverse('merchantapp:merchant_index'))
        self.assertEqual(200, response.status_code)

    def test_url_access_by_name_programs(self):
        response = self.client.get(reverse('merchantapp:programs'))
        self.assertEqual(200, response.status_code)

    def test_url_access_by_name_programs_create(self):
        response = self.client.get(reverse('merchantapp:program_create'))
        self.assertEqual(200, response.status_code)

    def test_url_access_by_name_branches(self):
        response = self.client.get(reverse('merchantapp:branches'))
        self.assertEqual(200, response.status_code)

    def test_url_access_by_name_branches_create(self):
        response = self.client.get(reverse('merchantapp:branch_create'))
        self.assertEqual(200, response.status_code)

    def test_url_access_by_name_employees(self):
        response = self.client.get(reverse('merchantapp:employees_list'))
        self.assertEqual(200, response.status_code)

    def test_url_access_by_name_employees_add(self):
        response = self.client.get(reverse('merchantapp:employee_add'))
        self.assertEqual(200, response.status_code)

    def test_url_access_by_name_customers(self):
        response = self.client.get(reverse('merchantapp:customers'))
        self.assertEqual(200, response.status_code)


class TestRendersCorrectTemplate(TestCase):
    def setUp(self):
        call_command("loaddata", "fixtures/tests/dump.json")
        self.client = Client()
        self.client.post('/ru/accounts/login/?next=/ru/', {'username': '77777777777', 'password': 'admin'})

    def test_index(self):
        response = self.client.get(reverse('merchantapp:merchant_index'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "index.html")

    def test_programs(self):
        response = self.client.get(reverse("merchantapp:programs"))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "program.html")

    def test_programs_create(self):
        response = self.client.get(reverse('merchantapp:program_create'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "program_create.html")

    def test_branches(self):
        response = self.client.get(reverse('merchantapp:branches'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "branches/branch_list.html")

    def test_branches_create(self):
        response = self.client.get(reverse('merchantapp:branch_create'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "branches/branch_create.html")

    def test_employees(self):
        response = self.client.get(reverse('merchantapp:employees_list'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "employees/employees_list.html")

    def test_employees_add(self):
        response = self.client.get(reverse('merchantapp:employee_add'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "employees/employee_add.html")

    def test_customers(self):
        response = self.client.get(reverse('merchantapp:customers'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "customers/customers_list.html")
