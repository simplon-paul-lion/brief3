#################################################
#                   03/08/2022                  #
#             jenkins app to Azure              #
#               Author: Nomad                   #
#################################################

import datetime
import re
import subprocess
import json
import time
import paramiko
import argparse
import requests


#######################
# argument handling  ##
#######################

parser = argparse.ArgumentParser()
parser.add_argument("--name-vm",
                    default="vm_app",
                    dest="name_vm",
                    help="Name of virtual machine.")
parser.add_argument("--location",
                    default="centralus",
                    dest="location",
                    help="Location. List:az account list-locations")
parser.add_argument("--fqdn",
                    default="jenkinsapptest",
                    dest="fqdn",
                    help="FQDN.")
parser.add_argument("--size",
                    default="Standard_D2as_v5",
                    dest="size",
                    help="Size of vm. List:az vm list-sizes --location \"location\"")
args = parser.parse_args()

# End argument handling

##############################
#      Variable              #
##############################
group = {
    'name': 'group5',
    'location': args.location
}

nsg_app = {
    'name': 'nsg_app'
}

nsg_bastion = {
    'name': 'nsg_bastion'
}

network = {
    'name': 'network',
    'adress': '10.0.1.0/24'
}

rule_app = {
    'name': 'https',
    'priority': '100',
    'description': 'https connexion on internet',
    'protocol': 'Tcp',
    'port': '443'
}
rule_http_app = {
    'name': 'http',
    'priority': '110',
    'description': 'http connexion on internet',
    'protocol': 'Tcp',
    'port': '80'
}
subnet_bastion = {
    'name': 'AzureBastionSubnet',
    'adress': '10.0.1.0/26'
}

subnet_app = {
    'name': 'subnet_app',
    'adress': '10.0.1.64/26'
}
disk_app = {
    'name': 'disk_app'
}

disk_app_data = {
    'name': 'disk_app_data'
}
nic = {
    'name': 'nic_app'
}
vm = {
    'name': args.name_vm,
    'admin': 'quentin',
    'size': args.size
}
ip_bastion = {
    'name': 'ip_bastion'
}
ip_app = {
    'name': 'ip_app',
    'dns_name': args.fqdn
}
bastion = {
    'name': 'bastion'
}
nsg_bastion = {
    'name': 'nsg_bastion'
}

workspace = {
    'name': 'monitor'
}

# End variable

##################################
#         Function               #
##################################

##################################
# Edit config send to vm         #
##################################


def edit_config(data):
    text = open('jenkins.conf', "r+")
    text_data = []
    for line in text:
        if line != '':
            line = re.sub("(^\s*server_name\s*)(.*)(\.centralus.cloudapp.azure.com;)", r"\1" + data + r"\3", line)
            line = re.sub("(^\s*ssl_certificate \/etc\/letsencrypt\/live\/)(.*)(\.centralus.cloudapp.azure.com\/fullchain.pem;)", r"\1" + data + r"\3", line)
            line = re.sub("(^\s*ssl_certificate_key \/etc\/letsencrypt\/live\/)(.*)(\.centralus.cloudapp.azure.com\/privkey.pem;)", r"\1" + data + r"\3", line)
            line = re.sub("(\s*if \(\$host = )(.*)(\.centralus.cloudapp.azure.com\) \{)", r"\1" + data + r"\3", line)
            text_data.append(line)
    text.close()
    rewrite = open('jenkins.conf', "w")

    for text in text_data:
        rewrite.write(text)
    rewrite.close()

##################################
#Function for execute azure CLI  #
##################################


def exec(cmd):
    cmd.append('--only-show-errors')
    handle_cmd(cmd)
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()

    if output:
        handle_data(output)
    elif err:
        handle_error(err.decode())
        print('delete')
        delete_group(group)


def exec_get(cmd):
    handle_cmd(cmd)
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()

    if output:
        print(output.decode().replace('\n', ''))
        write_log(json.loads(output.decode()))
        return json.loads(output.decode())
    else:
        handle_error(err.decode())
        print('delete')
        delete_group(group)


