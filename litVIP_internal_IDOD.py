# Create VIP Load Balancer for HTTP Traffic
# Internal VIPS for GHS Production in Little Rock

libra --os_auth_url=https://company.com/openstack/auth/url \
--os_username=username --os_password=pasword --os_tenant_name=tenant \
--os_region_name=region create --name=my_load_balancer \
--node 139.61.132.96:0
