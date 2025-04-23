"""Factory module for Fine-Grained Authorization (FGA) mechanisms.

This module provides a factory pattern implementation for creating FGA authorization
instances. It currently supports OpenFGA as an authorization mechanism and can be
extended to support additional mechanisms in the future.

Classes:
    Mechanism: Enum class defining supported authorization mechanisms.
    FgaAuthorizationFactory: Factory class for creating FGA authorization instances.

Example:
    >>> config = OpenFgaConfiguration(...)
    >>> authorizer = FgaAuthorizationFactory.create(
    ...     mechanism=Mechanism.OPEN_FGA,
    ...     configuration=config
    ... )
"""

from enum import Enum
from typing import Union

from adapters.fga_authorization_adapters.openfga_authorization_adapter import (
    OpenFgaAuthorization,
    Configuration as OpenFgaConfiguration,
)
from application_layer.abstractions.fga_authorizer_interface import IFGAAuthorizer


class Mechanism(str, Enum):
    """Enumeration of supported FGA authorization mechanisms.

    This enum inherits from str to allow for easy serialization and deserialization
    of mechanism types.

    Attributes:
        OPEN_FGA: String value representing OpenFGA authorization mechanism.
    """
    OPEN_FGA = "OPEN_FGA"


class FgaAuthorizationFactory:
    """Factory class for creating Fine-Grained Authorization instances.

    This class implements the factory pattern to create appropriate authorization
    instances based on the specified mechanism.
    """

    @staticmethod
    def create(mechanism: Mechanism, configuration: Union[OpenFgaConfiguration]) -> IFGAAuthorizer:
        """Creates an FGA authorization instance based on the specified mechanism.

        Args:
            mechanism: The authorization mechanism to use (from Mechanism enum).
            configuration: Configuration object for the authorization mechanism.
                Currently, supports only OpenFgaConfiguration.

        Returns:
            IFGAAuthorizer: An instance of the appropriate authorization class
                implementing the IFGAAuthorizer interface.

        Raises:
            ValueError: If the specified mechanism is not supported.
        """
        match mechanism:
            case Mechanism.OPEN_FGA:
                return OpenFgaAuthorization(configuration)
            case _:
                raise ValueError(f"Unknown authorization mechanism: {mechanism}")