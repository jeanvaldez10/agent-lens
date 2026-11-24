class MultiSessionException(Exception):
    def __init__(self, message):
        super().__init__(message)


class NoSessionException(Exception):
    def __init__(self, message="No session found"):
        super().__init__(message)


class NoApiKeyException(Exception):
    def __init__(
        self,
        message="Could not initialize agentlens client - API Key is missing."
        + "\n\t    Find your API key at http://localhost:3000/settings/projects",
    ):
        super().__init__(message)


class InvalidApiKeyException(Exception):
    def __init__(self, api_key, endpoint):
        message = f"API Key is invalid: {{{api_key}}}.\n\t    Find your API key at {endpoint}/settings/projects"
        super().__init__(message)


class ApiServerException(Exception):
    def __init__(self, message):
        super().__init__(message)


class agentlensClientNotInitializedException(RuntimeError):
    def __init__(self, message="agentlens client must be initialized before using this feature"):
        super().__init__(message)


class agentlensApiJwtExpiredException(Exception):
    def __init__(self, message="JWT token has expired"):
        super().__init__(message)
