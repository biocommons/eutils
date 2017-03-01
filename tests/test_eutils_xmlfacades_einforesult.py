import vcr


@vcr.use_cassette
def test_einfo_dblist(client):
    dblist_result = client.einfo()

    assert 'protein' in dblist_result.databases
    assert 48 == len(dblist_result.databases)


@vcr.use_cassette
def test_einfo_dbinfo(client):
    dbinfo_result = client.einfo(db="protein")

    assert "370927433" == dbinfo_result.count
    assert "protein" == dbinfo_result.dbname
    assert "Protein sequence record" == dbinfo_result.description
    assert "Protein" == dbinfo_result.menuname
