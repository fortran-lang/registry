import os
import docker
import tarfile
from app import app

#package testing container
client = docker.from_env()
container = client.containers.run(
    "registry",
    tty=True,
    detach=True,
    network_disabled=False
)


# Copying package file to container
def copy_to(package, dst, container):
    data = package.read()
    container.put_archive(os.path.dirname(dst), data)


def validate_package(tarball,packagename):
    copy_to(tarball, f'/home/registry/{packagename}.zip', container)
    container.exec_run('unzip package.zip')
    build_response = container.exec_run('sh -c "/home/registry/fpm build"')
    # execute_response = container.exec_run('sh -c "timeout 15s fpm run"',demux=True)
    if build_response.output[0] == None:
        if '<ERROR>' in build_response.output[1].decode():
            # package build failed 
            return False
        else:
            # package build success 
            return True

