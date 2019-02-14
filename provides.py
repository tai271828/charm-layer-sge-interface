from charms.reactive import when_any
from charms.reactive import Endpoint
from charms.reactive import set_flag, clear_flag
from charmhelpers.core import hookenv


class SGEProvides(Endpoint):
    @when_any('endpoint.{endpoint_name}.changed.unit_public_ip')
    def new_exchanger(self):
        print("Found an new client, connecting...")
        set_flag(self.expand_name('endpoint.{endpoint_name}.new-exchanger'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed.unit_public_ip'))

    def exchangers(self):
        exchanger_nodes = []
        for relation in self.relations:
            for unit in relation.units:
                unit_public_ip = unit.received['unit_public_ip']
                unit_private_ip = unit.received['unit_private_ip']
                if not unit_public_ip:
                    continue
                exchanger_nodes.append({
                    'unit_public_ip': unit_public_ip,
                    'unit_private_ip': unit_private_ip,
                    'relation_id': relation.relation_id,
                    'remote_unit_name': unit.unit_name,
                })
        return exchanger_nodes

    def publish_info_public_ip(self, address):
        for relation in self.relations:
            relation.to_publish['unit_public_ip'] = address or\
            hookenv.unit_get('public_address')
            info = relation.to_publish['unit_public_ip']
            message_template = 'A provider is publishing its public IP: {}'
            hookenv.log(message_template.format(info))

    def publish_info_private_ip(self, address):
        for relation in self.relations:
            relation.to_publish['unit_private_ip'] = address or\
            hookenv.unit_get('private_address')
            info = relation.to_publish['unit_private_ip']
            message_template = 'A provider is publishing its private IP: {}'
            hookenv.log(message_template.format(info))

    def publish_info_mpi(self, mpi_hosts=None):
        for relation in self.relations:
            hookenv.log("Publishing MPI host list...")
            relation.to_publish['mpi_hosts'] = mpi_hosts

