"""OpenFGA authorization adapter implementation.

This module provides an implementation of the IFGAAuthorizer interface using OpenFGA
as the authorization service. It handles the configuration and communication with
OpenFGA's API for permission checks and relationship management.

Classes:
    Configuration: TypedDict defining OpenFGA configuration parameters.
    OpenFgaAuthorization: Implementation of IFGAAuthorizer for OpenFGA service.

Example:
    >>> config = Configuration(
    ...     FGA_API_URL="https://api.fga.example",
    ...     FGA_STORE_ID="store123",
    ...     FGA_MODEL_ID="model123"
    ... )
    >>> auth = OpenFgaAuthorization(config)
    >>> result = auth.check({
    ...     "user_type": "user",
    ...     "user_id": "123",
    ...     "action": "read",
    ...     "resource_type": "document",
    ...     "resource_id": "456"
    ... })
"""

from typing import TypedDict

from openfga_sdk import ClientConfiguration
from openfga_sdk.client import ClientCheckRequest
from openfga_sdk.sync import OpenFgaClient

from application_layer.abstractions.fga_authorizer_interface import IFGAAuthorizer, CheckParams, CheckResponse


class Configuration(TypedDict):
    """Configuration parameters for OpenFGA authorization.

    Attributes:
        FGA_API_URL: Base URL of the OpenFGA API endpoint.
        FGA_STORE_ID: Identifier of the OpenFGA store.
        FGA_MODEL_ID: Identifier of the authorization model.
    """

    FGA_API_URL: str
    FGA_STORE_ID: str
    FGA_MODEL_ID: str


class OpenFgaAuthorization(IFGAAuthorizer):
    """OpenFGA implementation of the IFGAAuthorizer interface.

    This class provides methods to interact with OpenFGA service for authorization
    checks and relationship management.
    """

    def __init__(self, configuration: Configuration):
        """Initialize OpenFGA authorization client.

        Args:
            configuration: Dictionary containing OpenFGA configuration parameters.
                Must include FGA_API_URL, FGA_STORE_ID, and FGA_MODEL_ID.
        """
        client_configuration = ClientConfiguration(
            api_url=configuration.get("FGA_API_URL"),
            store_id=configuration.get("FGA_STORE_ID"),
            authorization_model_id=configuration.get("FGA_MODEL_ID"),
        )

        self.fga_client = OpenFgaClient(client_configuration)

    def check(self, params: CheckParams) -> CheckResponse:
        """Check if a user has a specific permission on a resource.

        Args:
            params: Dictionary containing check parameters:
                - user_type: Type of the user (e.g., 'user', 'service')
                - user_id: Unique identifier of the user
                - action: Permission to check (e.g., 'read', 'write')
                - resource_type: Type of the resource
                - resource_id: Unique identifier of the resource

        Returns:
            Dictionary containing the check result:
                - allowed: Boolean indicating if the permission is granted
        """
        body = ClientCheckRequest(
            user=f"{params.get('user_type')}:{params.get('user_id')}",
            relation=f"{params.get('action')}",
            object=f"{params.get('resource_type')}:{params.get('resource_id')}",
        )

        response = self.fga_client.check(body)

        return {"allowed": response.allowed}

    def batch_check(self):
        """Check multiple permissions at once.

        Not implemented yet.
        """
        pass

    def add_relation(self):
        """Add a relationship between a user and a resource.

        Not implemented yet.
        """
        pass

    def delete_relation(self):
        """Delete a relationship between a user and a resource.

        Not implemented yet.
        """
        pass