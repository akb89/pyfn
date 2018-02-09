"""A class to store different format of valence pattern."""

__all__ = ['ValencePattern']


def _pt_key(valence_unit):
    return valence_unit.fe.itype if valence_unit.fe.itype else valence_unit.pt


def _sorted_valence_units(valence_units):
    return sorted(valence_units, key=lambda x: (x.fe.name, _pt_key(x), x.gf))


class ValencePattern():
    """ValencePattern."""

    def __init__(self, valence_units):
        """Constructor."""
        self._valence_units = valence_units

    @property
    def valence_units(self):
        """Return a list of valence units."""
        return self._valence_units

    @property
    def with_fe_name(self):
        """Return a stringified list of FE.PT.GF strings.

        The FrameElement fe follows: 'fe.name'
        """
        valence_pattern = ''
        if not self._valence_units:
            return valence_pattern
        for valence_unit in _sorted_valence_units(self._valence_units):
            valence_pattern = '{} {}'.format(valence_pattern,
                                             valence_unit.with_fe_name)
        return valence_pattern.strip()

    @property
    def with_fe_cnc(self):
        """Return a stringified list of FE.PT.GF strings.

        The FrameElement fe follows: 'fe.name#C' is the FrameElement is core
        or 'fe.name#NC' if the FrameElement is non-core
        """
        valence_pattern = ''
        if not self._valence_units:
            return valence_pattern
        for valence_unit in _sorted_valence_units(self._valence_units):
            valence_pattern = '{} {}'.format(valence_pattern,
                                             valence_unit.with_fe_cnc)
        return valence_pattern.strip()

    @property
    def with_fe_coretype(self):
        """Return a stringified list of FE.PT.GF strings.

        The FrameElement FE follows: 'fe.name#fe.coretype'
        """
        valence_pattern = ''
        if not self._valence_units:
            return valence_pattern
        for valence_unit in _sorted_valence_units(self._valence_units):
            valence_pattern = '{} {}'.format(valence_pattern,
                                             valence_unit.with_fe_coretype)
        return valence_pattern.strip()
