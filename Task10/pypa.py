import boto3
import paramiko

aws_access_key = 'Your_Key'
aws_secret_key = 'Your_Key'

aws_region = 'us-east-1'

private_key_path = 'C:\\Users\\Your_user\\.ssh\\id_rsa'

ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

instance_id = None
public_ip = None

def create_instance():
    response = ec2.run_instances(
        ImageId='ami-0fc5d935ebf8bc3bc', 
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='task10', 
        SecurityGroupIds=['sg-0c98fe8d1ffd19ad0'], 
        TagSpecifications =[
            {
                'ResourceType':'instance',
                'Tags':[
                    {
                        'Key':'Name',
                        'Value':'Your_name'
                    },
                ]
            }
        ]
    )

    global instance_id
    instance_id = response['Instances'][0]['InstanceId']
    ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])

    instance_details = ec2.describe_instances(InstanceIds=[instance_id])
    global public_ip
    public_ip = instance_details['Reservations'][0]['Instances'][0].get('PublicIpAddress', 'N/A')

    instance_type = instance_details['Reservations'][0]['Instances'][0]['InstanceType']
    private_ip = instance_details['Reservations'][0]['Instances'][0]['PrivateIpAddress']
    os_type = instance_details['Reservations'][0]['Instances'][0].get('PlatformDetails', 'Linux')

    print(f'Запущен инстанс с ID: {instance_id}')
    print(f'Тип инстанса: {instance_type}')
    print(f'Public IP: {public_ip}')
    print(f'Private IP: {private_ip}')
    print(f'ОС: {os_type}')

def change_authorized_keys():
    local_private_key_path = 'C:\\Users\\Your_user\\.ssh\\your_inst_key.pem'
    local_new_key_path = 'C:\\Users\\Your_user\\.ssh\\id_rsa.pub'
    
    hostname = public_ip
    username = 'ubuntu'
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    private_key = paramiko.RSAKey(filename=local_private_key_path)
    
    client.connect(hostname, username=username, pkey=private_key)
    
    sftp = client.open_sftp()
    
    sftp.put(local_new_key_path, '.ssh/authorized_keys')
    sftp.close()
    
    print('Ключ заменен.')
  
def ssh_connect():
    key = paramiko.RSAKey.from_private_key_file(private_key_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(public_ip, username='ubuntu', pkey=key)
        print("SSH коннект установлен.")
        ssh.close()
    except Exception as fail:
        print(f"SSH коннект сброшен: {str(fail)}")

def terminate_instance():
    global instance_id
    if instance_id:
        ec2.terminate_instances(InstanceIds=[instance_id])
        ec2.get_waiter('instance_terminated').wait(InstanceIds=[instance_id])
        print(f'Инстанc {instance_id} убит.')
        if public_ip:
            print(f'Public IP: {public_ip}')

while True:
    print("Выберите действие:")
    print("1 - Создать инстанс и вывести статистику.")
    print("2 - Попробовать установить SSH коннект.")
    print("3 - Убить инстанс.")
    print("4 - Сменить ключ.")
    choice = input("Выберите ваш вариант: ")

    if choice == '1':
        create_instance()
    elif choice == '2':
        if public_ip:
            ssh_connect()
    elif choice == '3':
        terminate_instance()
    elif choice == '4':
        change_authorized_keys()

