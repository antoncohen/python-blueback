from blueback.util import ObjectDict

DEFAULTS = ObjectDict({
    'action': 'backup',
    'conf': ['/etc/blueback.conf', '/etc/blueback.d'],
    'destination_secure': True,
    'source_secure': True,
    })

ACTIONS = ('backup', 'restore')

BOOLEANS = ('true', 'false')

DESTINATIONS = ('s3', 's3-us-east-1', 's3-us-west-1', 's3-us-west-2',
                'cloudfiles')

SOURCES = ('directory',)

# TODO add more regions from:
# https://github.com/apache/libcloud/blob/trunk/libcloud/storage/providers.py
# https://github.com/boto/boto/blob/develop/boto/s3/connection.py
# This is a stupid amount of absraction, just use names from:
# https://github.com/apache/libcloud/blob/trunk/libcloud/storage/types.py
PROVIDERS = ObjectDict({
    's3': ('S3', 'cloud'),
    's3-us-east-1': ('S3', 'cloud'),
    's3-us-west-1': ('S3_US_WEST', 'cloud'),
    's3-us-west-2': ('S3_US_WEST_OREGON', 'cloud'),
    'cloudfiles': ('CLOUDFILES_US', 'cloud'),
    })
