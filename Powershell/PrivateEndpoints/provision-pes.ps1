<# 
To use this script, you provide the name of a CSV file and subscription via parameters
It'll loop through the CSV and set variables, based on the header, then use those values
to provision the private endpoint and create the appropriate zone group in the private DNS
zone to link that resource with an IP. 
############################################################################################
MAKE SURE YOU UNDERSTAND EVERYTHING IN THIS SCRIPT BEFORE YOU RUN IT.  USE AT YOUR OWN RISK
############################################################################################
#>
# call script.ps1 --subscription <your subscription ID> --csvfile < your csv filename >
param (
    [Parameter(Mandatory = $true,
        ParameterSetName = 'subscription',
        HelpMessage = 'Enter subscription ID')]
        [string]$subscription,
    [Parameter(Mandatory = $true,
        ParameterSetName = 'csvfile',
        HelpMessage = 'Enter required CSV filename')]
        [string]$csvfile
)
# Connect to Azure and set the subscription
Connect-AzAccount 
Set-AzContext -Subscription $subscription

<# ###############################################################
############ DO NOT EDIT BELOW THIS LINE #########################
#################################################################>

# import the CSV with the PEs
$pes = Import-Csv $csvfile

foreach($item in $pes){
    write-host "Variable rg is $($item.rg)"
    write-host "Variable pename is $($item.pename)"
    write-host "Variable vnet is $($item.vnet)"
    write-host "Variable subnet is $($item.subnet)"
    write-host "Variable nic is $($item.nic)"
    write-host "Variable dest is $($item.dest)"
    write-host "Variable plinkname is $($item.plinkname)"
    write-host "Variable location is $($item.location)"
    write-host "Variable destgroup is $($item.destgroup)"
    write-host "Variable zone is $($item.zone)"
    write-host "Variable zonegroup is $($item.zonegroup)"
    write-host "Variable zonename is $($item.zonename)" 
}


# lets make sure the data looks like they expect
$check = Read-host "Does this data look correct? Warning, y here will move forward with provisioning. (y/n)" 
if($check -eq 'y'){
    write-host "################################" -ForegroundColor green
    write-host "Continuing to provision" -ForegroundColor Green
    write-host "################################" -ForegroundColor green
}else{
    write-host "################################" -ForegroundColor Red
    write-host "Exiting Script" -ForegroundColor Red
    write-host "################################" -ForegroundColor Red
    exit
}

#do the provisioning
foreach($item in $pes){
    #provision the private endpoint
    # https://learn.microsoft.com/en-us/cli/azure/network/private-endpoint?view=azure-cli-latest#az-network-private-endpoint-create
    write-host "provisioning $($item.pename)" -ForegroundColor yellow
    az network private-endpoint create -g $item.rg -n $item.pename --vnet-name $item.vnet --subnet $item.subnet --nic-name $item.nic --private-connection-resource-id $item.dest --connection-name $item.plinkname -l $item.location --group-id $item.destgroup
    write-host "$($item.pename) complete" -ForegroundColor green

    #provision the private DNS
    # https://learn.microsoft.com/en-us/cli/azure/network/private-endpoint/dns-zone-group?view=azure-cli-latest#az-network-private-endpoint-dns-zone-group-create
    write-host "provisioning DNS for $($item.pename)" -ForegroundColor yellow
    az network private-endpoint dns-zone-group create --endpoint-name $item.pename -g $item.rg -n $item.zonegroup --zone-name $item.zone --private-dns-zone $item.zonename
    write-host "$($item.pename) added to DNS" -ForegroundColor green
    write-host "################################" -ForegroundColor green
}

write-host "################################" -ForegroundColor green
write-host "Script complete" -ForegroundColor green
write-host "################################" -ForegroundColor green