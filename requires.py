from charms.reactive import when_any
from charms.reactive import Endpoint


class SGERequires(Endpoint):
    @when_any('endpoint.sge-cluster-master.changed.hostname')
    def new_master(self):
        set_flag(self.expand_name('endpoint.{endpoint_name}.new-website'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed.hostname'))

    def master(self):
        master_nodes = []
        for relation in self.relations:
            for unit in relation.units:
                hostname = unit.received['hostname']
                if not hostname:
                    continue
                masters.append({
                    'hostname': hostname,
                    'relation_id': relation.relation_id,
                    'remote_unit_name': unit.unit_name,
                })
        return master_nodes

