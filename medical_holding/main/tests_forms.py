from django.test import TestCase
from main import forms


class MyUserCreationFormTest(TestCase):
    def test_valid_values(self):
        # arrange
        data = {
            'username': 'r1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wr'
                        'tt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrtt1wrt',
            'email': '2qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq@qq.ru',
            'password1': 'MhW4JPx&e82pfdGVRK%7cDvan3#UbwyYg$mN6LTrkzjCqA9u!BMhW4JPx&e82pfdGVRK%7cDvan3#UbwyYg$mN6LTrkzj'
                         'CqA9u!BMhW4JPx&e82pfdGVRK%7cDvan3#UbwyYg$mN6LTrkzjCqA9u!B',
            'password2': 'MhW4JPx&e82pfdGVRK%7cDvan3#UbwyYg$mN6LTrkzjCqA9u!BMhW4JPx&e82pfdGVRK%7cDvan3#UbwyYg$mN6LTrkzj'
                         'CqA9u!BMhW4JPx&e82pfdGVRK%7cDvan3#UbwyYg$mN6LTrkzjCqA9u!B',
        }

        # act
        form = forms.MyUserCreationForm(data=data)

        # assert
        self.assertTrue(form.is_valid(), f'Data is invalid, but expected valid data. Errors: {form.errors.as_text()}')

    def test_invalid_values(self):
        # arrange
        data = {
            'username': '12',
            'email': 'q@qq.r',
            'password1': '123456',
            'password2': '123456q',
        }
        expected_amount_errors = 3

        # act
        form = forms.MyUserCreationForm(data=data)
        amount_errors = len(form.errors)

        # assert
        self.assertFalse(form.is_valid(), 'Data is valid, but expected invalid data')
        self.assertEqual(amount_errors, expected_amount_errors,
                         f'Expected {expected_amount_errors} validation errors, but found a {amount_errors} number')


class ChangeUserProfileFormTest(TestCase):
    def test_valid_values(self):
        # arrange
        data = {
            'about': '',
            'first_name': '',
            'last_name': '',
            'gender': 'N',
            'birthday': '01.01.2005',
            'phone': '567893',
        }

        # act
        form = forms.ChangeUserProfileForm(data=data)

        # assert
        self.assertTrue(form.is_valid(), f'Data is invalid, but expected valid data. Errors: {form.errors.as_text()}')

    def test_invalid_values(self):
        # arrange
        data = {
            'about': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',
            'first_name': 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
                          'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
                          'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww',
            'last_name': 'ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt'
                         'ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt'
                         'ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt',
            'gender': 'Q',
            'birthday': '01.01.-2005',
            'phone': '56789',
        }
        expected_amount_errors = 6

        # act
        form = forms.ChangeUserProfileForm(data=data)
        amount_errors = len(form.errors)

        # assert
        self.assertFalse(form.is_valid(), 'Data is valid, but expected invalid data')
        self.assertEqual(amount_errors, expected_amount_errors,
                         f'Expected {expected_amount_errors} validation errors, but found a {amount_errors} number')


class OrganizationFormTest(TestCase):
    def test_valid_values(self):
        # arrange
        data = {
            'name': 'org',
            'about': 'q',
            'site': '',
            'inn': '12345678901',
        }

        # act
        form = forms.OrganizationForm(data=data)

        # assert
        self.assertTrue(form.is_valid(), f'Data is invalid, but expected valid data. Errors: {form.errors.as_text()}')

    def test_invalid_values(self):
        # arrange
        data = {
            'name': '',
            'about': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',
            'site': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                     'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',
            'inn': '123456789a',
        }
        expected_amount_errors = 4

        # act
        form = forms.OrganizationForm(data=data)
        amount_errors = len(form.errors)

        # assert
        self.assertFalse(form.is_valid(), 'Data is valid, but expected invalid data')
        self.assertEqual(amount_errors, expected_amount_errors,
                         f'Expected {expected_amount_errors} validation errors, but found a {amount_errors} number')


