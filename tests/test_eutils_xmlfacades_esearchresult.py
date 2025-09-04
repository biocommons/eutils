import vcr


@vcr.use_cassette
def test_esearchresult(client):
    r = client.esearch(db="pubmed", term="hart rk[author]")

    assert r.count > 5
    assert r.retstart == 0
    assert isinstance(r.ids, list)
    assert 27814769 in r.ids
