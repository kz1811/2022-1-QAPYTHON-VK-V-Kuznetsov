import os
import signal
import subprocess
import time
from copy import copy
import pytest
import requests
from requests.exceptions import ConnectionError
import settings


REPO_ROOT = os.path.abspath(os.path.join(__file__, os.pardir))


def wait_ready(host, port, time_wait=15):
    started = False
    st = time.time()
    while time.time() - st <= time_wait:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'{host}:{port} did not started in {time_wait}s!')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        ######### app configuration #########

        app_path = os.path.join(REPO_ROOT, 'application', 'app.py')

        env = copy(os.environ)
        env.update({
            'APP_HOST': settings.APP_HOST,
            'APP_PORT': settings.APP_PORT,
            'AGE_HOST': settings.STUB_HOST,
            'AGE_PORT': settings.STUB_PORT,
            'SURNAME_HOST': settings.MOCK_HOST,
            'SURNAME_PORT': settings.MOCK_PORT
        })

        app_stderr = open('/tmp/app_stderr', 'w')
        app_stdout = open('/tmp/app_stdout', 'w')

        app_proc = subprocess.Popen(['python3.8', app_path],
                                    stderr=app_stderr, stdout=app_stdout,
                                    env=env)
        wait_ready(settings.APP_HOST, settings.APP_PORT)

        config.app_proc = app_proc
        config.app_stderr = app_stderr
        config.app_stdout = app_stdout

        ######### app configuration #########
        #########
        #########
        #########
        ######### stub configuration #########
        stub_path = os.path.join(REPO_ROOT, 'stub', 'flask_stub.py')
        # stub_path = os.path.join(repo_root, 'stub', 'simple_http_stub.py')

        env = copy(os.environ)
        env.update({
            'STUB_HOST': settings.STUB_HOST,
            'STUB_PORT': settings.STUB_PORT
        })

        stub_stderr = open('/tmp/stub_stderr', 'w')
        stub_stdout = open('/tmp/stub_stdout', 'w')

        stub_proc = subprocess.Popen(['python3.8', stub_path],
                                     stderr=stub_stderr, stdout=stub_stdout,
                                     env=env)
        wait_ready(settings.STUB_HOST, settings.STUB_PORT)

        config.stub_proc = stub_proc
        config.stub_stderr = stub_stderr
        config.stub_stdout = stub_stdout
        ######### stub configuration #########
        #########
        #########
        #########
        ######### mock configuration #########
        from mock import flask_mock
        flask_mock.run_mock()

        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)
        ######### mock configuration #########


def pytest_unconfigure(config):
    ######### app unconfiguration #########

    config.app_proc.send_signal(signal.SIGINT)
    exit_code = config.app_proc.wait()

    assert exit_code == 0, f'app exited abnormally with exit code: {exit_code}'

    config.app_stderr.close()
    config.app_stdout.close()

    ######### app unconfiguration #########
    #########
    #########
    #########
    ######### stub unconfiguration #########
    config.stub_proc.send_signal(signal.SIGINT)
    config.app_proc.wait()

    config.stub_stderr.close()
    config.stub_stdout.close()
    ######### stub unconfiguration #########
    #########
    #########
    #########
    ######### mock unconfiguration #########
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')
    ######### mock configuration #########


@pytest.fixture(scope='function', autouse=True)
def clear_data():
    APP_DATA = {}
    USER_ID_SEQ = 1
    SURNAME_DATA = {}
