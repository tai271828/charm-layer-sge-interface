from charms.reactive import when_any
from charms.reactive import Endpoint
from charms.reactive import set_flag, clear_flag
from charmhelpers.core import hookenv


class SGERequires(Endpoint):
    @when_any('endpoint.{endpoint_name}.changed.hostname')
    def new_exchanger(self):
        print("Found an new master, connecting...")
        set_flag(self.expand_name('endpoint.{endpoint_name}.new-exchanger'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed.hostname'))


    def exchangers(self):
        exchanger_nodes = []
        for relation in self.relations:
            for unit in relation.units:
                hostname = unit.received['hostname']
                if not hostname:
                    continue
                exchanger_nodes.append({
                    'hostname': hostname,
                    'relation_id': relation.relation_id,
                    'remote_unit_name': unit.unit_name,
                })
        return exchanger_nodes


    def publish_info(self, hostname=None):
        for relation in self.relations:
            print("A requirer is publishing its config...")
            relation.to_publish['hostname'] = hostname or\
            hookenv.unit_get('public_address')

