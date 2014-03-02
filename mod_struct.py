""" Return nested members of module/class  """

import inspect
import sys
from collections import defaultdict

def get_entity_type(entity):
    """ Check whether entity is supported for docstring heck """
    for entity_type in ['module', 'function', 'class', 'method'] :
        # inspect module has inspect.ismodule, inspect.isfunction - leverage that
        inspect_func = getattr(inspect, 'is' + entity_type)
        if inspect_func(entity): return entity_type
    raise ValueError('Invalid entity: %s passed' % str(entity))

class Modstruct(object):
    """ Return a data structure representing all members of the passed
    entity """

    def __init__(self, base_entity, **options):
        self.base_entity_type = get_entity_type(base_entity)
        self.base_entity = base_entity
        self.base_module = base_entity
        self.id_name_map = {}
        self.all_members = []
        self.options = {
            'categorize': False
        }
        self.options.update(options)
        if self.base_entity_type != 'module':
            # if entity_type is class - know which module it belongs to
            self.base_module = sys.modules[base_entity.__module__]

    def get_entity_name(self, entity):
        """ Return fully qualified name of entity """
        return self.id_name_map.get(id(entity), None)

    def get_base_entity_name(self):
        """ Return the name of the base entity passed in by the user """
        # if base entity is not a method - just look up its id
        if self.base_entity_type != 'method':
            return self.get_entity_name(self.base_entity)

        # else as method id does not stay constant, cycle through all members 
        # and return the member matching the base entity ref
        for member in self.all_members:
            if self.base_entity == member['ref']:
                return self.get_entity_name(member['ref'])

    def build_id_name_map(self, entity, parent=None):
        """ Map entity id to its fully qualified name """
        entity_name = entity.__name__
        if not parent is None:
            id_parent = id(parent)
            if id_parent in self.id_name_map:
                parent_name = self.id_name_map[id_parent]
                entity_name = '.'.join([parent_name, entity.__name__])
        self.id_name_map[id(entity)] = entity_name

    def extract_entity_members(self):
        """ From all the members extract out member tree of the base 
        entity """
        if self.base_entity_type == 'module':
            self.base_entity_members = self.all_members
            return self.base_entity_members

        base_entity_name = self.get_base_entity_name()

        base_entity_members = []
        for member in self.all_members:
            if member['name'].startswith(base_entity_name):
                base_entity_members.append(member)
        self.base_entity_members = base_entity_members
        return self.base_entity_members

    def categorize(self):
        """ Categorize members based on their type """
        cats = defaultdict(list)
        for member in self.base_entity_members:
            cats[member['type']].append(member)
        return cats

    def get_entity_members(self, entity):
        """ Get first level members of the passed entity """
        members = []
        parent_name = self.get_entity_name(entity)
        for member in inspect.getmembers(entity):
            ref = member[1]
            # member has to be of supported entity type
            try:
                ref_type = get_entity_type(ref)
            except ValueError:
                continue

            # we will not inspect modules imported in base module
            if inspect.ismodule(ref): continue

            # member has to be defined in base module
            if ref.__module__ != self.base_module.__name__: continue

            # valid member - construct member data
            member_data = {
                'type': ref_type, 
                'ref': ref, 
                'name': parent_name + '.' + ref.__name__,
                'parent_ref': entity,
                'parent_name': parent_name,
            }
            members.append(member_data)
            self.build_id_name_map(ref, entity)
        return members

    def get_all_members(self):
        """ Get all the members (nested also) of the passed entity """

        # add base module as the first element
        all_members = [{'type': 'module',
                        'ref': self.base_module, 
                        'name': self.base_module.__name__, 
                        'parent_ref': None,
                        'parent_name': None}]

        # add base module as first entry to id_name_map - root of all names
        self.build_id_name_map(self.base_module, None)

        # get first level members of the module
        nested_members = self.get_entity_members(self.base_module)
        all_members.extend(nested_members)

        # call get_entity_members repetitively till you reach a stage where 
        # there are no nested members
        while nested_members:
            curr_nested_members = []
            # for member_type, member_ref, member_name in nested_members:
            for member_data in nested_members:
                if member_data['type'] == 'class':
                    # drill nested members only in a class
                    members = self.get_entity_members(member_data['ref'])
                    curr_nested_members.extend(members)
            nested_members = curr_nested_members
            all_members.extend(nested_members)

        self.all_members = all_members

        # extract subset of members in case base_entity is not a module
        self.extract_entity_members()

        # categorize members if required
        if self.options['categorize']:
            return self.categorize()

        return self.base_entity_members

def get_members(entity, categorize=False):
    m = Modstruct(entity, categorize=categorize)
    return m.get_all_members()

def main():
    import test_mod
    from pprint import pprint as pp

    pp("--- module and its members -----")
    pp(get_members(test_mod))
    print "\n"

    pp("--- function ----")
    pp(get_members(test_mod.main))
    print "\n"

    pp("--- class and its members -----")
    pp(get_members(test_mod.SpecFile.Section1))
    print "\n"

    pp("--- method ----")
    pp(get_members(test_mod.SpecFile.Section1.validate))
    print "\n"

    pp("--- all classes -----")
    pp(get_members(test_mod, categorize=True)['class'])
    print "\n"

    pp("--- all functions -----")
    pp(get_members(test_mod, categorize=True)['function'])
    print "\n"

    pp("--- all methods -----")
    pp(get_members(test_mod, categorize=True)['method'])
    print "\n"

    pp("--- methods of a specific class -----")
    pp(get_members(test_mod.SpecFile.Section1, categorize=True)['method'])

if __name__ == '__main__':
    main()
