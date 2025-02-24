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
        "Check what you submitted - it must be either the first toon name or the "
        "JSON object provided by either IdleonEfficiency or IdleonToolbox."
    )

    def __init__(self, msg, data):
        super().__init__(msg)
        self.msg = msg
        self.data = data



class DataTooLong(UserDataException):
    faq = True
    msg_base = (
        "Looks like the data you submitted was too long.<br>"
        "Check what you submitted - it must be either the first toon name or the "
        "JSON object provided by either IdleonEfficiency or IdleonToolbox."
        "<br><b>STEAM WORKAROUND DATA NOT SUPPORTED.</b>"
    )


class ProfileNotFound(BaseCustomException):
    reportable = False
    faq = True
    dirname = "private_profiles"
    msg_base = (
        "Looks like you haven't made your profile public yet.<br>"
        "Head on over to IdleonEfficiency and publish your data."
    )

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.log_msg = f"Public profile not found: {self.username}"


class EmptyResponse(BaseCustomException):
    dirname = "IE"
    msg_base = ("Hmm, something weird is going on with your data over at IdleonEfficiency, no data has been provided "
                "to us...")

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.log_msg = f"Empty response: {self.username}"


class IEConnectionFailed(BaseCustomException):
    dirname = "IE"
    msg_base = "We're having trouble connecting to IdleonEfficiency to collect data."

    def __init__(self, exc, trace):
        super().__init__()
        self.url = exc.request.url
        self.stacktrace = trace
        self.log_msg = f"Error connecting to {self.url}"


class JSONDecodeError(BaseCustomException):
    reportable = False
    faq = True
    dirname = "faulty_data"
    msg_base = "The data you submitted is corrupted or not a valid JSON structure."

    def __init__(self, data):
        super().__init__()
        self.data = data

class WtfDataException(BaseCustomException):
    reportable = False
    faq = True
    dirname = "wtf"
    msg_base = "This doesn't look like an IdleOn JSON, or is missing required data keys to be Reviewed.<br>NOTE: AutoReview cannot read the Steam Workaround JSONs from Toolbox at this time!<br>Please check your Data and try again!"

    def __init__(self, data):
        super().__init__()
        self.data = data
