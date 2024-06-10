def Test0(aws, param):
    instance_id = 'i-06c51f4f542763747'

    # Создайте объект клиента SSM
    ssm_client = bt('ssm')

    # Запустите команду на экземпляре и получите CommandId
    response = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': ['systemctl is-active apache2']}
    )

    command_id = response['Command']['CommandId']

    waiter = ssm_client.get_waiter('command_executed')

    # Определите максимальное время ожидания в секундах (например, 300 секунд)
    max_wait_time = 300

    # try:
    waiter.wait(
        InstanceId=instance_id,
        CommandId=command_id,
        WaiterConfig={
            'Delay': 15,  # Интервал проверки статуса (в секундах)
            'MaxAttempts': max_wait_time // 15  # Максимальное количество попыток
        }
    )
    # except WaiterError as e:
    #     print(f"Waiter failed: {e}")


def Test1(aws, param):

    # Создайте объект клиента SSM
    ssm_client = bt('ssm')

    # Укажите ID вашего EC2-инстанса
    instance_id = 'your_instance_id'

    # Определите команду, которую вы хотите выполнить (проверка статуса Apache)
    command = 'systemctl is-active apache2'

    # Отправьте команду на экземпляр
    response = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': [command]}
    )

    # Получите идентификатор команды для проверки статуса выполнения
    command_id = response['Command']['CommandId']

    # Дождитесь завершения выполнения команды
    ssm_client.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id
    )

