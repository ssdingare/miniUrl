import validators
import jsonschema
from user_agents import parse
from jsonschema.exceptions import ValidationError


class JsonValidationException(Exception):
    pass


class UrlValidationException(Exception):
    pass


request_schema = {
    "type": "object",
    "properties": {
        "default": {
            "type": "string"
        },
        "mobile": {
            "type": "string"
        },
        "tablet": {
            "type": "string"
        }
    },
    "required": ["default"]
}


def validate_json(json_obj):
    """
    Validates json request object against request_schema; raises JsonValidationException if no default_url supplied
    :param json_obj: a json object
    """
    try:
        jsonschema.validate(json_obj, request_schema)
    except ValidationError:
        raise JsonValidationException


def validate_urls(json_obj):
    """
    Checks that each supplied url in json request object is a valid url
    :param json_obj: a json object
    """
    for key in json_obj:
        if not(validators.url(json_obj[key])):
            raise UrlValidationException


def identify_device_type(user_agent_str):
    """
    identifies the device type as 'mobile' or 'tablet' or 'default'
    :param user_agent_str:
    :return: returns a string for the device type
    """
    user_agent = parse(user_agent_str)
    if user_agent.is_mobile:
        return 'mobile'
    elif user_agent.is_tablet:
        return 'tablet'
    else:
        return 'default'


