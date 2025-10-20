from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory

from shiori.app.auth.application.service import JwtService
from shiori.app.auth.application.usecase import RefreshUseCase, VerifyTokenUseCase
from shiori.app.diary.application.service import DiaryService
from shiori.app.diary.application.usecase import (
    UpsertDiary,
    GetDiary,
    GetWeekDiaryMeta,
    CreateSummarize,
    GetReflection,
)
from shiori.app.diary.infra.repository import (
    DiaryRepositoryImpl,
    DiaryMetaRepositoryImpl,
    TagRepositoryImpl,
    ReflectionRepositoryImpl,
)
from shiori.app.internal.application.usecase import SummarizeResult
from shiori.app.user.application.service import UserService
from shiori.app.user.application.usecase import (
    CreateUserUseCase,
    LoginUserUseCase,
    LogoutUserUseCase,
)
from shiori.app.user.infra.repository.user import UserRepositoryImpl


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        packages=[
            "shiori.app.user",
            "shiori.app.auth",
            "shiori.app.diary",
            "shiori.app.internal",
        ],
    )

    """ Repository """

    """ User """
    user_repository = Factory(UserRepositoryImpl)

    """ Diary """
    diary_repository = Factory(DiaryRepositoryImpl)
    diary_meta_repository = Factory(DiaryMetaRepositoryImpl)
    tag_repository = Factory(TagRepositoryImpl)
    reflection_repository = Factory(ReflectionRepositoryImpl)

    """ Service """

    """ Auth """
    jwt_service = Factory(JwtService)

    """ User """
    user_service = Factory(UserService, user_repo=user_repository)

    """ Diary """
    diary_service = Factory(
        DiaryService,
        diary_repo=diary_repository,
        diary_meta_repo=diary_meta_repository,
        tag_repo=tag_repository,
        reflection_repo=reflection_repository,
    )

    """ Usecase """

    """ User """
    create_user = Factory(CreateUserUseCase, user_service=user_service)
    login_user = Factory(LoginUserUseCase, user_service=user_service)
    logout_user = Factory(LogoutUserUseCase, user_service=user_service)
    refresh = Factory(RefreshUseCase, jwt_service=jwt_service)
    verify_token = Factory(VerifyTokenUseCase, jwt_service=jwt_service)

    """ Diary """
    upsert_diary = Factory(UpsertDiary, diary_service=diary_service)
    get_diary = Factory(GetDiary, diary_service=diary_service)
    get_week_diary_meta = Factory(GetWeekDiaryMeta, diary_service=diary_service)
    create_summarize = Factory(CreateSummarize, diary_service=diary_service)
    get_reflection = Factory(GetReflection, diary_service=diary_service)

    """ Internal """
    summarize_result = Factory(SummarizeResult, diary_service=diary_service)
