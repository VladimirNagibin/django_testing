import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args', (('news:home', None),
                   ('news:detail', pytest.lazy_fixture('args_for_news')),
                   ('users:login', None),
                   ('users:logout', None),
                   ('users:signup', None))
)
def test_pages_availability_for_anonymous_user(client, name, args):
    response = client.get(reverse(name, args=args))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'current_client, status', (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND)
    )
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_availability_for_comment_edit_and_delete(
    current_client, status, name, comment
):
    url = reverse(name, args=(comment.id,))
    response = current_client.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_redirect_for_anonymous_client(name, comment, client):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    response = client.get(url)
    assertRedirects(response, f'{login_url}?next={url}')
