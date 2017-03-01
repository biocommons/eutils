import vcr

@vcr.use_cassette
def test_esearchresult(client):
    r = client.esearch(db="pubmed", term="hart rk[author]")

    assert 5 < r.count
    assert 0 == r.retstart
    assert isinstance(r.ids, list)
    assert 27814769 in r.ids
