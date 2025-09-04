import vcr


@vcr.use_cassette
def test_einfo_dblist(client):
    dblist_result = client.einfo()

    assert "protein" in dblist_result.databases
    assert len(dblist_result.databases) == 40


@vcr.use_cassette
def test_einfo_dbinfo(client):
    dbinfo_result = client.einfo(db="protein")

    assert dbinfo_result.count == "1291933024"
    assert dbinfo_result.dbname == "protein"
    assert dbinfo_result.description == "Protein sequence record"
    assert dbinfo_result.menuname == "Protein"
