from typing import List

from fastapi.middleware.cors import CORSMiddleware


class CorsConfig:
    """
    Configures Cross-Origin Resource Sharing (CORS) settings for an application.

    Attributes:
        origins (List[str]): A list of allowed origins.
        allow_credentials (bool): Flag to allow credentials in CORS requests.
        allow_methods (List[str]): A list of allowed HTTP methods for CORS.
        allow_headers (List[str]): A list of allowed HTTP headers for CORS.
    """

    def __init__(self, origins: List[str], allow_credentials: bool = True,
                 allow_methods: List[str] = ("*",), allow_headers: List[str] = ("*",)):
        """
        Initializes CorsConfig with specified CORS settings.

        Args:
            origins (List[str]): List of origins allowed in CORS requests.
            allow_credentials (bool, optional): Whether to allow credentials in CORS.
                Defaults to True.
            allow_methods (List[str], optional): HTTP methods allowed in CORS.
                Defaults to ["*"].
            allow_headers (List[str], optional): HTTP headers allowed in CORS.
                Defaults to ["*"].
        """
        self.origins = origins
        self.allow_credentials = allow_credentials
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers

    def apply_to_server(self, server) -> None:
        """
        Applies the CORS configuration to the specified application.

        Args:
            server: The application instance to which CORS settings are applied.
        """
        server.use(
            CORSMiddleware,
            allow_origins=self.origins,
            allow_credentials=self.allow_credentials,
            allow_methods=self.allow_methods,
            allow_headers=self.allow_headers,
        )
