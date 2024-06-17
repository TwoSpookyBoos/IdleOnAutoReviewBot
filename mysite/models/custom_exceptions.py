class BaseCustomException(Exception):
    let_us_know = 'If the problem persists let us know in the <a href="{}">Bug reports</a> on our Discord server, mention<br><code>{}</code>'
    msg_base = None

    def __init__(self, *args, reportable=True):
        super().__init__(*args)
        self.msg_display = self.msg_base
        if reportable:
            self.msg_display = "<br>".join([self.msg_display, self.let_us_know])


class UsernameBanned(BaseCustomException):
    dirname = "banned"
    msg_base = "You have been banned from using this tool.<br>Goodbye."

    def __init__(self, username):
        super().__init__(reportable=False)
        self.username = username


class UserDataException(BaseCustomException):
    dirname = "bad_submits"
    msg_base = (
        "Looks like the data you submitted was neither a username nor valid data.<br>"
        "Check what you submitted - it must be either the first toon name or the "
        "JSON object provided by either IdleonEfficiency or IdleonToolbox."
    )

    def __init__(self, msg, data):
        super().__init__(msg, reportable=False)
        self.msg = msg
        self.data = data


class ProfileNotFound(BaseCustomException):
    dirname = "private_profiles"
    msg_base = "Looks like you haven't made your profile public yet.<br>Head on over to IdleonEfficiency and publish your data."

    def __init__(self, username):
        super().__init__()
        self.username = username


class EmptyResponse(BaseCustomException):
    dirname = "IE"
    msg_base = "Hmm, something weird is going on with your data over at IdleonEfficiency, no data has been provided to us..."

    def __init__(self, username):
        super().__init__()
        self.username = username


class IEConnectionFailed(BaseCustomException):
    dirname = "IE"
    msg_base = "We're having trouble connecting to IdleonEfficiency to collect data."

    def __init__(self, exc, trace):
        super().__init__()
        self.url = exc.request.url
        self.stacktrace = trace
