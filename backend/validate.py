from app import app
import subprocess
import toml
from mongo import db
from mongo import file_storage
from bson.objectid import ObjectId
from gridfs.errors import NoFile
import toml
from check_digests import check_digests
from typing import Union,List, Tuple, Dict, Any


def run_command(command: str) -> Union[str, None]:
    """
    Execute a shell command and return its output.

    Args:
        command (str): The command to execute.

    Returns:
        Union[str, None]: The standard output of the command if successful,
                          otherwise standard error.
    """
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}")
        print(result.stderr)
    return result.stdout if result.stdout else result.stderr

def collect_dependencies(section: str, parsed_toml: Dict[str, List[Dict[str, Any]]]) -> List[Tuple[str, str]]:
    """
    Collect dependencies from a section in a parsed TOML file.

    Args:
        section (str): The section in the TOML file to collect dependencies from.
        parsed_toml (Dict[str, List[Dict[str, Any]]]): The parsed TOML file represented as a dictionary.

    Returns:
        List[Tuple[str, str]]: A list of dependency tuples containing (namespace, dependency_name).

    """
    dependencies = list()
    for dependency_dict in parsed_toml.get(section, []):
        for dependency_name, dependency_info in dependency_dict.get('dependencies', {}).items():
            dependencies.append((dependency_info['namespace'],dependency_name))
    return dependencies

def process_package(packagename: str) -> Tuple[bool, Union[dict, None], str]:
    """
    This function creates a directory, extracts package contents, reads and parses 'fpm.toml',
    checks digests, and cleans up temporary files.

    Args:
        packagename (str): The name of the package.

    Returns:
        Tuple[bool, Union[dict, None], str]: A tuple containing:
            - bool: Whether the package processing was successful.
            - Union[dict, None]: Parsed 'fpm.toml' content if successful, None otherwise.
            - str: Message describing the result of the package processing.
    """
    create_dir_command = f'mkdir -p static/temp/{packagename}'
    run_command(create_dir_command)
    extract_command = f'tar -xzf static/temp/{packagename}.tar.gz -C static/temp/{packagename}/'
    run_command(extract_command)

    generate_model = f"cd static/temp/{packagename} && fpm build --dump=fpm_model.json" # TODO: interim bug fix, disable after fpm v0.10.2
    run_command(generate_model)
    
    # Read fpm.toml
    toml_path = f'static/temp/{packagename}/fpm.toml'
    try:
        with open(toml_path, 'r') as file:
            file_content = file.read()
        parsed_toml = toml.loads(file_content) # handle toml parsing errors
    except:
        return False, None,"Error parsing toml file"
    
    result = check_digests(f'static/temp/{packagename}/')

    # Clean up
    cleanup_command = f'rm -rf static/temp/{packagename} static/temp/{packagename}.tar.gz'
    # run_command(cleanup_command)
    print(result)

    if result[0]==-1:
        # Package verification failed 
        return False, parsed_toml, "Digests do not match or file not found."
    else:
        # Package verification success
        return True, parsed_toml, "Package verified successfully."


def validate() -> None:
    """
    This function checks the verification status of packages, verifies their contents,
    updates package information, and ensures dependencies are present in the database.

    Args:
        None

    Returns:
        None
    """
    # packages = db.packages.find({"versions": {"$elemMatch": {"isVerified": False}}}) # find packages with unverified versions
    packages = db.packages.find({"is_verified": False})
    packages = list(packages)
    for  package in packages:
        for i in package['versions']:
            if 'is_verified' in i.keys() and i['is_verified'] == False:
                try:
                    tarball = file_storage.get(ObjectId(i['oid']))
                except NoFile:
                    print("No tarball found for " + package['name'] + " " + i['version'])
                    continue
                packagename = package['name'] + '-' + i['version']
                with open(f"static/temp/{packagename}.tar.gz", "wb") as f:
                    f.write(tarball.read())
                result = process_package(packagename)
                update_data = {}
                if result[0] == False:
                    update_data['isVerified'] = False
                    update_data['unabletoVerify'] = True
                    print("Package tests failed for " + packagename)
                    print(result)
                else:
                    print("Package tests success for " + packagename)
                    update_data['isVerified'] = True

                if result[2] == "Error parsing toml file":
                    db.packages.update_one({"name": package['name'],"namespace":package['namespace']}, {"$set": update_data})
                    pass
                
                for key in ['repository', 'copyright', 'description',"homepage", 'categories', 'keywords']:
                    if key in result[1] and package[key] != result[1][key]:
                        if key in ['categories', 'keywords']:
                            update_data[key] = package[key] + result[1][key]
                        else:
                            update_data[key] = result[1][key]

                dependencies = list()
                try:
                    dependencies += [(dependency_info['namespace'],dependency_name) for dependency_name, dependency_info in result[1].get('dependencies', {}).items()]
                except:
                    pass
                for section in ['test', 'example', 'executable']:
                    try:
                        dependencies += collect_dependencies(section, result[1])
                    except:
                        pass
                
                update_data['dependencies'] = list(set(dependencies))

                for i in dependencies:
                    dependency_package = db.packages.find_one({"name": i[1], "namespace": i[0]}) # TODO: enable version checking
                    if dependency_package is None:
                        print(f"Dependency {i[0]}/{i[1]} not found in the database")
                        update_data['isVerified'] = False                     # if any dependency is not found, the package is not verified      

                for k,v in package.items():
                    if v == "Package Under Verification" and k not in update_data.keys():
                        update_data[k] = f"{k} not provided."

                db.packages.update_one({"name": package['name'],"namespace":package['namespace']}, {"$set": update_data})
                print(f"Package {packagename} verified successfully.")


validate()