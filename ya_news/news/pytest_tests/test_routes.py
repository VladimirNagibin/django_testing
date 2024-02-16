from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'current_url, current_client, status', (
        (pytest.lazy_fixture('url_home'),
         pytest.lazy_fixture('client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_news_detail'),
         pytest.lazy_fixture('client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_login'),
         pytest.lazy_fixture('client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_logout'),
         pytest.lazy_fixture('client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_signup'),
         pytest.lazy_fixture('client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_edit_comment'),
         pytest.lazy_fixture('author_client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_edit_comment'),
         pytest.lazy_fixture('reader_client'),
         HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('url_delete_comment'),
         pytest.lazy_fixture('author_client'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('url_delete_comment'),
         pytest.lazy_fixture('reader_client'),
         HTTPStatus.NOT_FOUND),
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
        (pytest.lazy_fixture('url_edit_comment'),
         pytest.lazy_fixture('client'),
         pytest.lazy_fixture('url_login')),
        (pytest.lazy_fixture('url_delete_comment'),
         pytest.lazy_fixture('client'),
         pytest.lazy_fixture('url_login'))
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
