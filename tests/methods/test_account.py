import pytest
from anilibria_api_client.models.legacy_models import (
    AgeRating,
    CollectionType,
    ContentType,
    ReleaseCollection,
    TimeCode,
)
from anilibria_api_client.models.responses import *

from anilibria_api_client.api_client import AsyncAnilibriaAPI


@pytest.mark.asyncio
async def test_col_releases_get_post(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    releases_get = (
        await anilibria_api_client.accounts.users_me_collections_releases_get(
            release_collection=ReleaseCollection(
                type_of_collection=CollectionType.PLANNED,
                page=1,
                limit=10,
                genres="14,29",
                types=[ContentType.MOVIE],
                years="2017",
                search="Мастера Меча Онлайн: Порядковый ранг",
                age_ratings=[AgeRating.R16_PLUS],
                include="",
            )
        )
    )

    releases_post = (
        await anilibria_api_client.accounts.users_me_collections_releases_post(
            release_collection=ReleaseCollection(
                type_of_collection=CollectionType.PLANNED,
                page=1,
                limit=10,
                genres="14,29",
                types=[ContentType.MOVIE],
                years="2017",
                search="Мастера Меча Онлайн: Порядковый ранг",
                age_ratings=[AgeRating.R16_PLUS],
                include="",
            )
        )
    )

    assert isinstance(releases_get, UsersMeCollectionsReleasesResponse)
    assert isinstance(releases_post, UsersMeCollectionsReleasesResponse)


@pytest.mark.asyncio
async def test_timecodes(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    response = await anilibria_api_client.accounts.users_me_views_timecodes()
    await anilibria_api_client.accounts.users_me_views_timecodes_delete(
        episode_id_list=["9fba7e92-1a4f-4712-962f-b0a683009e66"]
    )
    await anilibria_api_client.accounts.users_me_views_timecodes_update(
        timecode_list=[
            TimeCode(
                time=500.92,
                is_watched=False,
                release_episode_id="9fba7e92-1a4f-4712-962f-b0a683009e66",
            )
        ]
    )
    (await anilibria_api_client.accounts.users_me_views_timecodes())

    assert response.get_episode_timecodes()
    assert isinstance(response, UsersMeViewsTimecodesResponse)


@pytest.mark.asyncio
async def test_me_profile(
    anilibria_api_client: AsyncAnilibriaAPI,
) -> None:
    response = await anilibria_api_client.accounts.users_me_profile()

    assert isinstance(response, UsersMeProfileResponse)


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
        fav_age_ratings, UsersMeFavoritesReferencesAgeRatingsResponse
    )
    assert isinstance(fav_genres, UsersMeFavoritesReferencesGenresResponse)
    assert isinstance(fav_sorting, UsersMeFavoritesReferencesSortingResponse)
    assert isinstance(fav_types, UsersMeFavoritesReferencesTypesResponse)
    assert isinstance(fav_years, UsersMeFavoritesReferencesYearsResponse)

    assert isinstance(
        col_age_ratings, UsersMeCollectionsReferencesAgeRatingsResponse
    )
    assert isinstance(col_genres, UsersMeCollectionsReferencesGenresResponse)
    assert isinstance(col_types, UsersMeCollectionsReferencesTypesResponse)
    assert isinstance(col_years, UsersMeCollectionsReferencesYearsResponse)
