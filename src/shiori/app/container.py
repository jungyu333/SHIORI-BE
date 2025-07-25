from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory

from shiori.app.auth.application.service import JwtService
from shiori.app.auth.application.usecase import RefreshUseCase, VerifyTokenUseCase
from shiori.app.user.application.service import UserService
from shiori.app.user.application.usecase import (
    CreateUserUseCase,
    LoginUserUseCase,
    LogoutUserUseCase,
)
from shiori.app.user.infra.repository.user import UserRepositoryImpl


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["shiori.app.user", "shiori.app.auth"])

    jwt_service = Factory(JwtService)

    """repository"""
    user_repository = Factory(UserRepositoryImpl)

    """ service """
    user_service = Factory(UserService, user_repo=user_repository)

    """ usecase """

    """ User """
    create_user = Factory(CreateUserUseCase, user_service=user_service)
    login_user = Factory(LoginUserUseCase, user_service=user_service)
    logout_user = Factory(LogoutUserUseCase, user_service=user_service)
    refresh = Factory(RefreshUseCase, jwt_service=jwt_service)
    verify_token = Factory(VerifyTokenUseCase, jwt_service=jwt_service)
