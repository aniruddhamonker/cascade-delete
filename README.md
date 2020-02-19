# cascade-delete
script to dynamically remove child reference objects from contrail config DB

## Installation
git clone https://github.com/aniruddhamonker/cascade-delete.git

## Execution
```
cascade-delete-3.x.py [-h] [-c FILE] 
                             [--api_server_ip API_SERVER_IP]
                             [--api_server_port API_SERVER_PORT]
                             [--admin_user ADMIN_USER]
                             [--admin_password ADMIN_PASSWORD]
                             [--admin_tenant_name ADMIN_TENANT_NAME]
                             [--openstack_ip OPENSTACK_IP] 
                             [--dry_run]
                             resource_uuid
```
## Options
```
$python cascade-delete-3.x.py -h
usage: 

positional arguments:
  resource_uuid         Resource UUID to purge, that includes its children and
                        back-references resources

optional arguments:
  -h, --help            show this help message and exit
  -c FILE, --conf-file FILE
                        Specify config file
  --api_server_ip API_SERVER_IP
                        IP address of api server
  --api_server_port API_SERVER_PORT
                        Port of api server
  --admin_user ADMIN_USER
                        Name of keystone admin user
  --admin_password ADMIN_PASSWORD
                        Password of keystone admin user
  --admin_tenant_name ADMIN_TENANT_NAME
                        Tenamt name for keystone admin user
  --openstack_ip OPENSTACK_IP
                        IP address of openstack auth node
  --dry_run             Does not really delete any resource
```

## DEMO
This example uses the cascade-delete-3.x script to delete a virtual-network object having UUID "36be345f-499f-49b4-aa29-597e57cee156"
```
python cascade-delete-3.x.py --admin_user admin --admin_password Juniper --admin_tenant_name admin 6be345f-499f-49b4-aa29-597e57cee156

Graph contains 24 node(s)ce (graph size 24, depth 1)
Deleting Instance Ip 18c26eec-52f2-445c-8379-67f476f6c2c5
Deleting Instance Ip 49c51b8c-c9ac-44e0-83f9-26ff6dfcf63c
Deleting Instance Ip c5382af6-588b-4d12-a5e6-017bbb993b3d
Deleting Instance Ip 1fb9b4d0-1a74-458b-a624-2df2b79efc2b
Deleting Instance Ip 4597b9f9-1c0f-4c25-85aa-a74a6a091265
Deleting Instance Ip 9986a1e5-dd78-42a2-847a-5105a538b08f
Deleting Instance Ip 96fdc5f5-7c1d-4907-9995-a7b5fb938815
Deleting Instance Ip 9e658d12-134a-4307-b291-a7fe6ba7b15f
Deleting Instance Ip 6442d8c2-aa09-4879-8224-d0a5f99cf92d
Deleting Instance Ip bcf04a97-90c2-4b75-ae47-ed69e25cad7e
Deleting Instance Ip f20a8b94-2ed6-454b-97f4-285e80bbe3a4
Graph contains 13 node(s)
Deleting Virtual Machine Interface 5fda77df-01c2-4218-a616-aa1c164dfb6f
Deleting Virtual Machine Interface 2d0d6b41-5003-4b60-8b20-96f9266ae514
Deleting Virtual Machine Interface b41f0c8f-6f34-42fd-8d69-6f9c29192698
Deleting Virtual Machine Interface 32e82cbc-14d2-45ba-9126-4d8cb14416bd
Deleting Virtual Machine Interface 2a52b93c-e32f-4d2a-900e-b108dd124142
Deleting Virtual Machine Interface 7ebfdc01-4d0f-43e3-b389-a722e345e987
Deleting Virtual Machine Interface 9edafff6-5a28-47ae-9424-50c5385101c0
Deleting Virtual Machine Interface 797cf912-5a7d-4411-9edc-a6e72cb6778f
Deleting Virtual Machine Interface acca3793-11fe-4e06-8286-1ec6e0106152
Deleting Virtual Machine Interface b9bf8eca-24a3-4d38-968c-8bde45dd9bac
Deleting Virtual Machine Interface b7592234-0f72-4be9-ad07-c75fbabbda5a
Graph contains 2 node(s)
Deleting Routing Instance 8991ee53-41f6-4059-b22e-59c3fbb4152b
Graph contains 1 node(s)
Deleting Virtual Network 36be345f-499f-49b4-aa29-597e57cee156
```

