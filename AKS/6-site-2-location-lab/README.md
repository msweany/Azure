This has instructions on how to build a lab with 2 AKS clusters, using an NGINX ingress controller.

All commands I used to create the lab are in the **build-commands.txt** file.

**east-ingress.yaml** contains the config for name based host routing in one cluster and displays 3 different services (mapped to customer1-service, customer2-service, customer3-service)

**west-ingress.yaml** contains the config for name based host routing in the other cluster and displays 3 different services (mapped to customer4-service, customer5-service, customer6-service)

*Make sure you edit these ingress.yaml files since they are expecting domains in my mike-demo.com domain.*  If all you change is the -host values and use everything else the same, it should work for you.