def write_log(data):
    file = open("./logs", "a")
    file.write(str(data))
    file.close()


def handle_cmd(data):
    response = '############################################\n#               CMD                       #\n############################################\n\n'

    response_dt = ''
    for dt in data:
        if not dt:
            dt = ''
        response_dt += dt + ' '

    now = datetime.datetime.now()
    now = "Execute at: " + str(now)
    response = response + now + '\n' + response_dt.replace('\n', '') + '\n\n'

    write_log(response)
    print(response)


def dict_depth(data, level=0):
    response = ''
    if isinstance(data, dict):
        for dt in data:
            test = data[dt]
            if not data[dt]:
                test = ''
            if isinstance(data[dt], dict):
                test = ''
            if isinstance(data[dt], list):
                test = ''
            if isinstance(data[dt], int):
                test = str(test)

            response = '\t' * level + dt + ': ' + str(test)
            write_log(response + '\n')

            print(response)
            if isinstance(data[dt], dict) and data[dt]:
                dict_depth(data[dt], level=level + 1)
            if isinstance(data[dt], list) and data[dt]:
                dict_depth(data[dt], level=level + 1)
    if isinstance(data, list):
        for dt in data:
            test = dt
            if not dt:
                test = ''
            if isinstance(dt, dict):
                test = ''
            if isinstance(dt, list):
                test = ''
            if isinstance(dt, int):
                test = str(test)

            response = '\t' * level + str(test)
            write_log(response + '\n')

            print(response)
            if isinstance(dt, dict) and dt:
                dict_depth(dt, level=level)
            if isinstance(dt, list) and dt:
                dict_depth(dt, level=level)


def handle_data(data):
    response = '############################################\n#              STDOUT                      #\n############################################\n\n'
    write_log(response)
    print(response)
    now = datetime.datetime.now()
    now = "Stdout at: " + str(now)
    write_log(now + '\n')
    print(now)
    data = json.loads(data)
    dict_depth(data)


def handle_error(data):
    response = '############################################\n#              ERROR                      #\n############################################\n\n'
    now = datetime.datetime.now()
    now = "Stderr at: " + str(now)
    write_log(response)
    print(response)
    write_log(now + '\n')
    print(now)
    write_log(data)
    print(data)


def exec_bg(cmd):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return p

##################################
# Send cmd to function azure CLI #
##################################

##################################
#        Delete function         #
##################################
def delete_group(group):
    group_exists = exec_get(['az', 'group', 'exists', '-n', group['name']])
    if group_exists == "true":
        exec(['az', 'group', 'delete', '-n', group['name'], '--yes'])
    else:
        print('Group not exists.')

##################################
#        Create function         #
##################################
def create_group(group):
    exec(['az', 'group', 'create', '-n', group['name'], '-l', group['location']])

def create_network(group, network, subnet):
    # https://docs.microsoft.com/en-US/cli/azure/network/vnet?view=azure-cli-latest#az-network-vnet-create
    exec(['az', 'network', 'vnet', 'create',
          '-g', group,
          '--name', network['name'],
          '--address-prefix', network['adress'],
          '--subnet-name', subnet['name'],
          '--subnet-prefix', subnet['adress']
          ])


def create_nsg(nsg, group):
    exec(['az', 'network', 'nsg', 'create', '-n', nsg, '-g', group])


def create_subnet(group, network, nsg, subnet):
    exec(['az', 'network', 'vnet', 'subnet', 'create', '-n', subnet['name'], '-g', group,
          '--vnet-name', network, '--address-prefixes', subnet['adress'], '--network-security-group', nsg])


def create_public_adress():
    # https://docs.microsoft.com/fr-fr/cli/azure/network/public-ip?view=azure-cli-latest
    exec(['az', 'network', 'public-ip', 'create', '-g',
          'groupe5', '-n', "ip_bastion", '--sku', 'Standard'])


