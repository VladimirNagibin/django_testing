from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='User')
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

    def test_notes_list_for_different_users(self):
        for user_client, note_in_list in (
            (self.reader_client, False),
            (self.author_client, True)
        ):
            response = user_client.get(reverse('notes:list'))
            self.assertTrue(
                (self.note in response.context['object_list']) is note_in_list
            )

    def test_pages_contains_form(self):
        for name, args in (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        ):
            response = self.author_client.get(reverse(name, args=args))
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)
