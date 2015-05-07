from eutils.xmlfacades.base import Base

class SeqInterval(Base):

    _root_tag = 'Seq-interval'

    def __unicode__(self):
        return 'TODO'

    @property
    def interval_from(self):
        return int(self._xmlroot.findtext('Seq-interval_from'))

    @property
    def interval_to(self):
        return int(self._xmlroot.findtext('Seq-interval_to'))

    @property
    def strand(self):
        nastrand = int(self._xmlroot.find('Seq-interval_strand/Na-strand').get('value'))
        return 1 if nastrand == 'plus' else -1 if nastrand == 'minus' else None

    @property
    def gi(self):
        return int(self._xmlroot.findtext('Seq-interval_id/Seq-id/Seq-id_gi'))
