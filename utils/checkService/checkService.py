import subprocess

def getFullStatus(service_name):
    try:
        # Ejecutamos 'systemctl status'
        output = subprocess.check_output(['systemctl', 'status', service_name], 
                                         universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output