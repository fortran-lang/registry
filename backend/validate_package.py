import os
import docker
from app import app

# Package testing container
client = docker.from_env()
container = client.containers.run(
    "registry",
    tty=True,
    detach=True,
    network_disabled=False
)


def validate_package(package, packagename):
    data = package.read()
    container.put_archive(os.path.dirname(f"/home/registry/{packagename}.tar.gz"), data)
    build_response = container.exec_run(f'sh -c "cd /home/registry/{packagename} &&  /home/registry/fpm build"')
    container.exec_run(f'sh -c "cd /home/registry/ && rm -rf {packagename}"')
    if b'<ERROR>' in build_response.output:
        # Package build failed 
        # print("build failed")
        return False
    if b'[100%] Project compiled successfully.' in build_response.output:
        # Package build success 
        # print("build success")
        # print(build_response.output)
        return True
