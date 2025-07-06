from dependency_injector.containers import (DeclarativeContainer,
                                            WiringConfiguration)
from dependency_injector.providers import Factory

from shiori.app.user.application.service import UserService
from shiori.app.user.application.usecase import CreateUserUseCase
from shiori.app.user.infra.repository.user import UserRepositoryImpl


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["shiori.app.user"])

    """repository"""
    user_repository = Factory(UserRepositoryImpl)

    """ service """
    user_service = Factory(UserService, user_repo=user_repository)

    """ usecase """
    create_user = Factory(CreateUserUseCase, user_service=user_service)
