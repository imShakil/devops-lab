---
parent: Active Directory
title: LDAP Connection
---

## Light Directory Active Server

This doc will help to connect your internal(VM) LDAP server to any LDAP browser (jx explorer, Apache Directory).
Basically, I have installed an application with LDAP server in my Virtual Machine (vmware). After then, I was trying to connect that internal ldap server to Apache Directory in my Host Computer.
Thoug I could access application server through my browser, but could not able to make connection of the ldap server into the Apache Directory. Later I found this solution that is the port of that ldap server was not able to communicate with my host computer even after adding that port into the firewall.
Actually we have to create a tunnel of the ssh server to connect that port. 

## LDAP server info

bind dn: cn=admin/directory manager
server address: localhost/ip:port
server password: password

In my case it is:
bind dn: cn=directory manager
server address: localhost:1636
password: password

## Install openssh-server

Make sure that both side of the machine (host computer and VM) have installed the `openssh-server`.
To install openssh server:

```bash
sudo apt install openssh-server
```

To check the ssh status:

```bash
sudo service ssh status
```

## Configure SSH

We need to configure ssh config file as below:

```bash
sudo nano /etc/ssh/sshd_config
```

From this file remove `#` right before `PermitRootLogin` and replace `*-password` with `yes` right after `PermitRootLogin`

Then reload the ssh server:

```bash
sudo systemctl reload ssh
```

## Root login

with `sudo su -` login as a root user. then set a root password with below command:

```bash
sudo passwd
```

## Creating Tunnel

To create tunnel:

```bash
ssh -fNL [port to be used in ldap browser]:ldap server address:ldap server port root@internal ldap server ip address
```

an example:

```bash
ssh -fNL 5909:localhost:1636 root@172.16.132.129
```

It may asked a root password just enter the password you have created using `sudo passwd`. 
That's all.

## Connecting LDAP server in Apache Directory

Select for a new connection and enter like this accroding to your own ldap server value. Please choose SSL connection if your ldap server has ssl connection.

![Screenshot from 2021-07-27 16-58-18](https://user-images.githubusercontent.com/20867846/127233153-f3613156-1b38-401a-85bc-06ec2ce560df.png)

After then enter the `bind dn` value and ldap server password and finish it.

![Screenshot from 2021-07-27 16-58-48](https://user-images.githubusercontent.com/20867846/127233157-a269ca64-c2c3-4fe5-8b88-ffea405ba3d7.png)

Finally you should see as below if it connect succesfully.

![Screenshot from 2021-07-27 16-59-08](https://user-images.githubusercontent.com/20867846/127233158-d245a917-0d3a-4a38-9296-75c551799510.png)

Thanks.
