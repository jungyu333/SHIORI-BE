from dependency_injector.containers import (DeclarativeContainer,
                                            WiringConfiguration)
from dependency_injector.providers import Factory

from .application.service import UserService
from .application.usecase import CreateUserUseCase
from .infra.repository.user import UserRepositoryImpl


class UserContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app.user"])

    """ repository """
    user_repository = Factory(UserRepositoryImpl)

    """ service """
    user_service = Factory(UserService, user_repo=user_repository)

    """ usecase """
    create_user = Factory(CreateUserUseCase, user_service=user_service)