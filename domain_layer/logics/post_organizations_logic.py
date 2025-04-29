from domain_layer.utils.parse_token import token_parser
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.abstractions.request_interface import IRequest


def execute(request: IRequest, repo, entity=None):
    response_formatter = ResponseFormatter()

    # Validate entity
    if entity is None:
        return response_formatter.error('Entity cannot be None', 400)

    # Remove "Bearer " prefix from token and decode data
    decode_token = token_parser(request.get_headers()['authorization'])
    email = decode_token.get("email")
    if not email:
        return response_formatter.error('Email missing.',400)
    entity.email = email
    try:
        create_organizations = repo.post(entity, request.get_path_params())
        if create_organizations:
            return response_formatter.success( create_organizations, 'Organizations created successfully.', 200)
        else:
            return response_formatter.error('Organizations created failed', 500)

    except Exception as e:
        return response_formatter.error(str(e), 500)