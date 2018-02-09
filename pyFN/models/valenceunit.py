"""FrameNet Valence Unit."""

__all__ = ['ValenceUnit']


# pylint: disable=C0103
class ValenceUnit():
    """ValenceUnit: Frame Element + Phrase Type + Grammatical Function."""

    def __init__(self, fe, pt=None, gf=None):
        """Constructor."""
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
        """Return FE.PT.GF with FE as FE name."""
        if self._fe.itype:
            return '{}.{}'.format(self._fe.name, self._fe.itype)
        return '{}.{}.{}'.format(self._fe.name, self._pt, self._gf)

    @property
    def with_fe_cnc(self):
        """Return FE.PT.GF with FE as FE.name#C or FE.name#NC.

        C and NC stand for Core and Non-Core. No additionnal specification
        is given as to the type of Non-Core FE.
        """
        if not self._fe.coretype:
            return ''
        if self._fe.itype:
            if self._fe.coretype == 'Core' \
             or self._fe.coretype == 'Core-Unexpressed':
                return '{}#C.{}'.format(self._fe.name, self._fe.itype)
            return '{}#NC.{}'.format(self._fe.name, self._fe.itype)
        if self._fe.coretype == 'Core' \
         or self._fe.coretype == 'Core-Unexpressed':
            return '{}#C.{}.{}'.format(self._fe.name, self._pt, self._gf)
        return '{}#NC.{}.{}'.format(self._fe.name, self._pt, self._gf)

    @property
    def with_fe_coretype(self):
        """Return FE.PT.GF with FE as FE.name#FE.coreType."""
        if not self._fe.coretype:
            return ''
        if self._fe.itype:
            return '{}#{}.{}'.format(self._fe.name, self._fe.coretype,
                                     self._fe.itype)
        return '{}#{}.{}.{}'.format(self._fe.name, self._fe.coretype,
                                    self._pt, self._gf)
