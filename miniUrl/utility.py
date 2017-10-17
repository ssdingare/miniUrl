import validators
import jsonschema
from user_agents import parse
from jsonschema.exceptions import ValidationError


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
    try:
        jsonschema.validate(json_obj, request_schema)
    except ValidationError:
        raise ValueError("request")
    for key in json_obj:
        if not(validators.url(json_obj[key])):
            raise ValueError("url")
    return json_obj


def classify_user_agent(user_agent_str):
    user_agent = parse(user_agent_str)
    if user_agent.is_mobile:
        return 'mobile'
    elif user_agent.is_tablet:
        return 'tablet'
    else:
        return 'default'