def create_vm(vm, group, disk, nic, disk_data):
    exec(['az', 'vm', 'create',
          '--name', vm['name'],
          '-g', group,
          '--image', 'UbuntuLTS',
          '--admin-username', vm['admin'],
          '--ssh-key-value', '/home/nomad/.ssh/azure.pub',
          '--os-disk-name', disk,
          '--nics', nic,
          '--attach-data-disks', disk_data,
          '--authentication-type', 'ssh',
          '--size', vm['size']
          ])


def create_ip_public_app(ip, group):
    exec(['az', 'network', 'public-ip', 'create',
          '-n', ip['name'],
          '-g', group,
          '--sku', 'Standard',
          '--dns-name', ip['dns_name']
          ])


def create_ip_public(ip, group):
    exec(['az', 'network', 'public-ip', 'create', '-n',
          ip['name'], '-g', group, '--sku', 'Standard'])


def create_bastion(bastion, group, network, ip_bastion):
    exec(['az', 'network', 'bastion', 'create',
          '--name', bastion['name'],
          '--public-ip-address', ip_bastion,
          '-g', group,
          '--vnet-name', network])


def create_disk(disk, group):
    exec(['az', 'disk', 'create',
          '--name', disk['name'],
          '-g', group,
          '--size-g', '1000',
          '--encryption-type', 'EncryptionAtRestWithPlatformKey'
          ])


def create_nic(nic, group, subnet, network, ip):
    exec(['az', 'network', 'nic', 'create',
          '--name', nic['name'],
          '-g', group,
          '--subnet', subnet,
          '--vnet-name', network,
          '--public-ip-address', ip
          ])


def create_nsg_rule(rule, nsg, group):
    exec(['az', 'network', 'nsg', 'rule', 'create',
          '--name', rule['name'],
          '--nsg', nsg,
          '--priority', rule['priority'],
          '-g', group,
          '--description', rule['description'],
          '--protocol', rule['protocol'],
          '--destination-port-ranges', rule['port']
          ])


def create_user(group, username, key, vm):
    exec(['az', 'vm', 'user', 'update',
          '--username', username,
          '--ssh-key-value', key,
          '-n', vm,
          '-g', group
          ])


def create_workspace(group, workspace):
    exec(['az', 'monitor', 'log-analytics', 'workspace',
          'create', '-g', group, '-n', workspace['name']])


def create_app_insight(group, workspace):
    exec(['az', 'monitor', 'app-insights', 'component', 'create',
          '--app', 'vm_app',
          '-l', group['location'],
          '-g', group['name'],
          '--workspace', workspace])

##################################
#        Update function         #
##################################


def update_workspace_vm(group, vm, workspace):
    exec(['az', 'vm', 'update', '-g', group, '-n', vm, '--workspace', workspace])


def update_bastion_tunnel(id):
    exec(['az', 'resource', 'update',
          '--ids', id,
          '--set', 'properties.enableTunneling=True'
          ])

##################################
#           Get function         #
##################################


def get_bastion_id(group, bastion):
    id = exec_get(['az', 'network', 'bastion', 'show',
                   '-g', group,
                   '-n', bastion,
                   '--query', '"id"'
                   ])

    return id


def get_vm_id(group, vm):
    id = exec_get(['az', 'vm', 'show',
                   '-g', group,
                   '-n', vm,
                   '--query', '"id"'
                   ])

    return id


def get_status_bastion(group, bastion):
    # az network bastion show -n bastion -g group5 --query "provisioningState"
    status = exec_get(['az', 'network', 'bastion', 'show', '-n',
                       bastion, '-g', group, '--query', '"provisioningState"'])

    while status != "Succeeded":
        status = exec_get(['az', 'network', 'bastion', 'show', '-n',
                           bastion, '-g', group, '--query', '"provisioningState"'])


