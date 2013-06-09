class Resp(object):
    def _get_node(self,tag):
        return self.doc.find(tag)
    def _get_text(self,tag):
        n = self._get_node(tag)
        return None if n is None else n.text
