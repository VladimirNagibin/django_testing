import pytest
from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
    client, url_news_detail, form_data
):
    client.post(url_news_detail, data=form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        author_client,
        news,
        form_data,
        author,
        url_news_detail,
        url_to_comments
):
    response = author_client.post(url_news_detail, data=form_data)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, url_news_detail):
    bad_words_data = {'text': f'Text, {BAD_WORDS[0]}, text'}
    response = author_client.post(url_news_detail, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
    author_client, url_delete_comment, url_to_comments
):
    response = author_client.delete(url_delete_comment)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    reader_client, url_delete_comment
):
    response = reader_client.delete(url_delete_comment)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
    author_client, url_edit_comment, url_to_comments, comment, form_data
):
    response = author_client.post(url_edit_comment, data=form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(
    reader_client, url_edit_comment, comment, form_data
):
    comment_text = comment.text
    response = reader_client.post(url_edit_comment, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == comment_text