def get_workspace_id(group, workspace):
    id = exec_get(['az', 'monitor', 'log-analytics', 'workspace', 'show',
                   '-g', group, '--workspace-name', workspace, '--query', '"customerId"'])

    return id

##################################
#           Set function         #
##################################


def set_extension_linux(group, vm, workspace):
    exec(['az', 'vm', 'extension', 'set', '-g', group, '--vm-name', vm, '--name', 'OmsAgentForLinux', '--publisher',
          'Microsoft.EnterpriseCloud.Monitoring', '--settings', '{"workspaceId":"' + workspace + '","skipDockerProviderInstall": true}'])


def set_vm_insight(group, vm):
    exec(['az', 'vm', 'extension', 'set', '-g', group, '--vm-name', vm, '--name', 'DependencyAgentLinux',
          '--publisher', 'Microsoft.Azure.Monitoring.DependencyAgent', '--version', '9.5'])


def set_activate_module():
    exec(['az', 'config', 'set', 'extension.use_dynamic_install=yes_without_prompt'])


##################################
#           Tunneling            #
##################################
def tunnel(bastion_name, id, group):
    tunnel = exec_bg(['az', 'network', 'bastion', 'tunnel',
                      '-n', bastion_name,
                      '-g', group,
                      '--target-resource-id', id,
                      '--resource-port', '22',
                      '--port', '2023',
                      ])

    return tunnel

# End function Azure CLI

##################################
#          Ssh function          #
##################################


def ssh_co(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    barbare = True
    while barbare:
        time.sleep(60)
        try:
            client.connect(hostname="127.0.0.1", username="quentin",
                           key_filename='/home/nomad/.ssh/azure', port=2023)
        except:
            print('error co ssh')
        else:
            barbare = False

    stdin, stdout, stderr = client.exec_command(cmd)
    if stdout.channel.recv_exit_status() != 0:
        print('error')
    for line in iter(stdout.readline, ""):
        print(line, end="")
    for line in iter(stderr.readline, ""):
        print(line, end="")
    print('finished.')
    client.close()


def ssh_certbot(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname="127.0.0.1", username="quentin",
                   key_filename='/home/nomad/.ssh/azure', port=2023)

    stdin, stdout, stderr = client.exec_command(cmd)

    stdin.write("1\n")
    stdin.flush()
    stdin.write("2\n")
    stdin.flush()

    print(stderr.readlines())

    client.close()


def ssh_gdisk(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname="127.0.0.1", username="quentin",
                   key_filename='/home/nomad/.ssh/azure', port=2023)

    stdin, stdout, stderr = client.exec_command(cmd)

    stdin.write("n\n")
    stdin.flush()
    stdin.write("1\n")
    stdin.flush()
    stdin.write("\n")
    stdin.flush()
    stdin.write("\n")
    stdin.flush()
    stdin.write("\n")
    stdin.flush()
    stdin.write("w\n")
    stdin.flush()
    stdin.write("Y\n")
    stdin.flush()

    print(stderr.readlines())
    client.close()


def ssh_mkfs(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname="127.0.0.1", username="quentin",
                   key_filename='/home/nomad/.ssh/azure', port=2023)

    stdin, stdout, stderr = client.exec_command(cmd)

    stdin.write("Y\n")
    stdin.flush()

    print(stderr.readlines())
    client.close()


def ssh_sftp_conf_nginx_certbot():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname="127.0.0.1", username="quentin",
                   key_filename='/home/nomad/.ssh/azure', port=2023)

    sftp = client.open_sftp()
    f_out = sftp.file('/etc/nginx/conf.d/install_tls.conf', "w")
    f_out.write('server {\n\tlocation / {\n\t\troot /var/www;\n\t}\n}')
    f_out.close()

    print('finished.')

    client.close()


def ssh_sftp_conf_certbot():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname="127.0.0.1", username="quentin",
                   key_filename='/home/nomad/.ssh/azure', port=2023)

    sftp = client.open_sftp()
    f_out = sftp.file('/etc/letsencrypt/cli.ini', "w")
    f_out.write('email = b.quentin@protonmail.com\nagree-tos = true')
    f_out.close()

    print('finished.')
    client.close()


