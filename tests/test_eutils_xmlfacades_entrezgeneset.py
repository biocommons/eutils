import vcr


@vcr.use_cassette
def test_entrezgeneset(client):
    r = client.efetch(db="gene", id=4747)

    assert isinstance(r.entrezgenes, list)
    assert len(r.entrezgenes) == 1
    assert r.entrezgenes[0].gene_id == 4747
