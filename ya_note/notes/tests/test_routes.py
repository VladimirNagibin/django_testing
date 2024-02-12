from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    URLS_NOTES_WITH_SLUG = ('notes:edit', 'notes:detail', 'notes:delete')
    URLS_NOTES = ('notes:list', 'notes:add', 'notes:success')
    URLS_FOR_ANONYMOUS = ('notes:home',
                          'users:login',
                          'users:logout',
                          'users:signup')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.reader = User.objects.create(username='Reader')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Title',
            text='Text',
            author=cls.author,
            slug='slug'
        )

    def test_pages_availability_for_anonymous_user(self):
        for name in self.URLS_FOR_ANONYMOUS:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        for name in self.URLS_NOTES:
            with self.subTest(name=name):
                response = self.reader_client.get(reverse(name))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        for user_client, exp_status in (
            (self.reader_client, HTTPStatus.NOT_FOUND),
            (self.author_client, HTTPStatus.OK)
        ):
            for name in self.URLS_NOTES_WITH_SLUG:
                with self.subTest(name=name, user_client=user_client):
                    response = user_client.get(reverse(name,
                                                       args=(self.note.slug,)))
                    self.assertEqual(response.status_code, exp_status)

    def test_redirects(self):
        urls = tuple(
            zip(self.URLS_NOTES_WITH_SLUG,
                ((self.note.slug,),) * len(self.URLS_NOTES_WITH_SLUG))
        )
        urls += tuple(zip(self.URLS_NOTES,
                          (None,) * len(self.URLS_NOTES)))
        login_url = reverse('users:login')
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                self.assertRedirects(self.client.get(url), redirect_url)
