[Création resource group](https://docs.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest#az-group-create) :  

```console  
az group create \
    --name resGroupName \
    --location ... 
```

[Création Virtual Network](https://docs.microsoft.com/en-us/cli/azure/network/vnet?view=azure-cli-latest#az-network-vnet-create) :  
```console
az network vnet create \
  --name vNetName \
  --resource-group resGroupName \
  --subnet-name default
  ```
[Création Subnet](https://docs.microsoft.com/fr-fr/cli/azure/network/vnet/subnet?view=azure-cli-latest#az-network-vnet-subnet-create)
```console
az network vnet subnet create --address-prefixes
                              --name
                              --resource-group
                              --vnet-name
                              [--defer]
                              [--delegations]
                              [--disable-private-endpoint-network-policies {false, true}]
                              [--disable-private-link-service-network-policies {false, true}]
                              [--nat-gateway]
                              [--network-security-group]
                              [--route-table]
                              [--service-endpoint-policy]
                              [--service-endpoints]
```
[Création IP Publique](https://docs.microsoft.com/en-us/cli/azure/network/public-ip?view=azure-cli-latest#az-network-public-ip-create) :  
```console
az network public-ip create -g resGroupName -n MyIp --dns-name MyLabel --allocation-method Static
```  

[Création NSG](https://docs.microsoft.com/en-us/cli/azure/network/nsg?view=azure-cli-latest#az-network-nsg-create) :  
```console
az network nsg create --name
                      --resource-group
                      [--location]
                      [--tags]
```  

[Création Network Interface Card](https://docs.microsoft.com/en-us/cli/azure/network/nic?view=azure-cli-latest#az-network-nic-create)  
```console
az network nic create -g resGroupName --vnet-name MyVnet --subnet MySubnet -n MyNic \
    --ip-forwarding --network-security-group MyNsg
```

[Création VM](https://docs.microsoft.com/en-us/cli/azure/vm?view=azure-cli-latest#az-vm-create)  

```console
az vm create --name
             --resource-group
             [...]
```

[Création Disk](https://docs.azure.cn/zh-cn/cli/disk?view=azure-cli-latest#az-disk-create)

```console
az disk create --name
               --resource-group
               [--disk-access]
               [--disk-encryption-set]
               [--disk-iops-read-only]
               [--disk-iops-read-write]
               [--disk-mbps-read-only]
               [--disk-mbps-read-write]
               [--encryption-type]
               [--for-upload {false, true}]
               [--gallery-image-reference]
               [--gallery-image-reference-lun]
               [--hyper-v-generation {V1, V2}]
               [--image-reference]
               [--image-reference-lun]
               [--location]
               [--logical-sector-size]
               [--max-shares]
               [--network-access-policy {AllowAll, AllowPrivate, DenyAll}]
               [--no-wait]
               [--os-type {Linux, Windows}]
               [--size-gb]
               [--sku {Premium_LRS, StandardSSD_LRS, Standard_LRS, UltraSSD_LRS}]
               [--source]
               [--source-storage-account-id]
               [--subscription]
               [--tags]
               [--tier]
               [--upload-size-bytes]
               [--zone {1, 2, 3}]
```
