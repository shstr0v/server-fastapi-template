from dishka import Provider, Scope, provide_all

from app.application.interactors.auth.email_login import EmailLogin
from app.application.interactors.auth.logout import Logout
from app.application.interactors.auth.phone_login import PhoneLogin
from app.application.interactors.auth.phone_login_verify import PhoneLoginVerify
from app.application.interactors.otp.send import SendOtp
from app.application.interactors.uploads import CreatePresignedDownload, CreatePresignedUpload
from app.application.interactors.user import (
    ActivateUserWithTokenInteractor,
    CompleteUser,
    GetByUsername,
    SignUp,
    UpdateUser,
    VerifyPhone,
)


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    provides = provide_all(
        EmailLogin,
        Logout,
        PhoneLogin,
        PhoneLoginVerify,
        SendOtp,
        CreatePresignedDownload,
        CreatePresignedUpload,
        ActivateUserWithTokenInteractor,
        CompleteUser,
        GetByUsername,
        SignUp,
        UpdateUser,
        VerifyPhone,
    )
