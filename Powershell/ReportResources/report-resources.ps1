# parameters
# -isFiltered: if true, only list unique resources in a region
# -csvFilePath: path to the csv file to save the resources to
param (
    [bool]$isFiltered,
    [Parameter(Mandatory=$true)]
    [string]$csvFilePath
)
    
# Install and import the Azure PowerShell module if not already installed
if (-Not (Get-Module -Name Az -ListAvailable)) {
    Install-Module -Name Az -Force
}

# Connect to your Azure account
Connect-AzAccount

# Get all subscriptions
$subscriptions = Get-AzSubscription

# array to hold unique resources
$uniqueResources = @()

# Loop through each subscription
foreach ($subscription in $subscriptions) {
    # Set the context to the current subscription
    Set-AzContext -SubscriptionId $subscription.Id

    # Get the resources for the current subscription
    $resources = Get-AzResource

    # If the IsFiltered parameter is set to true, then only list the unique resources in a region
    if ($isFiltered) {
        foreach($resource in $resources){
            #$resource | Select-Object -Property ResourceId,ResourceName,ResourceType,Location | Export-Csv -Path $csvFilePath -NoTypeInformation -Append
            if(($resource.Location+':'+$resource.ResourceType) -notin $uniqueResources){
                $uniqueResources += $resource.Location+':'+$resource.ResourceType
                $resource | Select-Object -Property ResourceType,Location | Export-Csv -Path $csvFilePath -NoTypeInformation -Append
            }
        }
        write-host "$($subscription.Name) unique resources saved to CSV" -ForegroundColor Blue
    }else{
        # Export the resources to a CSV file named after the subscription
        $resources | Export-Csv -Path $csvFilePath -NoTypeInformation -Append
        write-host "$($subscription.Name) resources saved to CSV" -ForegroundColor Blue
    } 
}
# Write a message to the console when the export is complete
Write-Host "Export completed. CSV file for all subscriptions have been created."
