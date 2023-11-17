import os
import docker
from app import app
import toml

# Package testing container
client = docker.from_env()
container = client.containers.run(
    "validate_package",
    tty=True,
    detach=True,
    network_disabled=False
)


def validate(package, packagename):
    data = package.read()
    container.put_archive(os.path.dirname(f"/home/registry/{packagename}.tar.gz"), data)
    build_response = container.exec_run(f'sh -c "cd /home/registry/{packagename} &&  /home/registry/fpm build"')
    toml_data = container.exec_run(f'sh -c "cd /home/registry/{packagename} && cat fpm.toml"')
    parsed_toml = toml.loads(str(toml_data, 'utf-8'))
    container.exec_run(f'sh -c "cd /home/registry/ && rm -rf {packagename}"')
    if b'<ERROR>' in build_response.output:
        # Package build failed 
        return False, None
    if b'[100%] Project compiled successfully.' in build_response.output:
        # Package build success 
        return True, parsed_toml