def send_jenkins_config():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname="127.0.0.1", username="quentin",
                   key_filename='/home/nomad/.ssh/azure', port=2023)

    sftp = client.open_sftp()
    sftp.put('./jenkins.conf', '/etc/nginx/conf.d/jenkins.conf')
    sftp.close()
    client.close()


def send_nginx_config():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(hostname="127.0.0.1", username="quentin",
                   key_filename='/home/nomad/.ssh/azure', port=2023)

    sftp = client.open_sftp()
    sftp.put('./default.conf', '/etc/nginx/sites-available/default')
    sftp.close()
    client.close()

# End function ssh

##################################
#        Main process            #
##################################


# Edit config file with args
edit_config(args.fqdn)

##################################
#       Infrastructure           #
##################################
delete_group(group)
create_group(group)
create_nsg(nsg_app['name'], group['name'])
create_network(group['name'], network, subnet_bastion)
create_subnet(group['name'], network['name'], nsg_app['name'], subnet_app)
create_ip_public_app(ip_app, group['name'])
create_nic(nic, group['name'], subnet_app['name'],
           network['name'], ip_app['name'])
create_disk(disk_app_data, group['name'])
create_vm(vm, group['name'], disk_app['name'],
          nic['name'], disk_app_data['name'])
create_user(group['name'], 'paul', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDCWIWXMnQoBimi0uEDgNo+WY0oMzLIneka5OfvNtSA4zflxHYbv3wbYT0mLtDviolSXQAK26QlYBgaKd21men6S8SOxdLkrk24pqjT3dPk3CxNigaTqbx/AlAkClKxroT0kba8Pq6td/Z+FsIOI4CT1U/fBZ2BuQp5g5ghoi1PcoT339O8WQRCHX+vTRsGdZdJJCZPpRgNgu9Gh5O05/rnDgeDxFsjcsRBv91wCn0+PNIcqV9SEdppmeo6eAoSb00htk/0cY8e46dHlWvDMo3mKMNCJ1IocoJruQguIXebVwh9djhq/G9X0bG+v0JJ+F0hva19cE3gK/thwSUCyJ8JE5s0JrK0EO1iMUCLSjkKEZwEwPMFFuh+bItMAajFHBmY65kbmn1VE9CvYx6za9xv7G1b8kAHlD6+PRKOz08dxbUnnpS3X+oomPGZ4+hiZAEuwy2vKvYlvNZ3dTkK21VlVPZJFk7L/u5MnC3kiZBnRf6Ar2lNDUf57JwoKSgT0H0= utilisateur@UTILISA-RDIKR2H', vm['name'])
create_nsg_rule(rule_app, nsg_app['name'], group['name'])
create_nsg_rule(rule_http_app, nsg_app['name'], group['name'])
create_ip_public(ip_bastion, group['name'])
create_bastion(bastion, group['name'], network['name'], ip_bastion['name'])

id_bastion = get_bastion_id(group['name'], bastion['name'])
update_bastion_tunnel(id_bastion)


get_status_bastion(group['name'], bastion['name'])

create_workspace(group['name'], workspace)
id_work = get_workspace_id(group['name'], workspace['name'])
update_workspace_vm(group['name'], vm['name'], workspace['name'])
set_extension_linux(group['name'], vm['name'], id_work)
set_vm_insight(group['name'], vm['name'])
set_activate_module()
create_app_insight(group, workspace['name'])

# End infrastructure

##################################
#          Tunneling             #
##################################
print('get id app for tunnel')
app_id = get_vm_id(group['name'], vm['name'])
print('tunnel')
open_tunnel = tunnel(bastion['name'], app_id, group['name'])


##################################
#       ssh process for config   #
#         app for jenkins        #
##################################

##################################
#       Install sofware          #
##################################
"""
ssh_co('sudo apt update')
print('create partition')
ssh_gdisk('sudo gdisk /dev/disk/azure/scsi1/lun0')
print('formating partition')
ssh_mkfs('sudo mkfs -t ext4 /dev/disk/azure/scsi1/lun0')
ssh_co('sudo mkfs -t ext4 /dev/disk/azure/scsi1/lun0')
print('create file jenkins')
ssh_co('sudo mkdir /var/lib/jenkins')
print('mount')
ssh_co('sudo mount -t ext4 /dev/disk/azure/scsi1/lun0 /var/lib/jenkins')
print('Installation JAVA.')
ssh_co('sudo apt install openjdk-11-jre -y')
print('Add deb for jenkins.')
ssh_co('curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null')
ssh_co('echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null')
print('Update APT.')
ssh_co('sudo apt update')
"""
print('Installation Jenkins.')
ssh_co('sudo apt install jenkins -y')
print('Installation Certbot.')
ssh_co('sudo apt install certbot -y')
print('Installation Nginx.')
ssh_co('sudo apt install nginx -y')
print('Installation python3-certbot-nginx')
ssh_co('sudo apt install python3-certbot-nginx -y')

# End install software

##################################
#           Install Nginx        #
##################################
print('create file install_tls')
ssh_co('sudo touch /etc/nginx/conf.d/install_tls.conf')
print('chown intsall tls quentin')
ssh_co('sudo chown -R quentin:quentin /etc/nginx/conf.d/install_tls.conf')
print('send config certbot')
ssh_sftp_conf_nginx_certbot()
print('chown install_tls root')
ssh_co('sudo chown -R root:root /etc/nginx/conf.d/install_tls.conf')
print('start nginx')
ssh_co('sudo systemctl start nginx')
print('While wait fqdn:')

# End Install Nginx

##################################
#           check fqdn           #
##################################

r = requests.head("http://" + args.fqdn + ".centralus.cloudapp.azure.com/")
while r.status_code != 200:
    r = requests.head("http://" + args.fqdn + ".centralus.cloudapp.azure.com/")
    print('Waiting fqdn: ' + str(r.status_code))

if r.status_code == 200:
    print('FQDN is active.')

# End check FQDN

##################################
#   Install and config Certbot   #
##################################
print('chown cli.ini quentin')
ssh_co('sudo chown quentin:quentin /etc/letsencrypt/cli.ini')
print('Send file conf certbot')
ssh_sftp_conf_certbot()
print('chown cli.ini root')
ssh_co('sudo chown root:root /etc/letsencrypt/cli.ini')
print('certbot certif')
ssh_certbot('sudo certbot --nginx --config /etc/letsencrypt/cli.ini -d ' +
            args.fqdn + '.centralus.cloudapp.azure.com')

# End install certbot

##################################
#         Config nginx           #
#     for certbot with jenkins   #
##################################
print('chown conf.d quentin')
ssh_co('sudo chown -R quentin:quentin /etc/nginx/conf.d')
print('send jenkins conf')
send_jenkins_config()
print('chown conf.d root')
ssh_co('sudo chown -R root:root /etc/nginx/conf.d')
print('chown sites-available quentin')
ssh_co('sudo chown -R quentin:quentin /etc/nginx/sites-available')
print('send default nginx config')
send_nginx_config()
print('chown default root')
ssh_co('sudo chown -R root:root /etc/nginx/sites-available')
print('delete install_tls.conf')
ssh_co('sudo rm /etc/nginx/conf.d/install_tls.conf')

# End config nginx for certbot witj jenkins

##################################
#   (Re)start nginx and jenkins  #
##################################
print('restart nginx')
ssh_co('sudo systemctl restart nginx')
print('start jenkins')
ssh_co('sudo systemctl start jenkins')

# End (re)start nginx and jenkins

open_tunnel.terminate()
# End tunneling
# End main processs
