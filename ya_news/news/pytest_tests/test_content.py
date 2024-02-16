import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, url_home, many_news):
    """Проверка количество новостей на главной странице
    не более указанного в настройках.
    """
    response = client.get(url_home)
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, url_home, many_news):
    """Проверка сортировки новостей на главной странице от новых к старым."""
    response = client.get(url_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, url_news_detail, many_comments):
    """Проверка сортировки комментариев на странице отдельной новости
    от старых к новым.
    """
    response = client.get(url_news_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, url_news_detail):
    """Анонимному пользователю не видна форма для отправки комментария
    на странице отдельной новости.
    """
    response = client.get(url_news_detail)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, url_news_detail):
    """Авторизованному пользователю видна форма для отправки комментария
    на странице отдельной новости.
    """
    response = author_client.get(url_news_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
