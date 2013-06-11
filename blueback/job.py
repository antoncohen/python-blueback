from blueback.util import ObjectDict, expand_paths
from blueback.defaults import *

class Job(object):
    def __init__(self, config):
        self.config = ObjectDict(config)

    def print_section(self):
        print self.config.section
        print self.config

    def lookup_destination(self):
        if self.config.destination_type not in DESTINATIONS:
            raise AttributeError('Destination type %s not valid.' %
                    self.config.destination_type)

        provider = PROVIDERS[self.config.destination_type]

        return provider

    def lookup_host(self, direction='destination'):
        """Returns s3 host in the form of bucket_name.s3.amazonaws.com"""

        if self.config[direction + '_secure']:
            protocol = 'https'
        else:
            protocol = 'http'

        if self.config[direction + '_type'] == 's3':
            host = (protocol + '://' +
                    self.config[direction + '_container'] + '.s3.amazonaws.com')
            return host
        else:
            return None

        if direction == 'destination':
            if self.config.destination_secure:
                protocol = 'https'
            else:
                protocol = 'http'

            if self.config.desination_type == 's3':
                host = (protocol + '://' +
                        self.config.destination_container + '.s3.amazonaws.com')
                return host
            else:
                return None
        elif direction == 'source':
            if self.config.source_secure:
                protocol = 'https'
            else:
                protocol = 'http'

            if self.config.source_type == 's3':
                host = (protocol + '://' +
                        self.config.source_container + '.s3.amazonaws.com')
                return host
            else:
                return None
        else:
            return None

    def run(self):
        dest_provider, dest_type = self.lookup_destination()
        host = self.lookup_host('destination')

        if self.config.action == 'backup':
            self.backup(dest_provider=dest_provider, dest_type=dest_type,
                    host=host)
        else:
            print 'action not impemented yet'

    def backup(self, dest_provider, dest_type, host):
        import subprocess
        from datetime import datetime

        from libcloud.storage.types import Provider, ContainerDoesNotExistError
        from libcloud.storage.providers import get_driver
        import libcloud.security

        # TODO Make this optional
        libcloud.security.VERIFY_SSL_CERT = False

        print host

        driver = get_driver(getattr(Provider, dest_provider))(self.config.destination_key,
                                  self.config.destination_secret)

        directory = expand_paths([self.config.source_name])
        cmd = 'tar cvzpf - %s' % (' '.join(directory))

        object_name = '%s-%s.tar.gz' % (self.config.destination_prefix, datetime.now().strftime('%Y-%m-%d'))
        container_name = self.config.destination_container

        # Create a container if it doesn't already exist
        try:
            container = driver.get_container(container_name=container_name)
        except ContainerDoesNotExistError:
            container = driver.create_container(container_name=container_name)

        pipe = subprocess.Popen(cmd, bufsize=0, shell=True, stdout=subprocess.PIPE)
        return_code = pipe.poll()

        print 'Uploading object...'

        while return_code is None:
            # Compress data in our directory and stream it directly to CF
            obj = container.upload_object_via_stream(iterator=pipe.stdout,
                                                    object_name=object_name)
            return_code = pipe.poll()

        print 'Upload complete, transferred: %s KB' % ((obj.size / 1024))

