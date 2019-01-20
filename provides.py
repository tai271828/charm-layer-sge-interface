from charmhelpers.core import hookenv
from charms.reactive import Endpoint


class SGEProvides(Endpoint):
    def publish_info(self, hostname=None):
        for relation in self.relations:
            print("A master is publishing its config...")
            relation.to_publish['hostname'] = hostname or\
            hookenv.unit_get('private_address')