class BranchOrganizationFormTest(TestCase):
    def test_valid_values(self):
        # arrange
        data = {
            'street': 'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
                      'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
                      'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
                      'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
                      'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
                      'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu',
            'house': 1,
            'phone': '789653',
        }

        # act
        form = forms.BranchOrganizationForm(data=data)

        # assert
        self.assertTrue(form.is_valid(), f'Data is invalid, but expected valid data. Errors: {form.errors.as_text()}')

    def test_invalid_values(self):
        # arrange
        data = {
            'street': 'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
                      'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
                      'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
                      'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
                      'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu'
                      'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu',
            'house': 0,
            'phone': '78965378965378965',
        }
        expected_amount_errors = 3

        # act
        form = forms.BranchOrganizationForm(data=data)
        amount_errors = len(form.errors)

        # assert
        self.assertFalse(form.is_valid(), 'Data is valid, but expected invalid data')
        self.assertEqual(amount_errors, expected_amount_errors,
                         f'Expected {expected_amount_errors} validation errors, but found a {amount_errors} number')


class EmployeeOrganizationFormTest(TestCase):
    def test_valid_values(self):
        # arrange
        data = {
            'number_in_med_registry': '99',
            'experience_month': 0,
            'first_name': 'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                          'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                          'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw',
            'last_name': 'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                         'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                         'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw',
            'middle_name': 'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                           'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                           'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw',
            'qualification': 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
                             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
                             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
                             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
                             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
                             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
            'gender': 'M',
        }

        # act
        form = forms.EmployeeOrganizationForm(data=data)

        # assert
        self.assertTrue(form.is_valid(), f'Data is invalid, but expected valid data. Errors: {form.errors.as_text()}')

    def test_invalid_values(self):
        # arrange
        data = {
            'number_in_med_registry': '',
            'experience_month': 32_769,
            'first_name': 'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                          'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                          'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwe',
            'last_name': 'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                         'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                         'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwe',
            'middle_name': 'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                           'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqw'
                           'qwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwqwe',
            'qualification': 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
                             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
                             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
                             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
                             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
                             'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrree',
            'gender': 'F',
        }
        expected_amount_errors = 7

        # act
        form = forms.EmployeeOrganizationForm(data=data)
        amount_errors = len(form.errors)

        # assert
        self.assertFalse(form.is_valid(), 'Data is valid, but expected invalid data')
        self.assertEqual(amount_errors, expected_amount_errors,
                         f'Expected {expected_amount_errors} validation errors, but found a {amount_errors} number')


class RatingServiceFormTest(TestCase):
    def test_valid_values(self):
        # arrange
        data = {
            'grade': '0.01',
        }

        # act
        form = forms.RatingServiceForm(data=data)

        # assert
        self.assertTrue(form.is_valid(), f'Data is invalid, but expected valid data. Errors: {form.errors.as_text()}')

    def test_invalid_values(self):
        # arrange
        data = {
            'grade': '5.01',
        }
        expected_amount_errors = 1

        # act
        form = forms.RatingServiceForm(data=data)
        amount_errors = len(form.errors)

        # assert
        self.assertFalse(form.is_valid(), 'Data is valid, but expected invalid data')
        self.assertEqual(amount_errors, expected_amount_errors,
                         f'Expected {expected_amount_errors} validation errors, but found a {amount_errors} number')


class CommentAboutServiceFormTest(TestCase):
    def test_valid_values(self):
        # arrange
        data = {
            'text': 'hi',
        }

        # act
        form = forms.CommentAboutServiceForm(data=data)

        # assert
        self.assertTrue(form.is_valid(), f'Data is invalid, but expected valid data. Errors: {form.errors.as_text()}')

    def test_invalid_values(self):
        # arrange
        data = {
            'text': '',
        }
        expected_amount_errors = 1

        # act
        form = forms.CommentAboutServiceForm(data=data)
        amount_errors = len(form.errors)

        # assert
        self.assertFalse(form.is_valid(), 'Data is valid, but expected invalid data')
        self.assertEqual(amount_errors, expected_amount_errors,
                         f'Expected {expected_amount_errors} validation errors, but found a {amount_errors} number')
