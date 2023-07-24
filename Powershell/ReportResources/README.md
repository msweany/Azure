report-resources.ps1 script will connect to your Az Tenant, export a list of all resources in each subscription to a CSV file.

To run:
CD to the directory of this script.
```powershell
./report-resources.ps1 -csvFilePath path-to-file.csv
```

If you want to get a report of just the unique resources in a region, run this
```powershell
./report-resources.ps1 -csvFilePath path-to-file.csv -isFiltered $true
```
