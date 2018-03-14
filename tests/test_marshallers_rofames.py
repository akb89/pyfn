import os

import pyfn.marshalling.unmarshallers.framenet as framenet
import pyfn.marshalling.marshallers.semafor as semafor


LU_XML_FILE = os.path.join(os.path.dirname(__file__), 'resources',
                           'lu', 'lu1.xml')
ex_annosets_list = list(framenet._unmarshall_exemplar_xml(LU_XML_FILE, {}))

def test():
    pass
    # for annosets in ex_annosets_list:
    #     for annoset in annosets:
    #         print(semafor._get_frame_fe_num(annoset))
    #         print(semafor._get_fe_chunks(annoset))
    #         for label in annoset.labelstore.labels_by_layer_name['FE']:
    #             print(label)
