import json
import re

from domain_layer.abstractions.request_interface import IRequest


def get_query_params(request: IRequest) -> dict:
    query_params = request.get_query_params()
    query_data = query_params.get('filter', {}) if isinstance(query_params, dict) else {}

    query_data = re.sub(r"'([^']*)'", r'"\1"', query_data) if query_data and isinstance(query_data, str) else query_data

    try:
        return json.loads(query_data)
    except (json.JSONDecodeError, TypeError):
        return {}