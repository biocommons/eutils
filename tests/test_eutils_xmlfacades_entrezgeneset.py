import vcr


@vcr.use_cassette
def test_entrezgeneset(client):
    r = client.efetch(db="gene", id=4747)

    assert isinstance(r.entrezgenes, list)
    assert 1 == len(r.entrezgenes)
    assert 4747 == r.entrezgenes[0].gene_id
    
