import json
import re

from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.check_token import check_bearer_token
from domain_layer.utils.parse_token import token_parser


@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    """
    Retrieves a filtered collection of records based on path and query parameters.

    This function:
      1. Extracts path parameters from the request.
      2. Parses `filter` from query parameters (if provided as JSON string).
      3. Combines both into a final query object.
      4. Uses the provided repository to fetch records matching the query.
      5. Returns a formatted success response with the retrieved data.

    Args:
        request (IRequest): Abstract request object providing access to path and query parameters.
        repo: The repository interface used to fetch the collection of records.
        entity (Any, optional): Currently unused, present for interface consistency.

    Returns:
        dict: A formatted success response.

    Success Response Format:
        {
            "message": "Data retrieved successfully.",
            "status_code": 200,
            "data": [  # list of matched records
                {...}, {...}
            ]
        }
    """
    response_formatter = ResponseFormatter()
    ids = request.get_path_params()
    check_token = check_bearer_token(request)
    if not check_token:
        return response_formatter.error("Invalid or missing token", status_code=401)

    decode_token = token_parser(request.get_headers()['authorization'])

    if decode_token.get("study_agreement_id") is not None:
        ids["study_agreement_id"] = decode_token.get("study_agreement_id")
    if decode_token.get("organization_id") is not None:
        ids["organization_id"] = decode_token.get("organization_id")

    # Step 1: Extract path and query params
    query = request.get_query_params()
    query = query.get('filter', {}) if isinstance(query, dict) else {}

    # Step 2: Safely parse query as JSON if it's a string
    query = re.sub(r"'([^']*)'", r'"\1"', query) if query and isinstance(query, str) else query # Matches single-quoted string literals like: 'hello'

    try:
        query = json.loads(query)
    except (json.JSONDecodeError, TypeError):
        query = {}

    # Step 3: Combine path and query filters
    query = {**ids, **query}

    # Step 4: Fetch records and return response
    collected_records = repo.get_collection(query)

    return response_formatter.success(
        collected_records,
        message="Data retrieved successfully.",
        status_code=200
    )
