from http import HTTPStatus

from pytils.translit import slugify

from .test_routes import TestBase
from notes.forms import WARNING
from notes.models import Note


class TestLogic(TestBase):

    def test_user_can_create_note(self):
        """Проверка что залогиненный пользователь может создать заметку."""
        Note.objects.all().delete()
        response = self.author_client.post(self.URL_NOTES_ADD,
                                           data=self.form_data)
        self.assertRedirects(response, self.URL_NOTES_SUCCESS)
        self.assertEqual(Note.objects.count(), 1)
        note_new = Note.objects.get(slug=self.NEW_SLUG)
        self.assertEqual(note_new.title, self.NEW_TITLE)
        self.assertEqual(note_new.text, self.NEW_TEXT)
        self.assertEqual(note_new.author, self.author)
        self.assertEqual(note_new.slug, self.NEW_SLUG)

    def test_anonymous_user_cant_create_note(self):
        """Проверка анонимный пользователь не может создать заметку."""
        Note.objects.all().delete()
        response = self.client.post(self.URL_NOTES_ADD, data=self.form_data)
        self.assertRedirects(response,
                             f'{self.URL_LOGIN}?next={self.URL_NOTES_ADD}')
        self.assertEqual(Note.objects.count(), 0)

    def test_not_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        note_count = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(self.URL_NOTES_ADD,
                                           data=self.form_data)
        self.assertFormError(response,
                             'form',
                             'slug',
                             errors=(self.note.slug + WARNING))
        self.assertEqual(Note.objects.count(), note_count)

    def test_empty_slug(self):
        """Если при создании заметки не заполнен slug, то он формируется
        автоматически, с помощью функции pytils.translit.slugify.
        """
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.author_client.post(self.URL_NOTES_ADD,
                                           data=self.form_data)
        self.assertRedirects(response, self.URL_NOTES_SUCCESS)
        self.assertEqual(Note.objects.count(), 1)
        note_new = Note.objects.get(title=self.NEW_TITLE)
        self.assertEqual(note_new.slug, slugify(self.NEW_TITLE))
        self.assertEqual(note_new.title, self.NEW_TITLE)
        self.assertEqual(note_new.text, self.NEW_TEXT)
        self.assertEqual(note_new.author, self.author)

    def test_author_can_edit_note(self):
        """Пользователь может редактировать свои заметки."""
        self.assertEqual(Note.objects.count(), 1)
        response = self.author_client.post(self.URL_NOTES_EDIT, self.form_data)
        self.assertRedirects(response, self.URL_NOTES_SUCCESS)
        note = Note.objects.get(slug=self.NEW_SLUG)
        self.assertEqual(note.title, self.NEW_TITLE)
        self.assertEqual(note.text, self.NEW_TEXT)
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, self.NEW_SLUG)

    def test_other_user_cant_edit_note(self):
        """Пользователь не может редактировать чужие заметки."""
        self.assertEqual(Note.objects.count(), 1)
        response = self.reader_client.post(self.URL_NOTES_EDIT, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(slug=self.SLUG)
        self.assertEqual(note.title, self.TITLE)
        self.assertEqual(note.text, self.TEXT)
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.slug, self.SLUG)

    def test_author_can_delete_note(self):
        """Пользователь может удалять свои заметки."""
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        response = self.author_client.post(self.URL_NOTES_DELETE)
        self.assertRedirects(response, self.URL_NOTES_SUCCESS)
        self.assertEqual(Note.objects.count(), note_count - 1)

    def test_other_user_cant_delete_note(self):
        """Пользователь не может удалять чужие заметки."""
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        response = self.reader_client.post(self.URL_NOTES_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), note_count)
