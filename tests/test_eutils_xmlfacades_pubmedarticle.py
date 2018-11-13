import vcr

@vcr.use_cassette
def test_eutils_xmlfacades_pubmedarticle_22528466(client):
    pas = client.efetch(db="pubmed", id=22528466)
    pa = next(iter(pas))

    assert pa.abstract.startswith(u'Methods necessary for the successful transformation and regeneration of Aloe vera were developed and used to express the human protein, interferon alpha 2 (IFN\u03b12).')
    assert set(pa.authors) == set(["Lowther W",
                                   "Lorick K",
                                   "Lawrence SD",
                                   "Yeow WS"])
    assert set(pa.chemicals) == set(["Antiviral Agents",
                                     "IFNA2 protein, human",
                                     "Interferon-alpha",
                                     "Plant Extracts",
                                     "Glucuronidase"])
    assert pa.doi == "10.1007/s11248-012-9616-0"
    assert pa.issue == "6"
    assert pa.jrnl == "Transgenic Res."
    assert set(pa.mesh_headings) == set(["Aloe",
                                         "Antiviral Agents",
                                         "Encephalomyocarditis virus",
                                         "Genome, Plant",
                                         "Glucuronidase",
                                         "Humans",
                                         "Immunoblotting",
                                         "Interferon-alpha",
                                         "Plant Extracts",
                                         "Plant Leaves",
                                         "Plants, Genetically Modified",
                                         "Seeds",
                                         "Signal Transduction",
                                         "Transgenes"])
    assert set(pa.mesh_qualifiers) == set(["chemistry",
                                           "genetics",
                                           "pharmacology",
                                           "drug effects",
                                           "genetics",
                                           "metabolism",
                                           "genetics",
                                           "metabolism",
                                           "pharmacology",
                                           "drug effects",
                                           "genetics",
                                           "chemistry",
                                           "drug effects",
                                           "physiology"])
    assert pa.pages == "1349-57"
    assert pa.pii is None
    assert pa.pmc is None
    assert pa.pmid == "22528466"
    assert set(pa.pub_types) == set(["Journal Article",
                                    "Research Support, U.S. Gov't, Non-P.H.S."])
    assert pa.title == "Expression of biologically active human interferon alpha 2 in Aloe vera."
    assert pa.volume == "21"
    assert pa.year == "2012"
    assert "PubmedArticle(22528466" in str(pa)

@vcr.use_cassette
def test_eutils_xmlfacades_pubmedarticle_20412080(client):
    pas = client.efetch(db="pubmed", id=20412080)
    pa = next(iter(pas))

    assert pa.abstract.startswith('A standardized, controlled vocabulary allows phenotypic')
    assert set(pa.authors) == set(['Robinson PN', 'Mundlos S'])
    assert set(pa.chemicals) == set([])
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
    assert set(pa.mesh_qualifiers) == set(["methods"])
    assert pa.pages == '525-34'
    assert pa.pii == 'CGE1436'
    assert pa.pmc is None
    assert pa.pmid == '20412080'
    assert set(pa.pub_types) == set(["Journal Article", "Review"])
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


@vcr.use_cassette
def test_eutils_xmlfacades_pubmedarticle_29915538(client):
    pas = client.efetch(db="pubmed", id=29915538)
    pa = next(iter(pas))
    assert pa.abstract.startswith("Background: Semaglutide, a newly once-weekly glucagon like peptide-1 (GLP-1)")
    assert pa.abstract.endswith("GLP-1 receptor agonists of exenatide release and dulaglutide.")
    assert "Semaglutide" in pa.abstract
    assert "Results" in pa.abstract
    assert "P < 0.001" in pa.abstract
