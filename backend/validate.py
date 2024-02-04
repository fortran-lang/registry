from app import app
import subprocess
import toml
from mongo import db
from mongo import file_storage
from bson.objectid import ObjectId
from gridfs.errors import NoFile
import toml


def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        print(result.stderr)
    return result.stdout if result.stdout else result.stderr

def process_package(packagename):
    # Create a temp directory
    create_dir_command = f'mkdir -p static/temp/{packagename}'
    run_command(create_dir_command)
    # Extract the archive
    extract_command = f'tar -xzf static/temp/{packagename}.tar.gz -C static/temp/{packagename}/'
    run_command(extract_command)

    # Build the package
    build_command = f'cd static/temp/{packagename} && fpm build'
    result = run_command(build_command)

    # Read fpm.toml
    toml_path = f'static/temp/{packagename}/fpm.toml'
    try:
        with open(toml_path, 'r') as file:
            file_content = file.read()
        parsed_toml = toml.loads(file_content) # handle toml parsing errors
    except:
        return False, None

    # Clean up
    cleanup_command = f'rm -rf static/temp/{packagename} static/temp/{packagename}.tar.gz'
    run_command(cleanup_command)

    if '<ERROR>' in result:
        # Package build failed 
        return False, None
    if '[100%] Project compiled successfully.' in result:
        # Package build success 
        return True, parsed_toml


def validate():
    packages = db.packages.find({"versions": {"$elemMatch": {"isVerified": False}}})
    packages = list(packages)
    for  package in packages:
        for i in package['versions']:
            if 'isVerified' in i.keys() and i['isVerified'] == False:
                tarball = file_storage.get(ObjectId(i['oid']))
                packagename = package['name'] + '-' + i['version']
                with open(f"static/temp/{packagename}.tar.gz", "wb") as f:
                    f.write(tarball.read())
                result = process_package(packagename)
                if result[0] == False:
                    db.packages.update_one({"name": packages['name'],"namespace":package['namespace']}, {"$set": {"versions.$[elem].unabletoVerify": True}}, array_filters=[{"elem.version": i['version']}])
                    print("Package build failed for " + packagename)
                else:
                    print("Package build success for " + packagename)
                    db.packages.update_one({"name": package['name'],"namespace":package['namespace']}, {"$set": {"versions.$[elem].isVerified": True}}, array_filters=[{"elem.version": i['version']}])

                update_data = {}

                for key in ['repository', 'copyright', 'description']:
                    if key in result[1] and package[key] == "Package Under Verification":
                        update_data[key] = result[1][key]

                if update_data:
                    db.packages.update_one({"name": package['name'],"namespace":package['namespace']}, {"$set": update_data})
    return 0

validate()
