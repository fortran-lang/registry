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

def collect_dependencies(section, parsed_toml):
    dependencies = list()
    for dependency_dict in parsed_toml.get(section, []):
        for dependency_name, dependency_info in dependency_dict.get('dependencies', {}).items():
            dependencies.append((dependency_info['namespace'],dependency_name))
    return dependencies

def process_package(packagename):
    # Create a temp directory
    create_dir_command = f'mkdir -p static/temp/{packagename}'
    run_command(create_dir_command)
    # Extract the archive
    extract_command = f'tar -xzf static/temp/{packagename}.tar.gz -C static/temp/{packagename}/'
    run_command(extract_command)

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

    # if '<ERROR>' in result:
    #     # Package build failed 
    #     return False, None
    # if '[100%] Project compiled successfully.' in result:
    #     # Package build success 
    #     return True, parsed_toml


def validate():
    packages = db.packages.find({"versions": {"$elemMatch": {"isVerified": False}}})
    packages = list(packages)
    for  package in packages:
        for i in package['versions']:
            if 'isVerified' in i.keys() and i['isVerified'] == False:
                try:
                    tarball = file_storage.get(ObjectId(i['oid']))
                except NoFile:
                    print("No tarball found for " + package['name'] + " " + i['version'])
                    continue
                packagename = package['name'] + '-' + i['version']
                with open(f"static/temp/{packagename}.tar.gz", "wb") as f:
                    f.write(tarball.read())
                result = process_package(packagename)
                
                # if result[0] == False:
                #     db.packages.update_one({"name": packages['name'],"namespace":package['namespace']}, {"$set": {"versions.$[elem].unabletoVerify": True}}, array_filters=[{"elem.version": i['version']}])
                #     print("Package tests failed for " + packagename)
                # else:
                #     print("Package tests success for " + packagename)
                #     db.packages.update_one({"name": package['name'],"namespace":package['namespace']}, {"$set": {"versions.$[elem].isVerified": True}}, array_filters=[{"elem.version": i['version']}])

                update_data = {}

                for key in ['repository', 'copyright', 'description',"homepage", 'categories', 'keywords']:
                    if key in result[1] and package[key] != result[1][key]:
                        if key in ['categories', 'keywords']:
                            update_data[key] = package[key] + result[1][key]
                        else:
                            update_data[key] = result[1][key]

                dependencies = list()
                dependencies += [(dependency_info['namespace'],dependency_name) for dependency_name, dependency_info in result[1].get('dependencies', {}).items()]
                for section in ['test', 'example', 'executable']:
                    dependencies += collect_dependencies(section, result[1])
                
                # TODO: verify if the dependencies are present in the database
                update_data['dependencies'] = list(set(dependencies))

                for i in dependencies:
                    dependency_package = db.packages.find_one({"name": i[1], "namespace": i[0]}) # also verify the version
                    if dependency_package is None:
                        print(f"Dependency {i[0]}/{i[1]} not found in the database")
                        update_data['isVerified'] = False
                    else:
                        

                        # flag the package as not verified.
                    

                for k,v in package.items():
                    if v == "Package Under Verification" and k not in update_data.keys():
                        update_data[k] = f"{k} not provided."

                db.packages.update_one({"name": package['name'],"namespace":package['namespace']}, {"$set": update_data})


validate()


# # target checking of sections:

# # upload time
# # name: The name of the project 
# # version: The version of the project
# # license: The project license

# maintainer: Maintainer of the project                        auto supported by registry
# author: Author of the project                                auto supported by registry

# repository: The project’s repository                         supported 
# homepage: The project’s homepage                             supported 
# description: Description of the project                      supported 
# copyright: Copyright of the project                          supported 
# keywords: Keywords describing the project                    supported 
# categories: Categories associated with the project           not supported


# # support categories and keywords
# # support the keywords and update from verification
# # fix 595 line  and packages model tages to keywords.
# # add categories to packages model 

# # package is verified if and only if all versions are verified


# firstly check verified of a package
# if not verified then check for each version
# if not verified then process the package
# if verified then update the package
# if not verified then update the package

# bug fix package rating handling.

