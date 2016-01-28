import re
from fabric.api import env, run, hide, task
from envassert import detect, file, port, process, service, user
from hot.utils.test import get_artifacts


def magento_is_responding():
    with hide('running', 'stdout'):
        wget_cmd = ("wget --quiet --output-document - "
                    "--header='Host: example.com' http://localhost/")
        homepage = run(wget_cmd)
        if re.search('Magento Demo Store', homepage):
            return True
        else:
            return False


@task
def check():
    env.platform_family = detect.detect()

    # web server is listening
    assert port.is_listening(80), 'Web port 80 is not listening'

    # redis is listening
    assert port.is_listening(6381), 'Redis port 6381 is not listening'

    # nginx user is created
    assert user.exists("nginx"), 'nginx user does not exist'
    
    # domain ftp user is created
    assert user.exists("magento_sftp"), 'magento_sftp user does not exist'

    # processes are running
    assert process.is_up("nginx"), 'nginx is not running'
    assert process.is_up("php-fpm"), 'php-fpm is not running'
    assert process.is_up("redis"), 'redis is not running'
    
    # services are enabled
    assert service.is_enabled("nginx"), 'nginx service not enabled'
    assert service.is_enabled("redis"), 'redis service not enabled'
    assert service.is_enabled("php-fpm"), 'php-fpm not enabled'
    assert service.is_enabled("mysql"), 'database service not enabled'

    # magento main page is available
    assert magento_is_responding(), 'Magento did not respond as expected.'


@task
def artifacts():
    env.platform_family = detect.detect()
    get_artifacts()
