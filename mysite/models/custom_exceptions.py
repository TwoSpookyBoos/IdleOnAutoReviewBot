from config import app

class BaseCustomException(Exception):
    reportable = True
    faq = False
    let_us_know = (
        'If the problem persists let us know in the '
        f'<a class="bug" href="{app.config["CHANNEL_BUG_REPORTS"]}">Bug reports</a> '
        'on our Discord server. <strong>Paste what\'s copied once you click the link</strong>, '
        'or manually send<br><code>{}</code>'
    )
    faq_link = f'Check our <a href="{app.config["CHANNEL_FAQ"]}" target="_blank">FAQ section</a> for more info.'
    msg_base = None

    def __init__(self, *args):
        super().__init__(*args)
        self.msg_display = self.msg_base

        if self.faq:
            self.msg_display = "<br>".join([self.msg_display, self.faq_link])

        if self.reportable:
            self.msg_display = "<br>".join([self.msg_display, self.let_us_know])


class UsernameBanned(BaseCustomException):
    reportable = False
    dirname = "banned"
    msg_base = "You have been banned from using this tool.<br>Goodbye."

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.log_msg = f"Account banned: {self.username}"


class UserDataException(BaseCustomException):
    reportable = False
    dirname = "bad_submits"
    msg_base = (
        "Looks like the data you submitted was neither a username nor valid data.<br>"
        "Check what you submitted - it must be either your first character name or the "
        "JSON object provided by IdleonEfficiency, IdleonLeaderboards, or IdleonToolbox."
    )

    def __init__(self, msg, data):
        super().__init__(msg)
        self.msg = msg
        self.data = data


class ProfileNotFound(BaseCustomException):
    reportable = False
    faq = True
    dirname = "private_profiles"
    msg_base = (
        "Looks like you haven't made your profile public yet.<br>"
        "Head on over to IdleonEfficiency or IdleonLeaderboards to publish your data."
    )

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.log_msg = f"Public profile not found: {self.username}"


class EmptyResponse(BaseCustomException):
    dirname = "API"
    msg_base = ("AutoReview received empty JSONs back when requesting your data, weird."
                "<br>Please try re-uploading your Public Profile, or submit a JSON instead")

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.log_msg = f"Empty response: {self.username}"


class APIConnectionFailed(BaseCustomException):
    dirname = "API"
    msg_base = ("AutoReview didn't get a response from IdleonEfficiency or IdleonLeaderboards to collect data."
                "<br>Please try back later.")

    def __init__(self, exc, trace):
        super().__init__()
        try:
            self.url = exc.request.url
        except:
            self.url = "Unknown"
        self.stacktrace = trace
        self.log_msg = f"Error connecting to {self.url}"


class JSONDecodeError(BaseCustomException):
    reportable = False
    faq = True
    dirname = "faulty_data"
    msg_base = (
        "The JSON you submitted could not be Decoded.<br>"
        "Please verify the data wasn't pasted twice<br>"
        "or perhaps missing the enclosing curly brackets"
    )

    def __init__(self, data):
        super().__init__()
        self.data = data
