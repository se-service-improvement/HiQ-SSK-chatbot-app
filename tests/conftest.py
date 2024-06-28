import pytest


def pytest_addoption(parser):
***REMOVED***parser.addoption(
***REMOVED***"--use-keyvault-secrets",
***REMOVED***help='Get secrets from a keyvault instead of the environment.',
***REMOVED***action='store_true', default=False
)


@pytest.fixture(scope="session")
def use_keyvault_secrets(request) -> str:
***REMOVED***return request.config.getoption("use_keyvault_secrets")