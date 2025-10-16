"""OpenFGA authorization adapter implementation.

This module provides an implementation of the IFGAAuthorizer interface using OpenFGA
as the authorization service. It handles the configuration and communication with
OpenFGA's API for permission checks and relationship management.

Classes:
    Configuration: TypedDict defining OpenFGA configuration parameters.
    OpenFgaAuthorization: Implementation of IFGAAuthorizer for OpenFGA service.

Example:
    >>> config = Configuration(
    ...     OPENFGA_API_URL="https://api.fga.example",
    ...     OPENFGA_STORE_ID="store123",
    ...     OPENFGA_MODEL_ID="model123"
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
import json
import os
from typing import TypedDict

from openfga_sdk import ClientConfiguration
from openfga_sdk.client import ClientCheckRequest
from openfga_sdk.client.models import ClientTuple, ClientWriteRequest
from openfga_sdk.sync import OpenFgaClient

from application_layer.abstractions.fga_authorizer_interface import IFGAAuthorizer, CheckParams, CheckResponse, \
    AddRelationParams


class Configuration(TypedDict):
    """Configuration parameters for OpenFGA authorization.

    Attributes:
        OPENFGA_API_URL: Base URL of the OpenFGA API endpoint.
        OPENFGA_STORE_ID: Identifier of the OpenFGA store.
        OPENFGA_MODEL_ID: Identifier of the authorization model.
    """

    OPENFGA_API_URL: str
    OPENFGA_STORE_ID: str
    OPENFGA_MODEL_ID: str


class OpenFgaAuthorization(IFGAAuthorizer):
    """OpenFGA implementation of the IFGAAuthorizer interface.

    This class provides methods to interact with OpenFGA service for authorization
    checks and relationship management.
    """

    def __init__(self, configuration: Configuration):
        """Initialize OpenFGA authorization client.

        Args:
            configuration: Dictionary containing OpenFGA configuration parameters.
                Must include OPENFGA_API_URL, OPENFGA_STORE_ID, and OPENFGA_MODEL_ID.
        """
        client_configuration = ClientConfiguration(
            api_url=configuration.get("OPENFGA_API_URL"),
            store_id=configuration.get("OPENFGA_STORE_ID"),
            # authorization_model_id=configuration.get("OPENFGA_MODEL_ID"),
        )

        self.fga_client = OpenFgaClient(client_configuration)
        CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
        MODEL_FILE_PATH = os.path.join(CURRENT_DIR_PATH, 'openfga_authorization_model.json')
        with open(MODEL_FILE_PATH) as authorization_model_str:
            authorization_model = json.load(authorization_model_str)
            response = self.fga_client.write_authorization_model(authorization_model)
            print(f"{response=}")

        # async def write_authorization_model():
            # body_string = "{\"schema_version\":\"1.1\",\"type_definitions\":[{\"type\":\"user\"},{\"type\":\"document\",\"relations\":{\"reader\":{\"this\":{}},\"writer\":{\"this\":{}},\"owner\":{\"this\":{}}},\"metadata\":{\"relations\":{\"reader\":{\"directly_related_user_types\":[{\"type\":\"user\"}]},\"writer\":{\"directly_related_user_types\":[{\"type\":\"user\"}]},\"owner\":{\"directly_related_user_types\":[{\"type\":\"user\"}]}}}}]}"
            # response = await fga_client_instance.write_authorization_model(json.loads(body))

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

    def add_relation(self, params: AddRelationParams):
        try:
            print(f"{params=}")

            body = ClientWriteRequest(
                writes=[
                    ClientTuple(
                        user=f"{params.get('user_type')}:{params.get('user_id')}",
                        relation=f"{params.get('action')}",
                        object=f"{params.get('resource_type')}:{params.get('resource_id')}",
                    ),
                ],
            )
            return self.fga_client.write(body)
        except Exception as e:
            print(f"Error in add_relation: {e}")
            raise e


    def delete_relation(self):
        """Delete a relationship between a user and a resource.

        Not implemented yet.
        """
        pass
