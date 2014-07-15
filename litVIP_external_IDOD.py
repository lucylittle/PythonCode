# Create VIP Load Balancer for HTTPs Traffic
# External VIPS for IDOD Production in Little Rock
libra --os_auth_url=https://acxiom.com/openstack/auth/url \
--os_username=username --os_password=pasword --os_tenant_name=tenant \
--os_region_name=region create --name=my_load_balancer \
--node 198.160.97.78:443 --node 192.160.97.79:443 --protocol=TCP --port==443\
