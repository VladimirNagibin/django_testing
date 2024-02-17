from http import HTTPStatus

from .test_base import TestBase


class TestRoutes(TestBase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URLS_FOR_TESTS = (
            cls.URL_HOME,
            cls.URL_NOTES_LIST,
            cls.URL_NOTES_ADD,
            cls.URL_NOTES_SUCCESS,
            cls.URL_NOTES_EDIT,
            cls.URL_NOTES_DETAIL,
            cls.URL_NOTES_DELETE,
            cls.URL_LOGIN,
            cls.URL_SIGNUP,
            cls.URL_LOGOUT,
        )
        cls.URLS_UPDATE_NOTES = [
            cls.URL_NOTES_EDIT,
            cls.URL_NOTES_DETAIL,
            cls.URL_NOTES_DELETE,
        ]
        cls.URLS_FOR_ANONYMOUS = [
            cls.URL_HOME,
            cls.URL_LOGIN,
            cls.URL_LOGOUT,
            cls.URL_SIGNUP,
        ]

    def test_pages_availability_for_auth_user(self):
        """Проверка доступности страниц для пользователя - автора заметки."""
        for name in self.URLS_FOR_TESTS:
            with self.subTest(name=name):
                response = self.author_client.get(name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_reader_user(self):
        """Проверка для аутентифицированного пользователя - не автора заметки.
        Доступность главной страницы, страницы со списком заметок,
        страниц успешного добавления и добавления новой заметки, регистрации
        пользователей, входа в учётную запись и выхода из неё.
        При переходе на страницы отдельной заметки, удаления и редактирования
        заметки другого автора возвращается ошибка 404.
        """
        for name in self.URLS_FOR_TESTS:
            with self.subTest(name=name):
                if name in self.URLS_UPDATE_NOTES:
                    status = HTTPStatus.NOT_FOUND
                else:
                    status = HTTPStatus.OK
                response = self.reader_client.get(name)
                self.assertEqual(response.status_code, status)

    def test_pages_availability_for_anonymous_user(self):
        """Проверка для анонимного пользователя.
        Доступность главной страницы, страницы регистрации пользователей,
        входа в учётную запись и выхода из неё.
        При переходе на страницу со списком заметок, страниц успешного
        добавления и добавления новой заметки,страницу отдельной заметки,
        удаления и редактирования заметки происходит перенаправление на
        страницу логина.
        """
        for name in self.URLS_FOR_TESTS:
            with self.subTest(name=name):
                response = self.client.get(name)
                if name in self.URLS_FOR_ANONYMOUS:
                    self.assertEqual(response.status_code, HTTPStatus.OK)
                else:
                    self.assertRedirects(response,
                                         f'{self.URL_LOGIN}?next={name}')
