import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name', (pytest.lazy_fixture('url_home'),
             pytest.lazy_fixture('url_news_detail'),
             pytest.lazy_fixture('url_login'),
             reverse('users:logout'),
             reverse('users:signup'))
)
def test_pages_availability_for_anonymous_user(client, name):
    response = client.get(name)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'current_client, status', (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND)
    )
)
@pytest.mark.parametrize(
    'name',
    (pytest.lazy_fixture('url_edit_comment'),
     pytest.lazy_fixture('url_delete_comment')),
)
def test_availability_for_comment_edit_and_delete(
    current_client, status, name
):
    response = current_client.get(name)
    assert response.status_code == status


@pytest.mark.parametrize(
    'name',
    (pytest.lazy_fixture('url_edit_comment'),
     pytest.lazy_fixture('url_delete_comment')),
)
def test_redirect_for_anonymous_client(name, client, url_login):
    response = client.get(name)
    assertRedirects(response, f'{url_login}?next={name}')
