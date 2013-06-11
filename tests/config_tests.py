import os

from nose.tools import *

from blueback.config import *

def test_expand_paths():
    paths1 = ['/etc/hosts', 'tests/conf.d']
    paths2 = ['./tests/conf.d']
    paths3 = ['~/78hjksj3ds', './tests/test.conf']
    paths4 = ['tests/test.conf']

    fullpaths1 = expand_paths(paths1)
    fullpaths2 = expand_paths(paths2)
    fullpaths3 = expand_paths(paths3)
    fullpaths4 = expand_paths(paths4)

    eq_(fullpaths1, ['/etc/hosts',
                     'tests/conf.d/empty.conf',
                     'tests/conf.d/section1.conf'])
    eq_(fullpaths2, ['./tests/conf.d/empty.conf',
                     './tests/conf.d/section1.conf'])
    eq_(fullpaths3, [os.path.expanduser('~') + '/78hjksj3ds',
                     './tests/test.conf'])
    assert_not_equal(fullpaths4, '[tests/test.conf]')

