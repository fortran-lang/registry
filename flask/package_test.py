from flask import jsonify, request
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
def copy_to(src, dst, container):
    dst = dst
    container = container

    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src)
    tar = tarfile.open(src + ".tar", mode="w")
    try:
        tar.add(srcname)
    finally:
        tar.close()

    data = open(src + ".tar", "rb").read()
    container.put_archive(os.path.dirname(dst), data)


# Testing package inside container 
def test_package_in_container():
    copy_to('./package.zip', '/home/registry/package.zip', container)
    container.exec_run('unzip package.zip')
    print(container.exec_run('sh -c "/home/registry/fpm build"'))
    print(container.exec_run('ls'))
    a = container.exec_run('sh -c "timeout 15s fpm run"',demux=True)
    return a


# API Endpoint to test package
@app.route("/validate_package", methods=["POST","GET"])
def test_package():
    uuid = request.form.get("uuid")
    package_test = test_package_in_container()
    if package_test.output[0] == None:
        output = jsonify({"executed": ""})
        if '<ERROR>' in package_test.output[1].decode():
            output = jsonify({"package_testing_failed" : 'true'})
        
        return output, 202
    output = jsonify({"package_testing_failed": 'false'})

    return output, 202

