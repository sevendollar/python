#! /usr/bin/python

import paramiko

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip, username=user, password=pw)

remote_connection = ssh_client.invoke_shell()
remote_connection.send('terminal length 0\n')
remote_connection.send('show running-config\n')

time.sleep(1)
output = remote_connection.recv(65535)
print(output.decode('UTF-8'))
