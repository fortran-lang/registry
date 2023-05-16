import React from "react";

const Help = () => {
  return (<div>
    <p>First of all, you will need to register a user account:</p>
    <p>For uploading your package to the registry, you will have to step by step follow the following points:</p>
    <p>Register yourself as a user. You will require a unique username, email & password to set up your account.</p>
    <p>For uploading a package from fpm, you will have to first create a namespace. A namespace represents a collection of packages. Each package is published under a namespace in order to avoid collision of same package names. Namespace names will be unique always.
    Now, that you will have created a namespace with a unique name and a nice description. You can go to dashboard by from the dropdown options in the Navigation bar on top.
    In the dashboard, you can see the namespace that has been created by you. You can now generate a token for this namespace.</p>
    <p>This token will be valid for 1 week , but you can always generate a new token.</p>
  <p>  Use this token to upload packages from the fpm using the CLI:</p> 
    <code>fpm publish --token token-here </code>
    <p>After completing the above steps, you will receive a response in the fpm command line interface whether your upload was successful or not.
    
    If your upload was successful, you can now again go to the registry frontend and check the dashboard. It should display the package uploaded by you.
    You can now Add/Remove maintainers to your package. Mantainers have the rights to operate on the same package.</p></div>);
};

export default Help;
