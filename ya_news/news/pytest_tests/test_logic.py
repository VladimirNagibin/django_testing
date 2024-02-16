from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(
    client, url_news_detail, form_data
):
    """Проверка не возможности отправки комментария анонимным пользователем."""
    comments_count = Comment.objects.count()
    client.post(url_news_detail, data=form_data)
    assert Comment.objects.count() == comments_count


def test_user_can_create_comment(
        author_client,
        news,
        form_data,
        author,
        url_news_detail,
):
    """Проверка отправки комментария авторизованным пользователем."""
    comments_count = Comment.objects.count()
    comments_all = set(Comment.objects.all())
    response = author_client.post(url_news_detail, data=form_data)
    assertRedirects(response, url_news_detail + '#comments')
    assert Comment.objects.count() == comments_count + 1
    comments_upd_all = set(Comment.objects.all())
    comments_difference = comments_upd_all.difference(comments_all)
    assert len(comments_difference) == 1
    comment = comments_difference.pop()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, url_news_detail):
    """Проверка неопубликования комментария с запрещёнными словами."""
    comments_count = Comment.objects.count()
    bad_words_data = {'text': f'Text, {BAD_WORDS[0]}, text'}
    response = author_client.post(url_news_detail, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == comments_count


def test_author_can_delete_comment(
    author_client, url_delete_comment, url_news_detail
):
    """Проверка удаления комментариев авторизованным автором."""
    comments_count = Comment.objects.count()
    response = author_client.delete(url_delete_comment)
    assertRedirects(response, url_news_detail + '#comments')
    assert Comment.objects.count() == comments_count - 1


def test_user_cant_delete_comment_of_another_user(
    reader_client, url_delete_comment
):
    """Проверка, что авторизованный пользователь не может удалять чужие
    комментарии.
    """
    comments_count = Comment.objects.count()
    response = reader_client.delete(url_delete_comment)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count


def test_author_can_edit_comment(
    author_client, url_edit_comment, url_news_detail, form_data
):
    """Проверка редактирования авторизованным автором своих комментариев."""
    comments_all = set(Comment.objects.all())
    assert len(comments_all) == 1
    response = author_client.post(url_edit_comment, data=form_data)
    assertRedirects(response, url_news_detail + '#comments')
    comments_upd_all = set(Comment.objects.all())
    assert len(comments_upd_all.difference(comments_all)) == 0
    assert len(comments_upd_all) == 1
    comment_new = comments_upd_all.pop()
    comment_original = comments_all.pop()
    assert comment_new.text == form_data['text']
    assert comment_new.news == comment_original.news
    assert comment_new.author == comment_original.author
    assert comment_new.created == comment_original.created


def test_user_cant_edit_comment_of_another_user(
    reader_client, url_edit_comment, form_data
):
    """Проверка, что авторизованный пользователь не может редактировать чужие
    комментарии.
    """
    comments_all = set(Comment.objects.all())
    assert len(comments_all) == 1
    response = reader_client.post(url_edit_comment, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_upd_all = set(Comment.objects.all())
    assert len(comments_upd_all.difference(comments_all)) == 0
    assert len(comments_upd_all) == 1
    comment_new = comments_upd_all.pop()
    comment_original = comments_all.pop()
    assert comment_new.text == comment_original.text
    assert comment_new.news == comment_original.news
    assert comment_new.author == comment_original.author
    assert comment_new.created == comment_original.created
