from miniUrl.utility import *
import pytest


@pytest.mark.parametrize("json", [
    {"default": "http://news.bbc.co.uk" },

    {"default": "http://gmail.com",
     "mobile" : "http://m.gmail.com" },
])
def test_validate_json_passes(json):
    validate_json(json)


@pytest.mark.parametrize("json", [
    {"mobile": "http://m.gmail.com"},

    {"phone": "http://m.gmail.com"},

    {"default": "https://gmail.com",
     "phone": "http://m.gmail.com"},
])
def test_validate_json_raises(json):
    with pytest.raises(JsonValidationException):
        validate_json(json)


@pytest.mark.parametrize("json", [
    {"default": "ftp://www.example.com"},
    {"default": "http://localhost:5000"},
    {"mobile": "news.bbc.co.uk"},
    {"mobile": "DROP 'TABLE"},
])
def test_validate_urls(json):
    with pytest.raises(UrlValidationException):
        validate_urls(json, "http://localhost:5000")


@pytest.mark.parametrize("user_agent_str, expected", [
    ("Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko", "default"),
    ("Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1", "mobile"),
    ("Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)", "mobile"),
    ("Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10", "tablet"),
])
def test_identify_device_type(user_agent_str, expected):
    assert identify_device_type(user_agent_str) == expected

