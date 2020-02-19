#!/usr/bin/env python

# python cascade-delete.py --admin_user neutron --admin_password mypass --admin_tenant_name service --openstack_ip wpc-load-balancer-1.cedev21.d103.eng.pdx.wd --dry-run e8f30c96-875d-46a9-b27b-eda13e0889bd

from __future__ import print_function
import argparse
import ConfigParser
import sys
import time

from cfgm_common.exceptions import ResourceExhaustionError
from networkx import DiGraph
from vnc_api.vnc_api import VncApi
from vnc_api.gen.resource_client import *


def get_back_refs(resource, graph, depth=0):
    try:
        object = getattr(vnc_api, '%s_read' % resource[0])(id=resource[1])
    except Exception as e:
        exit("Cannot read %s: %s" %
             (resource[0].replace('_', ' ').title(), str(e)))
    print("lookup child/back reference (graph size %d, depth %d)" %
          (len(graph), depth), end="\r")
    if resource not in graph:
        graph.add_node(resource)

    for back_ref_field, (back_ref_type, _, _) in\
            object.backref_field_types.items():
        back_ref_type = back_ref_type.replace('-', '_')
        for back_ref in getattr(object, 'get_%s' % back_ref_field,
                                lambda: [])() or []:
            try:
                back_ref_object = getattr(vnc_api, '%s_read' % back_ref_type)(
                    id=back_ref['uuid'])
            except Exception as e:
                print("Cannot read %s back-ref: %s" %
                      (back_ref_type.replace('_', ' ').title(), str(e)))
                continue
            back_ref = (back_ref_type, back_ref_object.uuid)
            if back_ref not in graph:
                graph.add_node(back_ref)
            if (resource, back_ref) not in graph.in_edges(back_ref):
                graph.add_edge(back_ref, resource)
            if graph.in_edges(back_ref):
                continue
            graph = get_back_refs(back_ref, graph, depth+1)

    for child_ref_field, (child_ref_type, _) in\
            object.children_field_types.items():
        child_ref_type = child_ref_type.replace('-', '_')
        for child_ref in getattr(object, 'get_%s' % child_ref_field,
                                 lambda: [])() or []:
            try:
                child_object = getattr(vnc_api, '%s_read' % child_ref_type)(
                    id=child_ref['uuid'])
            except Exception as e:
                print("Cannot read %s child: %s" %
                      (child_ref_type.replace('_', ' ').title(), str(e)))
                continue
            child_ref = (child_ref_type, child_object.uuid)
            if child_object not in graph:
                graph.add_node(child_ref)
            if (resource, child_ref) not in graph.in_edges(child_ref):
                graph.add_edge(child_ref, resource)
            if graph.in_edges(child_ref):
                continue
            graph = get_back_refs(child_ref, graph, depth+1)

    return graph


if __name__ == "__main__":
    defaults = {
        'api_server_ip': '127.0.0.1',
        'api_server_port': '8082',
    }
    keystone = {
        'admin_user': 'admin',
        'admin_password': 'contrail123',
        'admin_tenant_name': 'admin',
    }
    conf_parser = argparse.ArgumentParser(add_help=False)
    conf_parser.add_argument(
        "-c", "--conf-file",
        default="/etc/contrail/contrail-api.conf",
        help="Specify config file",
        metavar="FILE")
    args, remaining_argv = conf_parser.parse_known_args(sys.argv[1:])

    if args.conf_file:
        config = ConfigParser.SafeConfigParser()
        config.read([args.conf_file])
        if 'DEFAULTS' in config.sections():
            defaults.update(dict(config.items("DEFAULTS")))
        if 'KEYSTONE' in config.sections():
            keystone.update(dict(config.items("KEYSTONE")))

    # Override with CLI options
    # Don't surpress add_help here so it will handle -h
    parser = argparse.ArgumentParser(
        # Inherit options from config_parser
        parents=[conf_parser],
        # print script description with -h/--help
        description=__doc__,
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    defaults.update(keystone)
    parser.set_defaults(**defaults)

    parser.add_argument(
        "--api_server_ip", help="IP address of api server")
    parser.add_argument(
        "--api_server_port", help="Port of api server")
    parser.add_argument(
        "--admin_user", help="Name of keystone admin user")
    parser.add_argument(
        "--admin_password", help="Password of keystone admin user")
    parser.add_argument(
        "--admin_tenant_name", help="Tenamt name for keystone admin user")
    parser.add_argument(
        "--openstack_ip", help="IP address of openstack auth node")
    parser.add_argument(
        "--dry_run", action='store_true',
        help="Does not really delete any resource")
    parser.add_argument(
        "resource_uuid", help="Resource UUID to purge, that includes its "
                              "children and back-references resources")
    args = parser.parse_args(remaining_argv)

    connected = False
    while not connected:
        try:
            vnc_api = VncApi(
                args.admin_user,
                args.admin_password,
                args.admin_tenant_name,
                args.api_server_ip,
                args.api_server_port,
                '/',
                auth_host=args.openstack_ip,
                auth_protocol='https',
                auth_port=5000,
                auth_url='/v3/auth/tokens',
                apicafile='/etc/contrail/ssl/certs/sslca.pem',
            )
            connected = True
        except ResourceExhaustionError:
            time.sleep(3)

    try:
        object_type = vnc_api.id_to_fq_name_type(
            args.resource_uuid)[1].replace('-', '_')
    except Exception as e:
        exit("Cannot determine type of resource %s: %s" %
             (args.resource_uuid, str(e)))
    graph = get_back_refs((object_type, args.resource_uuid), DiGraph())
    while graph.node:
        print('Graph contains', len(graph.node), 'node(s)')
        nodes_to_remove = set()
        for node in graph.nodes:
            if not graph.in_edges(node):
                print('Deleting', node[0].replace('_', ' ').title(), node[1])
                if not args.dry_run:
                    try:
                        getattr(vnc_api, '%s_delete' % node[0])(id=node[1])
                    except Exception as e:
                        print("Cannot delete %s: %s" %
                            (node[0].replace('_', ' ').title(), str(e)))
                nodes_to_remove.add(node)
        graph.remove_nodes_from(nodes_to_remove)