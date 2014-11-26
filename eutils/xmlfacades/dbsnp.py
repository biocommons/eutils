import re

import lxml.etree

from eutils.exceptions import *
import eutils.xmlfacades.base


genome_ac_re = re.compile('^(?:NC)_')
transcript_ac_re = re.compile('^(?:ENST|NG|NM)_')
protein_ac_re = re.compile('^(?:ENSP|NP)_')


class ExchangeSet(eutils.xmlfacades.base.Base):
    def __iter__(self):
        return ( Rs(n)
                 for n in self._xmlroot.iterfind('docsum:Rs',namespaces={'docsum': self._xmlroot.nsmap[None]}) )
    def __len__(self):
        return len( self._xmlroot.findall('docsum:Rs',namespaces={'docsum': self._xmlroot.nsmap[None]}) )


class Rs(object):
    def __init__(self,rs_node):
        assert rs_node.tag == '{http://www.ncbi.nlm.nih.gov/SNP/docsum}Rs'
        self._n = rs_node

    #def __unicode__(self):
    #    return "Rs({self.id})".format(self=self)

    @property
    def rs_id(self):
        return 'rs' + self._n.get('rsId')

    @property
    def withdrawn(self):
        return 'notwithdrawn' not in self._n.get('snpType')
    
    @property
    def orient(self):
        return self._n.get('orient')
    
    @property
    def strand(self):
        return self._n.get('strand')

    @property
    def hgvs_tags(self):
        return self._n.xpath('docsum:hgvs/text()', namespaces={'docsum': self._n.nsmap[None]})

    @property
    def hgvs_genome_tags(self):
        return [ t for t in self.hgvs_tags if genome_ac_re.match(t) ]
    @property
    def hgvs_transcript_tags(self):
        return [ t for t in self.hgvs_tags if transcript_ac_re.match(t) ]
    @property
    def hgvs_protein_tags(self):
        return [ t for t in self.hgvs_tags if protein_ac_re.match(t) ]
