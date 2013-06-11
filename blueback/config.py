import os
# Py3k uses lowercase configparser
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

# argparse is new for 2.7, included is a backport for 2.6
try:
    import argparse
except ImportError:
    import blueback.argparse as argparse

from blueback.defaults import *

def expand_paths(paths):
    fullpaths = []
    for i in paths:
        path = os.path.expanduser(i)
        if os.path.isdir(path):
            contents = os.listdir(path)
            for content in contents:
                if os.path.isfile(os.path.join
                                  (path, content)) and content.endswith('.conf'):
                    fullpaths.append(os.path.join(path, content))
        else:
            fullpaths.append(path)

    return fullpaths


def return_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', action='append')
    parser.add_argument('-a', '--action', choices=ACTIONS)
    parser.add_argument('-d', '--destination-type', choices=DESTINATIONS)
    parser.add_argument('-s', '--source-type', choices=SOURCES)
    parser.add_argument('--destination-secure', choices=BOOLEANS)
    parser.add_argument('--source-secure', choices=BOOLEANS)
    parser.add_argument('--destination-key')
    parser.add_argument('--source-key')
    parser.add_argument('--destination-secret')
    parser.add_argument('--source-secret')
    parser.add_argument('--destination-container')
    parser.add_argument('--source-container')
    parser.add_argument('--destination-path')
    parser.add_argument('--source-path')
    parser.add_argument('--destination-prefix')
    parser.add_argument('--source-name')

    # Setting defaults here will return them when parsed and override
    # .conf settings in return_section_configs()
    #parser.set_defaults(**DEFAULTS)
    argsobj, sections = parser.parse_known_args()
    args = vars(argsobj)

    # Removing default None values so they don't override .conf values
    for k, v in args.items():
        if v == None: del args[k]

    return args, sections


def return_section_configs(configs=None, sections=None, args=None):
    if configs == None:
        configs = expand_paths(['/etc/blueback.conf', '/etc/blueback.d/'])
    elif isinstance(configs, basestring):
        configs = expand_paths([configs])
    else:
        configs = expand_paths(configs)

    if isinstance(sections, basestring):
        sections = [sections]

    configlist = []

    config = configparser.SafeConfigParser()
    config.read(configs)

    if config.has_section('main'):
        has_main = True
        mainsec = dict(config.items('main'))
    else:
        has_main = False

    if sections:
        for section in sections:
            sectionconfig = {'section': section}
            sectionconfig.update(DEFAULTS)
            if has_main: sectionconfig.update(mainsec)
            sectionconfig.update(dict(config.items(section)))
            if args: sectionconfig.update(args)

            configlist.append(sectionconfig)
    else:
        sectionconfig = dict(**DEFAULTS)
        if has_main:
            sectionconfig.update({'section': 'main'})
            sectionconfig.update(mainsec)
        else:
            sectionconfig.update({'section': 'cmdline'})

        if args: sectionconfig.update(args)

        configlist.append(sectionconfig)

    return configlist


def get_config():
    args, sections = return_args()

    if 'conf' in args:
        configs = args['conf']
    else:
        configs = None

    configlist = return_section_configs(configs=configs,
                                        sections=sections,
                                        args=args)

    return configlist
