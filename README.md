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
