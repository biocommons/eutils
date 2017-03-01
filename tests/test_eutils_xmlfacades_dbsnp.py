
import vcr


@vcr.use_cassette
def test_two_snps(client):
    es = client.efetch(db="snp", id=[2031,14181])

    assert len(es) == 2
