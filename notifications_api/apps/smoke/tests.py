import http

from django.urls import reverse


def test_smoke(client):
    url = reverse("smoke")
    response = client.get(url)
    assert response.status_code == http.HTTPStatus.OK
