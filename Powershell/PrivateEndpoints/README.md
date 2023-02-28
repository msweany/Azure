To use this script, create a CSV file with the following headers

# Create a CSV file that has the following headers
rg #resource group where the private endpoint will be deployed \n\n
pename #Name of the private endpoint \n\n
vnet #name of the vNet where the private endpoint will be deployed \n\n
subnet #subnet the private endpoint will be deployed \n\n
nic #The custom name of the network interface attached to the private endpoint. \n\n
dest #The resource id of the private endpoint to connect to. \n\n
plinkname #Name of the private link service connection. \n\n
location #Location the where the private endpoint will be deployed (values from az account list-locations) \n\n
destgroup # group ID of endpoint connecting to (IE: sqlServer) \n\n
zonename #Private DNS Zone name (IE: privatelink-database-windows-net) \n\n
zonegroup #Name of the private dns zone group (IE: default). \n\n
zone #Name of the private dns zone (IE: privatelink.database.windows.net). \n\n

# Run the script
Download the provision-pes.ps1 script and call it with the following syntax
provision-pes.ps1 --subscription <your subscription ID> --csvfile <the csvfilename formatted with the above headers>