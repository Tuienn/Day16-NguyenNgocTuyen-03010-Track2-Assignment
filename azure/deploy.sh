#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export AZURE_CONFIG_DIR="${AZURE_CONFIG_DIR:-/tmp/day16-azure-config}"
rg_name=ai-lab-rg
location=southeastasia
if [[ $(az group exists --name "$rg_name") == true ]]; then
  owner=$(az group show --name "$rg_name" --query tags.lab -o tsv)
  [[ "$owner" == day16-track2 ]] || { echo 'Resource group exists without lab tag; aborting.' >&2; exit 1; }
fi
[[ -f lab-key.pub ]] || ssh-keygen -t ed25519 -f lab-key -N '' -C day16-azure-lab
source_ip=$(curl -fsS --max-time 20 https://api.ipify.org)
python3 -c 'import ipaddress,sys; ipaddress.IPv4Address(sys.argv[1])' "$source_ip"
az group create --name "$rg_name" --location "$location" --tags lab=day16-track2 --output none
az network vnet create --resource-group "$rg_name" --name ai-lab-vnet \
  --address-prefixes 10.16.0.0/16 --subnet-name ai-lab-subnet \
  --subnet-prefixes 10.16.1.0/24 --output none
az network nsg create --resource-group "$rg_name" --name ai-lab-nsg --output none
az network nsg rule create --resource-group "$rg_name" --nsg-name ai-lab-nsg \
  --name allow-ssh-from-me --priority 100 --source-address-prefixes "$source_ip/32" \
  --destination-port-ranges 22 --access Allow --protocol Tcp --output none
az vm create --resource-group "$rg_name" --name ai-cpu-node \
  --image Ubuntu2204 --size Standard_B2s_v2 --admin-username azureuser \
  --ssh-key-values lab-key.pub --vnet-name ai-lab-vnet --subnet ai-lab-subnet \
  --nsg ai-lab-nsg --nsg-rule NONE --public-ip-sku Standard \
  --storage-sku Standard_LRS --os-disk-size-gb 30 \
  --custom-data cloud-init-cpu.yaml --tags lab=day16-track2 --output json
