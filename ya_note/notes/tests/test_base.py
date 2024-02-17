from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestBase(TestCase):

    SLUG = 'slug'
    TITLE = 'Title'
    TEXT = 'Text'
    NEW_SLUG = 'new_slug'
    NEW_TITLE = 'New title'
    NEW_TEXT = 'New text'
    URL_HOME = reverse('notes:home')
    URL_LOGIN = reverse('users:login')
    URL_LOGOUT = reverse('users:logout')
    URL_SIGNUP = reverse('users:signup')
    URL_NOTES_LIST = reverse('notes:list')
    URL_NOTES_ADD = reverse('notes:add')
    URL_NOTES_SUCCESS = reverse('notes:success')
    URL_NOTES_EDIT = reverse('notes:edit', args=(SLUG,))
    URL_NOTES_DETAIL = reverse('notes:detail', args=(SLUG,))
    URL_NOTES_DELETE = reverse('notes:delete', args=(SLUG,))

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.reader = User.objects.create(username='Reader')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title=cls.TITLE,
            text=cls.TEXT,
            author=cls.author,
            slug=cls.SLUG
        )
        cls.form_data = {'title': cls.NEW_TITLE,
                         'text': cls.NEW_TEXT,
                         'slug': cls.NEW_SLUG}
