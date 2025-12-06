import vcr


@vcr.use_cassette
def test_einfo_dblist(client):
    dblist_result = client.einfo()

    assert "assembly" in dblist_result.databases  # noqa: S101
    assert "protein" in dblist_result.databases  # noqa: S101
    assert "snp" in dblist_result.databases  # noqa: S101


@vcr.use_cassette
def test_einfo_dbinfo(client):
    dbinfo_result = client.einfo(db="protein")

    assert dbinfo_result.count == "1291933024"  # noqa: S101
    assert dbinfo_result.dbname == "protein"  # noqa: S101
    assert dbinfo_result.description == "Protein sequence record"  # noqa: S101
    assert dbinfo_result.menuname == "Protein"  # noqa: S101
