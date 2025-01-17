#!/user/bin/env python
'''advancedQuery.py

This filter runs an RCSB PDB Advanced Search web service using a JSON query
description.

References
----------
- `Advanced Search Query <https://www.rcsb.org/pdb/staticHelp.do?p=help/advancedSearch.html>`_

Examples
--------
Find PDB entries that contain the word "mutant" in the structure title:

>>> query = "<orgPdbQuery>" + \
...         "<queryType>org.pdb.query.simple.StructTitleQuery</queryType>" + \
...         "<struct.title.comparator>contains</struct.title.comparator>" + \
...         "<struct.title.value>mutant</struct.title.value" + \
... "</orgPdbQuery>"
>>> pdb = pdb.filter(AdvancedSearch(query));

'''
__author__ = "Mars (Shih-Cheng) Huang"
__maintainer__ = "Mars (Shih-Cheng) Huang"
__email__ = "marshuang80@gmail.com"
__version__ = "0.2.0"
__status__ = "Done"

from mmtfPyspark.webservices.advancedQueryService import post_query


class AdvancedQuery(object):
    '''Filters using the RCSB PDB Advanced Search web service

    Attributes
    ----------
    query : str
            query in RCSB PDB JSON format
    '''

    def __init__(self, query):

        result_type, results, scores = post_query(query)
        self.result_type = result_type
        #self.entityLevel = (len(results) > 0) and (":" in results[0])
        self.entityLevel = result_type == 'polymer_entity'

        #print('result_type:', result_type, 'entityLevel:', self.entityLevel)
        self.structureIds = list(set(results))
        #print('structureIds:', self.structureIds)
        self.exclusive = False

    def get_structure_ids(self):
        return list(self.structureIds)

    def get_result_type(self):
        return self.result_type

    def __call__(self, t):

        structure = t[1]

        globalMatch = False
        numChains = structure.chains_per_model[0]
        entityChainIndex = self._get_chain_to_entity_index(structure)

        for i in range(numChains):

            ID = t[0]

            if self.entityLevel:
                ID = self._get_structure_entity_id(
                    structure, ID, entityChainIndex[i])

            match = ID in self.structureIds
        #    if match:
        #        print("matched ID", ID)

            if match and not self.exclusive:
                return True

            if not match and self.exclusive:
                return False

            if match:
                globalMatch = True

        return globalMatch

    def _get_structure_entity_id(self, structure, origStructureId, origEntityId):

        keyStructureId = origStructureId

        try:
            index = keyStructureId.index(".")
            #index = keyStructureId.index("_")
            keyStructureId = keyStructureId[:index]
        except:
            pass

        try:
        #    print("structure.structure_id:", structure.structure_id)
            pos = structure.structure_id.rindex(".")

            valueStructureId = structure.structure_id[:structure.structure_id.index(
                ".")]

        #    print("key/valueStructureId:", keyStructureId, valueStructureId)
            if keyStructureId != valueStructureId:
                raise Exception("Structure mismatch: key vs value: %s vs. %s"
                                % (keyStructureId, valueStructureId))

            entityId = structure.structure_id[pos + 1:]
        #    print("entityId:", entityId)
            # ID = valueStructureId + ":" + entityId
            ID = valueStructureId + "_" + entityId

        except:
            # ID = keyStructureId + ":" + str(origEntityId + 1)
            ID = keyStructureId + "_" + str(origEntityId + 1)

        return ID

    def _get_chain_to_entity_index(self, structure):

        entityChainIndex = [0] * structure.num_chains

        for i in range(len(structure.entity_list)):

            for j in structure.entity_list[i]['chainIndexList']:

                entityChainIndex[j] = i

        return entityChainIndex
