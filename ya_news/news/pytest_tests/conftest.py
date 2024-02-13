from datetime import datetime, timedelta
import pytest

from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


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
        title='Title',
        text='Text',
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Text',
    )
    return comment


@pytest.fixture
def form_data():
    return {
        'text': 'New text'
    }


@pytest.fixture
def args_for_news(news):
    return (news.id,)


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
def all_news():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'News {index}',
            text='Text.',
            date=today - timedelta(days=index))
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def all_comments(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Text {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
