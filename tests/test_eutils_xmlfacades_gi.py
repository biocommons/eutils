import vcr


@vcr.use_cassette
def test_esearchresult(client):
    r = next(iter(client.efetch(db="nuccore", id="NM_152783.3")))

    # in #150 fails with AttributeError: 'GBSeq' object has no attribute 'seqids'
    assert r.gi == 119964727

    # test for some additional bugs that were fixed together with #150
    assert len(r.features.cds.db_xrefs) == 4

    for s in ["CCDS:CCDS33426.1", "GeneID:728294", "HGNC:HGNC:28358", "MIM:609186"]:
        assert s in r.features.cds.db_xrefs

    prot = (
        "MLPRRPLAWPAWLLRGAPGAAGSWGRPVGPLARRGCCSAPGTPE"
        "VPLTRERYPVRRLPFSTVSKQDLAAFERIVPGGVVTDPEALQAPNVDWLRTLRGCSKV"
        "LLRPRTSEEVSHILRHCHERNLAVNPQGGNTGMVGGSVPVFDEIILSTARMNRVLSFH"
        "SVSGILVCQAGCVLEELSRYVEERDFIMPLDLGAKGSCHIGGNVATNAGGLRFLRYGS"
        "LHGTVLGLEVVLADGTVLDCLTSLRKDNTGYDLKQLFIGSEGTLGIITTVSILCPPKP"
        "RAVNVAFLGCPGFAEVLQTFSTCKGMLGEILSAFEFMDAVCMQLVGRHLHLASPVQES"
        "PFYVLIETSGSNAGHDAEKLGHFLEHALGSGLVTDGTMATDQRKVKMLWALRERITEA"
        "LSRDGYVYKYDLSLPVERLYDIVTDLRARLGPHAKHVVGYGHLGDGNLHLNVTAEAFS"
        "PSLLAALEPHVYEWTAGQQGSVSAEHGVGFRKRDVLGYSKPPGALQLMQQLKALLDPK"
        "GILNPYKTLPSQA"
    )
    assert prot == r.features.cds.translation

    # this returns the ranges
    exons = r.exons
    assert len(exons) == 10

    # this returns GBFeatureExon objects
    exon = next(iter(r.features.exons))
    assert exon.inference == "alignment:Splign:1.39.8"
