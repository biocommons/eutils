class EutilsError(Exception):
    pass

class EutilsBadRequestError(EutilsError):
    pass
EutilsRequestError = EutilsBadRequestError

class EutilsNotFoundError(EutilsError):
    pass

class EutilsNCBIError(EutilsError):
    pass
