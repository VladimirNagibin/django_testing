from .test_base import TestBase
from notes.forms import NoteForm


class TestContent(TestBase):

    def test_note_in_list_for_author(self):
        """Проверка что отдельная заметка передаётся на страницу со списком
        заметок в списке object_list, в словаре context
        """
        response = self.author_client.get(self.URL_NOTES_LIST)
        object_list = response.context['object_list']
        self.assertEqual(object_list.count(), 1)
        note = set(object_list).pop()
        self.assertEqual(note.author, self.author)
        self.assertEqual(note.title, self.TITLE)
        self.assertEqual(note.text, self.TEXT)
        self.assertEqual(note.slug, self.SLUG)

    def test_note_not_in_list_for_another_user(self):
        """Проверка что в список заметок одного пользователя не попадают
        заметки другого пользователя
        """
        response = self.reader_client.get(self.URL_NOTES_LIST)
        object_list = response.context['object_list']
        self.assertEqual(object_list.count(), 0)

    def test_pages_contains_form(self):
        """Проверка что на страницы создания и редактирования заметки
        передаются формы.
        """
        urls_notes_add_edit = (self.URL_NOTES_ADD, self.URL_NOTES_EDIT)
        for name in urls_notes_add_edit:
            with self.subTest(name=name):
                response = self.author_client.get(name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
