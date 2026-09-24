import pytest
from anilibria_api_types.codegen.enums.accounts import (
    AccountsUsersUserCollectionType,
)
from anilibria_api_types.codegen.enums.anime import (
    AnimeReleasesReleaseAgeRating,
    AnimeReleasesReleaseType,
)
from anilibria_api_types.codegen.responses.models import (
    AccountsUsersCollectionsReleases,
    AccountsUsersMeCollectionsReferencesAgeRatings,
    AccountsUsersMeCollectionsReferencesGenres,
    AccountsUsersMeCollectionsReferencesTypes,
    AccountsUsersMeCollectionsReferencesYears,
    AccountsUsersMeFavoritesReferencesAgeRatings,
    AccountsUsersMeFavoritesReferencesGenres,
    AccountsUsersMeFavoritesReferencesSorting,
    AccountsUsersMeFavoritesReferencesTypes,
    AccountsUsersMeFavoritesReferencesYears,
    UsersV1User,
)

from anilibria_api_client.api_client import AsyncAnilibriaAPI


@pytest.mark.asyncio
async def test_col_releases_get_post(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    releases_get = (
        await anilibria_api_client.accounts.users_me_collections_releases_get(
            type_of_collection=AccountsUsersUserCollectionType.PLANNED,
            page=1,
            limit=10,
            f_genres="14,29",
            f_types=[AnimeReleasesReleaseType.MOVIE],
            f_years="2017",
            f_search="Мастера Меча Онлайн: Порядковый ранг",
            f_age_ratings=[AnimeReleasesReleaseAgeRating.R16_PLUS],
        )
    )

    releases_post = (
        await anilibria_api_client.accounts.users_me_collections_releases_post(
            page=1,
            limit=10,
            type_of_collection=AccountsUsersUserCollectionType.PLANNED,
        )
    )

    assert isinstance(releases_get, AccountsUsersCollectionsReleases)
    assert isinstance(releases_post, AccountsUsersCollectionsReleases)


@pytest.mark.asyncio
async def test_timecodes(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    response = (
        await anilibria_api_client.accounts.users_me_views_timecodes_get()
    )

    # Generated method returns the raw JSON array (no model validation).
    assert isinstance(response, list)


@pytest.mark.asyncio
async def test_me_profile(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    response = await anilibria_api_client.accounts.users_me_profile()

    assert isinstance(response, UsersV1User)


@pytest.mark.asyncio
async def test_all_references(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    fav_age_ratings = await anilibria_api_client.accounts.users_me_favorites_references_age_ratings()
    fav_genres = await anilibria_api_client.accounts.users_me_favorites_references_genres()
    fav_sorting = await anilibria_api_client.accounts.users_me_favorites_references_sorting()
    fav_types = await anilibria_api_client.accounts.users_me_favorites_references_types()
    fav_years = await anilibria_api_client.accounts.users_me_favorites_references_years()

    col_age_ratings = await anilibria_api_client.accounts.users_me_collections_references_age_ratings()
    col_genres = await anilibria_api_client.accounts.users_me_collections_references_genres()
    col_types = await anilibria_api_client.accounts.users_me_collections_references_types()
    col_years = await anilibria_api_client.accounts.users_me_collections_references_years()

    assert isinstance(
        fav_age_ratings, AccountsUsersMeFavoritesReferencesAgeRatings
    )
    assert isinstance(fav_genres, AccountsUsersMeFavoritesReferencesGenres)
    assert isinstance(fav_sorting, AccountsUsersMeFavoritesReferencesSorting)
    assert isinstance(fav_types, AccountsUsersMeFavoritesReferencesTypes)
    assert isinstance(fav_years, AccountsUsersMeFavoritesReferencesYears)

    assert isinstance(
        col_age_ratings, AccountsUsersMeCollectionsReferencesAgeRatings
    )
    assert isinstance(col_genres, AccountsUsersMeCollectionsReferencesGenres)
    assert isinstance(col_types, AccountsUsersMeCollectionsReferencesTypes)
    assert isinstance(col_years, AccountsUsersMeCollectionsReferencesYears)
