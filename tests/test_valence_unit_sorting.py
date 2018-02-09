"""Testing sorting of ValenceUnit objects."""

import pyfn.models.valencepattern as valencepattern
from pyfn.models.frameelement import FrameElement
from pyfn.models.valenceunit import ValenceUnit

def test_sorted_valence_units():
    fe1 = FrameElement(_id=1, name='A', coretype='Core')
    fe2 = FrameElement(_id=2, name='B', coretype='Core')
    fe3 = FrameElement(_id=3, name='A', coretype='Core', itype='INI')
    fe4 = FrameElement(_id=3, name='A', coretype='Core', itype='CNI')
    vu1 = ValenceUnit(fe=fe3)
    vu2 = ValenceUnit(fe=fe4)
    vu3 = ValenceUnit(fe=fe1, pt='DP', gf='Ext')
    vu4 = ValenceUnit(fe=fe1, pt='DP', gf='Obj')
    vu5 = ValenceUnit(fe=fe2, pt='AN', gf='AN')

    vus = [vu1, vu2, vu4, vu5, vu3]  # A.INI A.CNI A.DP.Obj B.AN.AN A.DP.Ext
    sorted_vus = valencepattern._sorted_valence_units(vus)  # A.CNI A.DP.Ext A.DP.Obj A.INI B.AN.AN
    assert sorted_vus[0] == vu2
    assert sorted_vus[1] == vu3
    assert sorted_vus[2] == vu4
    assert sorted_vus[3] == vu1
    assert sorted_vus[4] == vu5
