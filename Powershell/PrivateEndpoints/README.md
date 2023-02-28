To use this script, create a CSV file with the following headers

# Create a CSV file that has the following headers
**rg** #resource group where the private endpoint will be deployed <br>
**pename** #Name of the private endpoint <br>
**vnet** #name of the vNet where the private endpoint will be deployed <br>
**subnet** #subnet the private endpoint will be deployed <br>
**nic** #The custom name of the network interface attached to the private endpoint. <br>
**dest** #The resource id of the private endpoint to connect to. <br>
**plinkname** #Name of the private link service connection.<br>
**location** #Location the where the private endpoint will be deployed (values from az account list-locations) <br>
**destgroup** # group ID of endpoint connecting to (IE: sqlServer) <br>
**zonename** #Private DNS Zone name (IE: privatelink-database-windows-net) <br>
**zonegroup** #Name of the private dns zone group (IE: default). <br>
**zone** #Name of the private dns zone (IE: privatelink.database.windows.net). <br>

# Run the script
Download the provision-pes.ps1 script and call it with the following syntax<br>
```
provision-pes.ps1 --subscription <your subscription ID> --csvfile <the csvfilename formatted with the above headers>
```