#import eutils.client

import os

import eutils.resp.gene
import eutils.resp.pubmed
import eutils.resp.refseq

data_dir = os.path.realpath(os.path.join(__file__,'..','tests/data'))
gene_xml = open(os.path.join(data_dir,'efetch.fcgi?retmode=xml&db=gene&id=4747.xml')).read()
pubmed_xml = open(os.path.join(data_dir,'efetch.fcgi?rettype=xml&db=pubmed&id=20412080.xml')).read()
rs_xml = open(os.path.join(data_dir,'efetch.fcgi?db=nuccore&id=148536845&retmode=xml.xml')).read()

g = eutils.resp.gene.Gene(gene_xml)
pm = eutils.resp.pubmed.PubMedArticle(pubmed_xml)
rs = eutils.resp.refseq.RefSeq(rs_xml)
