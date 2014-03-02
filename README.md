mod_struct
==========


Rationale behind creation: <a href=" http://curiosityhealsthecat.blogspot.in/2014/02/lessons-learnt-while-automating.html" target="_blank"> Lessons learnt while automating docstring checking </a>

Long story short: Get fully qualified names and other info about members of a module/class. 

As of now, it inspects functions, classes under a module and methods, nested classes under a class.

Usage:
=====

``` 
>>> import mod_struct

>>> import os # import the module which you want to inspect

>>> mod_struct.get_members(os) # return all the members nested under this module (including this module)

[{'name': 'os',
  'parent_name': None,
  'parent_ref': None,
  'ref': <module 'os' from '/usr/lib/python2.7/os.pyc'>,
  'type': 'module'},
 {'name': 'os._Environ',
  'parent_name': 'os',
  'parent_ref': <module 'os' from '/usr/lib/python2.7/os.pyc'>,
  'ref': os._Environ,
  'type': 'class'},
 {'name': 'os._execvpe',
  'parent_name': 'os',
  'parent_ref': <module 'os' from '/usr/lib/python2.7/os.pyc'>,
  'ref': <function os._execvpe>,
  'type': 'function'},
 {'name': 'os._Environ.update',
  'parent_name': 'os._Environ',
  'parent_ref': os._Environ,
  'ref': <unbound method _Environ.update>,
  'type': 'method'}
 .
 .
 .

>>> mod_struct.get_members(os._Environ) # return all the members nested under this class (including this class)

[{'name': 'os._Environ',
  'parent_name': 'os',
  'parent_ref': <module 'os' from '/usr/lib/python2.7/os.pyc'>,
  'ref': os._Environ,
  'type': 'class'},
 {'name': 'os._Environ.__delitem__',
  'parent_name': 'os._Environ',
  'parent_ref': os._Environ,
  'ref': <unbound method _Environ.__delitem__>,
  'type': 'method'},
 {'name': 'os._Environ.__init__',
  'parent_name': 'os._Environ',
  'parent_ref': os._Environ,
  'ref': <unbound method _Environ.__init__>,
  'type': 'method'},
 {'name': 'os._Environ.__setitem__',
  'parent_name': 'os._Environ',
  'parent_ref': os._Environ,
  'ref': <unbound method _Environ.__setitem__>,
  'type': 'method'},
 .
 .
 .

>>> x = os.walk

>>> mod_struct.get_members(x) # given a ref - get info about its type, name, etc.

[{'name': 'os.walk',
  'parent_name': 'os',
  'parent_ref': <module 'os' from '/usr/lib/python2.7/os.pyc'>,
  'ref': <function os.walk>,
  'type': 'function'}]

>>> mod_struct.get_members(os, categorize=True).keys() # member categories

['function', 'class', 'module', 'method']

>>> mod_struct.get_members(os, categorize=True)['class'] # return all class related info

[{'name': 'os._Environ',
  'parent_name': 'os',
  'parent_ref': <module 'os' from '/usr/lib/python2.7/os.pyc'>,
  'ref': os._Environ,
  'type': 'class'}]

>>> mod_struct.get_members(os, categorize=True)['function'] # return all function related info

[{'name': 'os._execvpe',
  'parent_name': 'os',
  'parent_ref': <module 'os' from '/usr/lib/python2.7/os.pyc'>,
  'ref': <function os._execvpe>,
  'type': 'function'},
 {'name': 'os._exists',
  'parent_name': 'os',
  'parent_ref': <module 'os' from '/usr/lib/python2.7/os.pyc'>,
  'ref': <function os._exists>,
  'type': 'function'},
 .
 .
 .

>>> mod_struct.get_members(os, categorize=True)['method'] # return all method related info

[{'name': 'os._Environ.__delitem__',
  'parent_name': 'os._Environ',
  'parent_ref': os._Environ,
  'ref': <unbound method _Environ.__delitem__>,
  'type': 'method'},
 {'name': 'os._Environ.__init__',
  'parent_name': 'os._Environ',
  'parent_ref': os._Environ,
  'ref': <unbound method _Environ.__init__>,
  'type': 'method'},
 .
 .
 .

>>> import test_mod 

>>> mod_struct.get_members(test_mod.SpecFile.StaticSection, categorize = True)['method'] # return methods of a specific class

[{'name': 'test_mod.SpecFile.StaticSection.__init__',
  'parent_name': 'test_mod.SpecFile.StaticSection',
  'parent_ref': test_mod.StaticSection,
  'ref': <unbound method StaticSection.__init__>,
  'type': 'method'},
 {'name': 'test_mod.SpecFile.StaticSection.validate',
  'parent_name': 'test_mod.SpecFile.StaticSection',
  'parent_ref': test_mod.StaticSection,
  'ref': <unbound method StaticSection.validate>,
  'type': 'method'}]

``` 
