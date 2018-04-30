import vcr


@vcr.use_cassette
def test_eutils_xmlfacades_pubmedcentralarticle_PMC3299399(client):
    pas = client.efetch(db="pmc", id=3299399)
    pa = next(iter(pas))

    assert pa.pmc == '3299399'
    assert pa.pmid == '22416237'
    assert pa.doi == '10.3389/fpsyt.2012.00018'
    assert pa.title == 'The Effects of Psychosis Risk Variants on Brain Connectivity: A Review'
    assert 'It is characterized by hallucinations and delusions, reduced emotion and cognitive impairment' in pa.body_text
    assert 'PubmedCentralArticle(pmc=3299399;pmid=22416237;doi=10.3389/fpsyt.2012.00018;The Effects of Psychosis Risk Variants on Brain Connectivity: A Review)' in str(pa)
