from enum import Enum
from typing import Union

from sqlalchemy import Case

from application_layer.abstractions.fga_authorizer_interface import IFGAAuthorizer

from adapters.fga_authorization_adapters.openfga_authorization_adapter import OpenFgaAuthorization, \
    Configuration as OpenFgaConfiguration


class Mechanism(str, Enum):
    OPEN_FGA = "OPEN_FGA"

class FgaAuthorizationFactory:
    @staticmethod
    def create(mechanism: Mechanism, configuration: Union[OpenFgaConfiguration]) -> IFGAAuthorizer:
        match mechanism:
            case Mechanism.OPEN_FGA:
                return OpenFgaAuthorization(configuration)
            case _:
                raise "Error"
