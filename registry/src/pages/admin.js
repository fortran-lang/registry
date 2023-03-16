import React, { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import {
  MDBBtn,
  MDBModal,
  MDBModalDialog,
  MDBModalContent,
  MDBModalHeader,
  MDBModalTitle,
  MDBModalBody,
  MDBModalFooter,
  MDBIcon,
} from "mdb-react-ui-kit";

const AdminSection = () => {
  const [deprecateModal, setdeprecateModal] = useState(false);
  const [deleteNamespaceModal, setdeleteNamespaceModal] = useState(false);
  const [deletePackageModal, setdeletePackageModal] = useState(false);
  const [deleteUserModal, setdeleteUserModal] = useState(false);
  const [deleteReleaseModal, setdeleteReleaseModal] = useState(false);
  const [changePasswordModal, setchangePasswordModal] = useState(false);
  const toggleShowDeprecateModal = () => setdeprecateModal(!deprecateModal);
  const toggleShowDeleteUserModal = () => setdeleteUserModal(!deleteUserModal);
  const toggleShowDeleteNamespaceModal = () =>
    setdeleteNamespaceModal(!deleteNamespaceModal);
  const toggleShowDeletePackageModal = () =>
    setdeletePackageModal(!deletePackageModal);
  const toggleShowDeleteReleaseModal = () =>
    setdeleteReleaseModal(!deleteReleaseModal);
  const toggleShowChangePasswordModal = () =>
    setchangePasswordModal(!changePasswordModal);
  const [packageName, setPackageName] = useState("");
  const [deprecatepackageName, setdeprecatepackageName] = useState("");
  const [toggleSwitch, setToggleSwitch] = useState(false);
  const [namespaceName, setNamespaceName] = useState("");
  const [userName, setUserName] = useState("");
  const [releaseName, setReleaseName] = useState("");
  const [newPassword, setNewPassword] = useState("");
//   const [isAdmin, setIsAdmin] = 

  useEffect(() => {
   
    //   dispatch(resetErrorMessage());
  
  }, [isAuthenticated]);


  const handleDeprecatePackage = () => {
    // Deprecate package logic
  };

  const handleDeleteNamespace = () => {
    // Delete namespace logic
  };

  const handleDeletePackage = () => {
    // Delete package logic
  };

  const handleDeleteUser = () => {
    // Delete user logic
  };

  const handleDeleteRelease = () => {
    // Delete release logic
  };

  const handleChangePassword = () => {
    // Change password logic
  };

  return (
    <Container className="mt-5">
      <div>
        <h2>Admin Settings</h2>
        <div>
          <h3>Deprecate package</h3>
          <p style={{ textAlign: "left" }}>
            <input
              type="text"
              placeholder="Package Name"
              value={deprecatepackageName}
              onChange={(e) => setdeprecatepackageName(e.target.value)}
            />
          </p>
          <MDBBtn onClick={toggleShowDeprecateModal} style={{ fontSize: 16 }}>
            Deprecate Package
          </MDBBtn>
          <MDBModal
            show={deprecateModal}
            setShow={setdeprecateModal}
            tabIndex="-1"
          >
            <MDBModalDialog>
              <MDBModalContent>
                <MDBModalHeader>
                  <MDBModalTitle>Deprecate Package</MDBModalTitle>
                  <MDBBtn
                    className="btn-close"
                    color="none"
                    onClick={toggleShowDeprecateModal}
                  ></MDBBtn>
                </MDBModalHeader>
                <MDBModalBody>
                  <MDBIcon fas icon="exclamation-triangle" /> You will not be
                  able to recover {deprecatepackageName} package after you
                  delete it.
                </MDBModalBody>
                <MDBModalFooter>
                  <MDBBtn color="secondary" onClick={toggleShowDeprecateModal}>
                    Close
                  </MDBBtn>
                  <MDBBtn onClick={handleDeprecatePackage}>
                    Deprecate Package
                  </MDBBtn>
                </MDBModalFooter>
              </MDBModalContent>
            </MDBModalDialog>
          </MDBModal>
        </div>
        <div>
          <h3>Delete namespace</h3>
          <p style={{ textAlign: "left" }}>
            <input
              type="text"
              placeholder="Namespace Name"
              value={namespaceName}
              onChange={(e) => setNamespaceName(e.target.value)}
            />
          </p>
          <MDBBtn
            onClick={toggleShowDeleteNamespaceModal}
            style={{ fontSize: 16 }}
          >
            Delete Namespace
          </MDBBtn>
          <MDBModal
            show={deleteNamespaceModal}
            setShow={setdeleteNamespaceModal}
            tabIndex="-1"
          >
            <MDBModalDialog>
              <MDBModalContent>
                <MDBModalHeader>
                  <MDBModalTitle>Delete Namespace</MDBModalTitle>
                  <MDBBtn
                    className="btn-close"
                    color="none"
                    onClick={toggleShowDeleteNamespaceModal}
                  ></MDBBtn>
                </MDBModalHeader>
                <MDBModalBody>
                  <MDBIcon fas icon="exclamation-triangle" /> You will not be
                  able to recover {namespaceName} Namespace after you delete it.
                </MDBModalBody>
                <MDBModalFooter>
                  <MDBBtn
                    color="secondary"
                    onClick={toggleShowDeleteNamespaceModal}
                  >
                    Close
                  </MDBBtn>
                  <MDBBtn onClick={handleDeleteNamespace}>
                    Delete Namespace
                  </MDBBtn>
                </MDBModalFooter>
              </MDBModalContent>
            </MDBModalDialog>
          </MDBModal>
        </div>
        <div>
          <h3>Delete package</h3>
          <p style={{ textAlign: "left" }}>
            <input
              type="text"
              placeholder="Package Name"
              value={packageName}
              onChange={(e) => setPackageName(e.target.value)}
            />
          </p>
          <MDBBtn
            onClick={toggleShowDeletePackageModal}
            style={{ fontSize: 16 }}
          >
            Deprecate Package
          </MDBBtn>
          <MDBModal
            show={deletePackageModal}
            setShow={setdeletePackageModal}
            tabIndex="-1"
          >
            <MDBModalDialog>
              <MDBModalContent>
                <MDBModalHeader>
                  <MDBModalTitle>Delete Package</MDBModalTitle>
                  <MDBBtn
                    className="btn-close"
                    color="none"
                    onClick={toggleShowDeletePackageModal}
                  ></MDBBtn>
                </MDBModalHeader>
                <MDBModalBody>
                  <MDBIcon fas icon="exclamation-triangle" /> You will not be
                  able to recover {packageName} package after you delete it.
                </MDBModalBody>
                <MDBModalFooter>
                  <MDBBtn
                    color="secondary"
                    onClick={toggleShowDeletePackageModal}
                  >
                    Close
                  </MDBBtn>
                  <MDBBtn onClick={handleDeletePackage}>Delete Package</MDBBtn>
                </MDBModalFooter>
              </MDBModalContent>
            </MDBModalDialog>
          </MDBModal>
        </div>
        <div>
          <h3>Delete user</h3>
          <p style={{ textAlign: "left" }}>
            <input
              type="text"
              placeholder="User Name"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
            />
          </p>
          {/* <button onClick={handleDeleteUser}>Confirm</button>
           */}
          <MDBBtn onClick={toggleShowDeleteUserModal} style={{ fontSize: 16 }}>
            Delete User
          </MDBBtn>
          <MDBModal
            show={deleteUserModal}
            setShow={setdeleteUserModal}
            tabIndex="-1"
          >
            <MDBModalDialog>
              <MDBModalContent>
                <MDBModalHeader>
                  <MDBModalTitle>Delete User</MDBModalTitle>
                  <MDBBtn
                    className="btn-close"
                    color="none"
                    onClick={toggleShowDeleteUserModal}
                  ></MDBBtn>
                </MDBModalHeader>
                <MDBModalBody>
                  <MDBIcon fas icon="exclamation-triangle" /> You will not be
                  able to recover {userName} user after you delete it.
                </MDBModalBody>
                <MDBModalFooter>
                  <MDBBtn color="secondary" onClick={toggleShowDeleteUserModal}>
                    Close
                  </MDBBtn>
                  <MDBBtn onClick={handleDeleteUser}>Delete User</MDBBtn>
                </MDBModalFooter>
              </MDBModalContent>
            </MDBModalDialog>
          </MDBModal>
        </div>
        <div>
          <h3>Delete release</h3>
          <p style={{ textAlign: "left" }}>
            <input
              type="text"
              placeholder="Release Name"
              value={releaseName}
              onChange={(e) => setReleaseName(e.target.value)}
            />
          </p>

          <MDBBtn
            onClick={toggleShowDeleteReleaseModal}
            style={{ fontSize: 16 }}
          >
            Delete Release
          </MDBBtn>
          <MDBModal
            show={deleteReleaseModal}
            setShow={setdeleteReleaseModal}
            tabIndex="-1"
          >
            <MDBModalDialog>
              <MDBModalContent>
                <MDBModalHeader>
                  <MDBModalTitle>Delete Release</MDBModalTitle>
                  <MDBBtn
                    className="btn-close"
                    color="none"
                    onClick={toggleShowDeleteReleaseModal}
                  ></MDBBtn>
                </MDBModalHeader>
                <MDBModalBody>
                  <MDBIcon fas icon="exclamation-triangle" /> You will not be
                  able to recover {releaseName} release after you delete it.
                </MDBModalBody>
                <MDBModalFooter>
                  <MDBBtn
                    color="secondary"
                    onClick={toggleShowDeleteReleaseModal}
                  >
                    Close
                  </MDBBtn>
                  <MDBBtn onClick={handleDeleteRelease}>Delete Release</MDBBtn>
                </MDBModalFooter>
              </MDBModalContent>
            </MDBModalDialog>
          </MDBModal>
        </div>
        <div>
          <h3>Change password</h3>
          <p style={{ textAlign: "left" }}>
            <input
              type="text"
              placeholder="User Name"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
            />
          </p>
          <p style={{ textAlign: "left" }}>
            <input
              type="text"
              placeholder="New Password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
          </p>
          <MDBBtn
            onClick={toggleShowChangePasswordModal}
            style={{ fontSize: 16 }}
          >
            Change Password
          </MDBBtn>
          <MDBModal
            show={changePasswordModal}
            setShow={setchangePasswordModal}
            tabIndex="-1"
          >
            <MDBModalDialog>
              <MDBModalContent>
                <MDBModalHeader>
                  <MDBModalTitle>Change Password</MDBModalTitle>
                  <MDBBtn
                    className="btn-close"
                    color="none"
                    onClick={toggleShowChangePasswordModal}
                  ></MDBBtn>
                </MDBModalHeader>
                <MDBModalBody>
                  <MDBIcon fas icon="exclamation-triangle" /> You will not be
                  able to recover {userName} user's password after you change
                  password.
                </MDBModalBody>
                <MDBModalFooter>
                  <MDBBtn
                    color="secondary"
                    onClick={toggleShowChangePasswordModal}
                  >
                    Close
                  </MDBBtn>
                  <MDBBtn onClick={handleChangePassword}>
                    Change Password
                  </MDBBtn>
                </MDBModalFooter>
              </MDBModalContent>
            </MDBModalDialog>
          </MDBModal>
        </div>
      </div>
    </Container>
  );
};

export default AdminSection;
