from charms.reactive import when_any
from charms.reactive import Endpoint
from charms.reactive import set_flag, clear_flag


class SGERequires(Endpoint):
    @when_any('endpoint.{endpoint_name}.changed.hostname')
    def new_master(self):
        print("Found new master, connecting...")
        set_flag(self.expand_name('endpoint.{endpoint_name}.new-master'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed.hostname'))

    def masters(self):
        master_nodes = []
        for relation in self.relations:
            for unit in relation.units:
                hostname = unit.received['hostname']
                if not hostname:
                    continue
                master_nodes.append({
                    'hostname': hostname,
                    'relation_id': relation.relation_id,
                    'remote_unit_name': unit.unit_name,
                })
        return master_nodes

