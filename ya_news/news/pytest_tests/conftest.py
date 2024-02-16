from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse

from news.models import Comment, News

NEWS_COUTN_ADD = 1
COMMENTS_COUNT_ADD = 5
TEXT = 'Text'
NEW_TEXT = 'New text'
TITLE = 'Title'


@pytest.fixture
def author(django_user_model):
    """Авторизованный пользователь, автор комментариев."""
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def reader(django_user_model):
    """Авторизованный пользователь, не автор комментариев."""
    return django_user_model.objects.create(username='Reader')


@pytest.fixture
def author_client(author):
    """Клиент с авторизованным пользователем author."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    """Клиент с авторизованным пользователем reader."""
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    """Экземпляр класса News."""
    news = News.objects.create(
        title=TITLE,
        text=TEXT,
    )
    return news


@pytest.fixture
def comment(author, news):
    """Экземпляр класса Comment с автором author."""
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=TEXT,
    )
    return comment


@pytest.fixture
def form_data():
    """Словарь с данными для обновления комментария."""
    return {
        'text': NEW_TEXT
    }


@pytest.fixture
def url_news_detail(news):
    """Страница отдельной новости."""
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_edit_comment(comment):
    """Страница редактирования комментария."""
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def url_delete_comment(comment):
    """Страница удаления комментария."""
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def url_home():
    """Главная страница."""
    return reverse('news:home')


@pytest.fixture
def url_login():
    """Страница входа в учётную запись."""
    return reverse('users:login')


@pytest.fixture
def url_logout():
    """Страница выхода из учётной записи."""
    return reverse('users:logout')


@pytest.fixture
def url_signup():
    """Страница регистрации пользователей."""
    return reverse('users:signup')


@pytest.fixture
def many_news():
    """Создание набора новостей."""
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'{TITLE} {index}',
            text=TEXT,
            date=today - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + NEWS_COUTN_ADD)
    )


@pytest.fixture
def many_comments(news, author):
    """Создание набора комментариев."""
    for index in range(COMMENTS_COUNT_ADD):
        Comment.objects.create(
            news=news, author=author, text=f'{TEXT} {index}'
        )
