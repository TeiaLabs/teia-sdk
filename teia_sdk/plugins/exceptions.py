from ..exceptions import TeiaSdkError


class ErrorToGetPluginInfo(TeiaSdkError):
    """Error to get plugin info"""


class ErrorToGetPluginResponse(TeiaSdkError):
    """Error to get plugin info"""


class ErrorPluginAPISelectAndRun(TeiaSdkError):
    """API was not able to select and run plugins"""
