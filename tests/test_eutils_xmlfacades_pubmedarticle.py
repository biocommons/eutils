import vcr


@vcr.use_cassette
def test_eutils_xmlfacades_pubmedarticle_20412080(client):
    pas = client.efetch(db="pubmed", id=20412080)
    pa = next(iter(pas))

    assert pa.abstract.startswith('A standardized, controlled vocabulary allows phenotypic')
    assert set(pa.authors) == set(['Robinson PN', 'Mundlos S'])
    assert pa.doi == '10.1111/j.1399-0004.2010.01436.x'
    assert pa.issue == '6'
    assert pa.jrnl == 'Clin. Genet.'
    assert set(pa.mesh_headings) == set(['Algorithms',
                                          'Computational Biology',
                                          'Databases, Genetic',
                                          'Gene Expression',
                                          'Humans',
                                          'Phenotype',
                                          'Vocabulary, Controlled'])
    assert pa.pages == '525-34'
    assert pa.pii == 'CGE1436'
    assert pa.pmc is None
    assert pa.pmid == '20412080'
    assert pa.title == 'The human phenotype ontology.'
    assert pa.volume == '77'
    assert pa.year == '2010'
    assert 'PubmedArticle(20412080' in str(pa)


@vcr.use_cassette
def test_eutils_xmlfacades_pubmedarticle_23121403(client):
    pas = client.efetch(db="pubmed", id=23121403)
    pa = next(iter(pas))
    assert 'ASPIRE Investigators' in pa.authors


@vcr.use_cassette
def test_eutils_xmlfacades_pubmedarticle_22351513(client):
    pas = client.efetch(db="pubmed", id=22351513)
    pa = next(iter(pas))
    assert 'Mahmooduzzafar' in pa.authors
    assert pa.abstract.startswith("The oil content and fatty acid composition")
    assert pa.abstract.endswith("edible vegetable oil after toxicological studies.")
