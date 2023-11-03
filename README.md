# Brief 3

- [Brief 3](#brief-3)
  - [1 Plan d'action.](#1-plan-daction)
    - [1.1 Topologie de l'infrastructure.](#11-topologie-de-linfrastructure)
    - [1.2 Liste des ressources.](#12-liste-des-ressources)
    - [1.3 Liste des tâches.](#13-liste-des-tâches)

Réalisé par : Alain, Noa, Paul et Quentin

## 1 Plan d'action.

### 1.1 Topologie de l'infrastructure.

```mermaid
graph BT
    subgraph Internet
        ip_bastion_public[Adresse Ip Publique: ip_bastion_public]
        ip_app_public[Adresse Ip Publique: ip_app_public]
    end


    ip_bastion_public --> subnet_bastion
    ip_app_public --> subnet_public_app

    subnet_public_app --> nic_app_public
    subnet_bastion --> service_bastion




    subgraph network
        subgraph Administration
            subgraph nsg_public_bastion
                subnet_bastion((AzureBastionSubnet))
            end

            service_bastion[Azure Bastion: service_bastion]

        end

        subgraph monitoring[Monitoring]
            service_sentinel[Azure Sentinel: service_sentinel]
            service_insights[Azure Application: Insights: service_insights]
            service_vault[Coffre Recovery Services]
        end

        subgraph Resources
            subgraph nsg_private
                subnet_private((subnet_private))
            end

            subgraph nsg_public_app

            subnet_public_app((subnet_public))
            end

            disk(Disque de donnée)

            vm_app[Jenkins: vm_app]
            nic_app_public(Network Interface: nic_app_public)
            nic_app_private(Network Interface: nic_app_private)

            service_vault -.-> vm_app
            disk -.-> vm_app
            service_bastion -.-> subnet_private
            subnet_private -.-> nic_app_private
            nic_app_private -.-> vm_app

            service_sentinel -.-> vm_app
            service_sentinel -.-> service_bastion

            service_insights -.-> vm_app
            service_insights -.-> service_bastion
        end

        nic_app_public --> vm_app
    end

    classDef primary fill:#faa,stroke:#f66,stroke-width:4px,color:#fff,stroke-dasharray: 5 5;
    class ip_bastion_public,Administration,nsg_public_bastion,nsg_private,nic_app_private, primary;
    classDef secondary fill:#aff,stroke:#025,stroke-width:2px,color:#003;
    class ip_app_public,nsg_public_app,nic_app_public, secondary;
    classDef tertiary fill:#afa,stroke:#66f,stroke-width:4px,color:#000,stroke-dasharray: 5 5;
    class monitoring,BBBB,CCCC, tertiary;

```

### 1.2 Liste des ressources.

| Nom | Type | Description | Annotation |
| -------- | -------- | -------- | - |
|   BRIEF_3  | Resource group |      | |
| vnet_3     | Virtual Network | Réseau virtuel | Réseau virtuel contenant toute l'infrastructure |
| AzureBastionSubnet | Virtual Network | Sous-réseau réservé au Bastion    | Réseau virtuel réservé au bastion |
| PrivateSubnet     | Virtual Network     | Carte réseau permettant la communication entre la machine applicative et le bastion    | Contient l'application |
| AppSubnet  | Virtual Network    | Carte réseau permettant la connection HTTP des utilisateurs     |  |
| public_ip_app | Public IP address |  |IP Publique permettant l'accès depuis le navigatteur en HTTPS |
| public_ip_bas | Public IP address |  | IP Publique du bastion|
| nsg_public_bas     | Network Security Group   |      | |
| nsg_private    | Network Security Group     |      | |
| nsg_public_app     | Network Security Group     |      | |
| nic_app_public    | Network Interface  |      |  |
| nic_app_private    | Network Interface  |      | Permet la communication en SSH |
| disk_app | Disk | Support de stockage pour la machine virtuelle applicative| |
| vm_appli | Virtual Machine | Machine virtuelle contenant l'application Jenkins |
| Sentinel | Azure Sentinel| |
| Insight | Azure Insight | |
| Vault | Coffre Recovery Service |  |

### 1.3 Liste des tâches.
- [ ] Planifier les actions et quelles ressources mettre en place.

    - [x] Créer la topologie de l'infrastructure
    - [x] Lister les ressources
    - [x] Lister les tâches
    - [x] Assigner les tâches
    - [x] Quel langage utiliser pour le scripting ? --> **Python**

- [x] Production du script python d'automatisation du déploiement de l'infrastructure.
    - [x] Période de reflexion
        - [ ] Sélection des différentes commandes ainsi que l'ordre dans lequel elle seront appelées
        - [ ] Préparation du script : mise en place de l'architecture du programme
    - [x] Rédaction du script
    - [x] Test du script
    - [x] Rédaction de la documentation

- [x] Production du script python d'automatisation de l'installation de l'application et ses dépendances
    - [x] Période de reflexion.
        - [x] Sélection des différentes commandes ainsi que l'ordre dans lequel elle seront appelées
            - [x] Installation de certbot
            - [x] Rétention des logs
            - [x] Publication des clés publiques (ssh)
    - [x] Rédaction du script
    - [x] Test du script
    - [x] Rédaction de la documentation

<!--
[Lien vers doc Microsoft pour déployer Bastion](https://docs.microsoft.com/en-us/azure/bastion/create-host-cli)
Penser au --help :
![img_bastion](https://github.com/b-quentin/simplon_brief3/blob/master/IMG/BASTION/screen0_bastion_help.png?raw=trueg)

[Doc commande créa / chargement ssh](https://docs.microsoft.com/fr-fr/azure/virtual-machines/ssh-keys-azure-cli)


https://docs.microsoft.com/fr-fr/azure/developer/jenkins/configure-on-linux-vm
-->
