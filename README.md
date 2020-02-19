# cascade-delete
script to dynamically remove child reference objects from contrail config DB

##Installation
git clone https://github.com/aniruddhamonker/cascade-delete.git

##Execution
python cascade-delete.py --admin_user <USERNAME> --admin_password <PASSWD> --admin_tenant_name <TENANT> --openstack_ip <KEYSTONE_AUTH_IP> <UUID_OF_RESOURCE_TO_DELETE>
