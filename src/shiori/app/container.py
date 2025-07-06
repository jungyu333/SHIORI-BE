from dependency_injector.containers import (DeclarativeContainer,
                                            WiringConfiguration)

from shiori.app.user.container import UserContainer


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    user_container = UserContainer()