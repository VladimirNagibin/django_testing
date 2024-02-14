from datetime import datetime, timedelta
import pytest

from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

COMMENTS_COUNT = 10
NEWS_COUTN_ADD = 1
TEXT = 'Text'
NEW_TEXT = 'New text'
TITLE = 'Title'


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Reader')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title=TITLE,
        text=TEXT,
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=TEXT,
    )
    return comment


@pytest.fixture
def form_data():
    return {
        'text': NEW_TEXT
    }


@pytest.fixture
def url_news_detail(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_to_comments(url_news_detail):
    return url_news_detail + '#comments'


@pytest.fixture
def url_edit_comment(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def url_delete_comment(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def url_login():
    return reverse('users:login')


@pytest.fixture
def url_home():
    return reverse('news:home')


@pytest.fixture
def many_news():
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
    now = timezone.now()
    for index in range(COMMENTS_COUNT):
        comment = Comment.objects.create(
            news=news, author=author, text=f'{TEXT} {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
