from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

URL_HOME = pytest.lazy_fixture('url_home')
URL_NEWS_DETAIL = pytest.lazy_fixture('url_news_detail')
URL_LOGIN = pytest.lazy_fixture('url_login')
URL_LOGOUT = pytest.lazy_fixture('url_logout')
URL_SIGNUP = pytest.lazy_fixture('url_signup')
URL_EDIT_COMMENT = pytest.lazy_fixture('url_edit_comment')
URL_DELETE_COMMENT = pytest.lazy_fixture('url_delete_comment')
ANONYMOUS_CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
READER_CLIENT = pytest.lazy_fixture('reader_client')


@pytest.mark.parametrize(
    'current_url, current_client, status', (
        (URL_HOME, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_NEWS_DETAIL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_LOGIN, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_LOGOUT, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_SIGNUP, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (URL_EDIT_COMMENT, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_EDIT_COMMENT, READER_CLIENT, HTTPStatus.NOT_FOUND),
        (URL_DELETE_COMMENT, AUTHOR_CLIENT, HTTPStatus.OK),
        (URL_DELETE_COMMENT, READER_CLIENT, HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability_for_anonymous_user(
    current_url, current_client, status
):
    """Проверка доступности страниц:
    Главная страница, страница отдельной новости, страницы регистрации
    пользователей, входа в учётную запись и выхода из неё доступна
    анонимному пользователю.
    Страницы удаления и редактирования комментария доступны автору комментария.
    При попытке перехода на страницу редактирования или удаления чужих
    комментариев авторизованным пользователем возвращается ошибка 404.
    """
    response = current_client.get(current_url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'current_url, current_client, redirect_url', (
        (URL_EDIT_COMMENT, ANONYMOUS_CLIENT, URL_LOGIN),
        (URL_DELETE_COMMENT, ANONYMOUS_CLIENT, URL_LOGIN)
    )
)
def test_redirect_for_anonymous_client(
    current_url, current_client, redirect_url
):
    """Проверка редиректа. При попытке перейти на страницу редактирования
    или удаления комментария анонимный пользователь перенаправляется на
    страницу авторизации.
    """
    response = current_client.get(current_url)
    assertRedirects(response, f'{redirect_url}?next={current_url}')
