import os
import json
import pytest
import tempfile
import validators
from miniUrl import app, init_db


@pytest.fixture()
def client(request):
    db_file_handle, app.config['DATABASE'] = tempfile.mkstemp()
    app.testing = True
    with app.app_context():
        init_db()

    def tear_down():
        os.close(db_file_handle)
        os.unlink(app.config['DATABASE'])

    return app.test_client()


def test_shorten_url(client):
    response = client.post('/shorten', data='{"default" : "http://cnn.com"}', content_type='application/json');
    json_response = json.loads(response.data.decode('utf8'))
    assert response.status_code == 200
    assert "miniUrl" in json_response
    mini_url = json_response['miniUrl']
    validators.url(mini_url)
    assert app.config['MINI_URL_BASE'] in mini_url


def test_redirect(client):
    response = client.post('/shorten', data='{"default" : "http://cnn.com"}', content_type='application/json');
    mini_url = json.loads(response.data.decode('utf8'))["miniUrl"]
    response = client.get(mini_url)
    assert response.status_code == 302
    assert("cnn" in response.data)


def test_stats(client):
    for count in range(5):
        client.post('/shorten', data='{"default" : "http://cnn.com"}', content_type='application/json');
    response = client.get('/stats')
    json_response = json.loads(response.data.decode('utf8'))
    assert response.status_code == 200
    urls_stored_count = 0
    for key in json_response:
        validators.url(key)
        urls_stored_count+=1
    assert urls_stored_count == 5
