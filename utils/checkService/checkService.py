import subprocess

def getServiceStatus(service_name):
    try:
        result = subprocess.run(
            ['systemctl', 'list-unit-files', f'{service_name}.service'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        exists = service_name in result.stdout
        return exists
        
    except Exception as e:
        print(f"Error checking service: {e}")
        return False