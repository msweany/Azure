To use this script, create a CSV file with the following headers

# Create a CSV file that has the following headers
rg #resource group where the private endpoint will be deployed
pename #Name of the private endpoint
vnet #name of the vNet where the private endpoint will be deployed
subnet #subnet the private endpoint will be deployed
nic #The custom name of the network interface attached to the private endpoint.
dest #The resource id of the private endpoint to connect to.
plinkname #Name of the private link service connection.
location #Location the where the private endpoint will be deployed (values from az account list-locations)
destgroup # group ID of endpoint connecting to (IE: sqlServer)
zonename #Private DNS Zone name (IE: privatelink-database-windows-net)
zonegroup #Name of the private dns zone group (IE: default).
zone #Name of the private dns zone (IE: privatelink.database.windows.net).

Download the provision-pes.ps1 script and call it with the following syntax
provision-pes.ps1 --subscription <your subscription ID> --csvfile <the csvfilename formatted with the above headers>