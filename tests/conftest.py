import logging
import os
from pathlib import Path

import pytest
import vcr

import biocommons.eutils

logging.basicConfig()
logger = logging.getLogger("vcr")
logger.setLevel(logging.DEBUG)

test_dir = Path(__file__)
test_data_dir = test_dir / "data" / "cassettes"

vcr.default_vcr = vcr.VCR(
    cassette_library_dir=test_data_dir,
    filter_headers=["Authorization"],
    filter_post_data_parameters=["Authorization"],
    record_mode=os.environ.get("VCR_RECORD_MODE", "once"),
)
vcr.use_cassette = vcr.default_vcr.use_cassette


@pytest.fixture(scope="session")
def client():
    return biocommons.eutils.Client()


@pytest.fixture(scope="session")
def qs():
    return biocommons.eutils.QueryService()
