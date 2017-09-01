"""FrameNet Valence Unit."""

__all__ = ['ValenceUnit']


class ValenceUnit():
    "ValenceUnit: Frame Element + Phrase Type + Grammatical Function."

    def __init__(self, fe, pt=None, gf=None):
        self._fe = fe
        self._pt = pt
        self._gf = gf

    @property
    def fe(self):
        """Return a FrameElement object."""
        return self._fe

    @property
    def pt(self):
        """Return a string for the phrase type."""
        return self._pt

    @property
    def gf(self):
        """Return a string for the grammatical function."""
        return self._gf

    @property
    def with_fe_name(self):
        if self._fe.itype:
            return '{}.{}'.format(self._fe.name, self._fe.itype)
        return '{}.{}.{}'.format(self._fe.name, self._pt, self._gf)

    @property
    def with_fe_cnc(self):
        if not self._fe.coretype:
            return ''
        if self._fe.itype:
            if self._fe.coretype == 'Core':
                return '{}#C.{}'.format(self._fe.name, self._fe.itype)
            return '{}#NC.{}'.format(self._fe.name, self._fe.itype)
        if self._fe.coretype == 'Core':
            return '{}#C.{}.{}'.format(self._fe.name, self._pt, self._gf)
        return '{}#NC.{}.{}'.format(self._fe.name, self._pt, self._gf)

    @property
    def with_fe_coretype(self):
        if not self._fe.coretype:
            return ''
        if self._fe.itype:
            return '{}#{}.{}'.format(self._fe.name, self._fe.coretype,
                                     self._fe.itype)
        return '{}#{}.{}.{}'.format(self._fe.name, self._fe.coretype,
                                    self._pt, self._gf)
