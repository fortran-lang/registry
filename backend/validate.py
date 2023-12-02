import os
from flask import request, jsonify
from auth import is_ci
from app import app
import logging
import subprocess
import toml


logging.basicConfig(
    filename="validate.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Page not found", "code": 404})

@app.errorhandler(500)
def internal_server_error(e):
    logging.error("Server Error: %s", str(e))
    return jsonify({"message": "Internal server error", "code": 500})


def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        print(result.stderr)
    return result.stdout if result.stdout else result.stderr

def process_package(packagename):
    # Extract the archive
    extract_command = f'tar -xzf static/temp/{packagename}.tar.gz -C static/temp/'
    run_command(extract_command)

    # Build the package
    build_command = f'cd static/temp/{packagename} && home/registry/fpm build'
    result = run_command(build_command)

    # Read fpm.toml
    toml_path = f'static/temp/{packagename}/fpm.toml'
    with open(toml_path, 'r') as file:
        file_content = file.read()
    parsed_toml = toml.loads(file_content)

    # Clean up
    cleanup_command = f'rm -rf static/temp/{packagename}'
    run_command(cleanup_command)

    if '<ERROR>' in result:
        # Package build failed 
        return False, None
    if '[100%] Project compiled successfully.' in result:
        # Package build success 
        return True, parsed_toml



@app.route("/", methods=['POST'])
def validate():
    print("request received")
    package = request.files['package']
    packagename = request.form['packagename']
    with open(f"static/temp/{packagename}.tar.gz", "wb") as f:
        f.write(package.read())
    # package.save(f"tmp/{packagename}.tar.gz")
    result = process_package(packagename)
    print(result)
    return result


# Log all unhandled exceptions
def log_exception(sender, exception, **extra):
    sender.logger.error(
        "An exception occurred: %s", str(exception), exc_info=(exception)
    )


app.register_error_handler(Exception, log_exception)

debug = True if is_ci != "true" else False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("FLASK_SERVER_PORT", 5000), debug=debug)