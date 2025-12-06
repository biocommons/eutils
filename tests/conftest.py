import os

import pytest
import vcr

import biocommons.eutils

test_dir = os.path.dirname(__file__)  # noqa: PTH120
test_data_dir = os.path.join(test_dir, "data", "cassettes")  # noqa: PTH118

vcr.default_vcr = vcr.VCR(
    cassette_library_dir=test_data_dir,
    filter_headers=["Authorization"],
    filter_post_data_parameters=["Authorization"],
    filter_query_parameters=["api_key"],
    record_mode=os.environ.get("VCR_RECORD_MODE", "none"),
)
vcr.use_cassette = vcr.default_vcr.use_cassette


@pytest.fixture(scope="session")
def client():
    return biocommons.eutils.Client()


@pytest.fixture(scope="session")
def qs():
    return biocommons.eutils.QueryService()
