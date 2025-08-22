from domain_layer.abstractions.request_interface import IRequest
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.check_token import check_bearer_token


def execute(request: IRequest, repo, entity=None):
    response_formatter = ResponseFormatter()
    ids = request.get_path_params()
    check_token = check_bearer_token(request, ids.get('study_agreement_id'))
    if not check_token:
        return response_formatter.error("Invalid or missing token", status_code=401)
    try:
        update_result = repo.patch(entity, ids)

        if update_result:
            return response_formatter.success(update_result, 'Entity updated successfully.', 201)
        else:
            return response_formatter.error('Entity update failed', 500)

    except Exception as e:
        return response_formatter.error(str(e), 500)
