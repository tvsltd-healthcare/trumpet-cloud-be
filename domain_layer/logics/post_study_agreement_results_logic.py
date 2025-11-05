from domain_layer.abstractions.request_interface import IRequest
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.check_token import check_bearer_token
from domain_layer.utils.parse_token import token_parser

def execute(request: IRequest, repo, entity=None):
    response_formatter = ResponseFormatter()
    ids = request.get_path_params()
    check_token = check_bearer_token(request)
    if not check_token:
        return response_formatter.error("Invalid or missing token", status_code=401)
    try:
        decode_token = token_parser(request.get_headers()['authorization'])

        if decode_token.get("study_agreement_id") is not None:
            ids["study_agreement_id"] = decode_token.get("study_agreement_id")

        if decode_token.get("organization_id") is not None:
            ids["organization_id"] = decode_token.get("organization_id")

        create_result = repo.post(entity, ids)

        if create_result:
            return response_formatter.success(create_result, 'Entity created successfully.', 201)
        else:
            return response_formatter.error('Entity created failed', 500)

    except Exception as e:
        return response_formatter.error(str(e), 500)
