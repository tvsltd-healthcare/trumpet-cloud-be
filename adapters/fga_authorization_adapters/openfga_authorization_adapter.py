from typing import TypedDict

from openfga_sdk import ClientConfiguration
from openfga_sdk.client import ClientCheckRequest
from openfga_sdk.sync import OpenFgaClient

from application_layer.abstractions.fga_authorizer_interface import IFGAAuthorizer, CheckParams, CheckResponse


class Configuration(TypedDict):
    FGA_API_URL: str
    FGA_STORE_ID: str
    FGA_MODEL_ID: str


class OpenFgaAuthorization(IFGAAuthorizer):
    def __init__(self, configuration: Configuration):
        client_configuration = ClientConfiguration(
            api_url=configuration.get("FGA_API_URL"),
            store_id=configuration.get("FGA_STORE_ID"),
            authorization_model_id=configuration.get("FGA_MODEL_ID"),
        )

        self.fga_client = OpenFgaClient(client_configuration)

    def check(self, params: CheckParams) -> CheckResponse:
        print(params)

        print(f"{params.get("user_type")}:{params.get('user_id')}")
        print(f"{params.get('action')}")
        print(f"{params.get('resource_type')}:{params.get('resource_id')}")

        body = ClientCheckRequest(
            user=f"{params.get("user_type")}:{params.get('user_id')}",
            relation=f"{params.get('action')}",
            object=f"{params.get('resource_type')}:{params.get('resource_id')}",
        )

        response = self.fga_client.check(body)

        return {"allowed": response.allowed}

    def batch_check(self):
        pass

    def add_relation(self):
        pass

    def delete_relation(self):
        pass
