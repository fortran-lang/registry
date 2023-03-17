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

const isEmpty = (...values) => {
  return values.some((value) => value === "");
};

const AdminSection = () => {
  const [deprecateModal, setdeprecateModal] = useState(false);
  const toggleShowDeprecateModal = () => {
    if (!isEmpty(deprecatePackageNamespaceName, deprecatepackageName)) {
      setdeprecateModal(!deprecateModal);
    } else {
      toggleShowemptyModal();
    }
  };
  const [deprecatepackageName, setdeprecatepackageName] = useState("");
  const [deprecatePackageNamespaceName, setdeprecatePackageNamespaceName] =
    useState("");

  const [emptyModal, setemptyModal] = useState(false);
  const toggleShowemptyModal = () => setemptyModal(!emptyModal);

  const [deleteNamespaceModal, setdeleteNamespaceModal] = useState(false);
  const toggleShowDeleteNamespaceModal = () => {
    if (!isEmpty(deletenamespaceName)) {
      setdeleteNamespaceModal(!deleteNamespaceModal);
    } else {
      toggleShowemptyModal();
    }
  };

  const [deletenamespaceName, setdeletenamespaceName] = useState("");

  const [deletePackageModal, setdeletePackageModal] = useState(false);
  const toggleShowDeletePackageModal = () => {
    if (!isEmpty(deletepackagenamespaceName, deletepackageName)) {
      setdeletePackageModal(!deletePackageModal);
    } else {
      toggleShowemptyModal();
    }
  };
  const [deletepackageName, setdeletepackageName] = useState("");
  const [deletepackagenamespaceName, setdeletepackagenamespaceName] =
    useState("");

  const [deleteUserModal, setdeleteUserModal] = useState(false);
  const toggleShowDeleteUserModal = () => {
    if (!isEmpty(deleteuserName)) {
      setdeleteUserModal(!deleteUserModal);
    } else {
      toggleShowemptyModal();
    }
  };

  const [deleteuserName, setdeleteuserName] = useState("");

  const [deleteReleaseModal, setdeleteReleaseModal] = useState(false);
  const toggleShowDeleteReleaseModal = () => {
    if (
      !isEmpty(
        deletereleasenamespaceName,
        deletereleasepackageName,
        deletereleaseName
      )
    ) {
      setdeleteReleaseModal(!deleteReleaseModal);
    } else {
      toggleShowemptyModal();
    }
  };
  const [deletereleasepackageName, setdeletereleasepackageName] = useState("");
  const [deletereleasenamespaceName, setdeletereleasenamespaceName] =
    useState("");
  const [deletereleaseName, setdeletereleaseName] = useState("");

  const [changePasswordModal, setchangePasswordModal] = useState(false);
  const toggleShowChangePasswordModal = () => {
    if (!isEmpty(userName, newPassword)) {
      setchangePasswordModal(!changePasswordModal);
    } else {
      toggleShowemptyModal();
    }
  };

  const [userName, setUserName] = useState("");
  const [newPassword, setNewPassword] = useState("");

  useEffect(() => {
    //   dispatch(adminAuth());
  }, []);

  const handleDeprecatePackage = () => {
    // Deprecate package logic
    // dispatch(deprecatePackage(deprecatePackageNamespaceName, deprecatepackageName));
    setdeprecatePackageNamespaceName("");
    setdeprecatepackageName("");
  };

  const handleDeleteNamespace = () => {
    // Delete namespace logic

    // dispatch(deleteNamespace(deletenamespaceName));
    setdeletenamespaceName("");
  };

  const handleDeletePackage = () => {
    // Delete package logic
    // dispatch(deletePackage(deletepackagenamespaceName, deletepackageName));
    setdeletepackagenamespaceName("");
    setdeletepackageName("");
  };

  const handleDeleteUser = () => {
    // Delete user logic
    // dispatch(deleteUser(deleteuserName));
    setdeleteuserName("");
  };

  const handleDeleteRelease = () => {
    // Delete release logic
    // dispatch(deleteRelease(deletereleasenamespaceName, deletereleasepackageName, deletereleaseName));
    setdeletereleasenamespaceName("");
    setdeletereleasepackageName("");
    setdeletereleaseName("");
  };

  const handleChangePassword = () => {
    // Change password logic
    // dispatch(changePassword(userName, newPassword));
    setUserName("");
    setNewPassword("");
  };

  return (
    <Container className="mt-5">
      <MDBModal show={emptyModal} setShow={setemptyModal} tabIndex="-1">
        <MDBModalDialog>
          <MDBModalContent>
            <MDBModalHeader>
              <MDBModalTitle>Empty Inputs</MDBModalTitle>
              <MDBBtn
                className="btn-close"
                color="none"
                onClick={toggleShowemptyModal}
              ></MDBBtn>
            </MDBModalHeader>
            <MDBModalBody>
              <MDBIcon fas icon="exclamation-triangle" /> You must fill all the
              fields.
            </MDBModalBody>
            <MDBModalFooter>
              <MDBBtn color="secondary" onClick={toggleShowDeprecateModal}>
                Close
              </MDBBtn>
            </MDBModalFooter>
          </MDBModalContent>
        </MDBModalDialog>
      </MDBModal>
      <h2 style={{ textAlign: "left" }}>Admin Settings</h2>
      <div>
        <h4>Deprecate package</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="Namespace Name"
            value={deprecatePackageNamespaceName}
            onChange={(e) => setdeprecatePackageNamespaceName(e.target.value)}
            style={{ width: 300 }}
          />{" "}
          <input
            type="text"
            placeholder="Package Name"
            value={deprecatepackageName}
            onChange={(e) => setdeprecatepackageName(e.target.value)}
            style={{ width: 300 }}
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
                <MDBIcon fas icon="exclamation-triangle" /> You will not be able
                to recover {deprecatePackageNamespaceName}/
                {deprecatepackageName} package after you deprecate it.
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
        <h4>Delete namespace</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="Namespace Name"
            value={deletenamespaceName}
            onChange={(e) => setdeletenamespaceName(e.target.value)}
            style={{ width: 300 }}
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
                <MDBIcon fas icon="exclamation-triangle" /> You will not be able
                to recover {deletenamespaceName} Namespace after you delete it.
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
        <h4>Delete package</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="Namespace Name"
            value={deletepackagenamespaceName}
            onChange={(e) => setdeletepackagenamespaceName(e.target.value)}
            style={{ width: 300 }}
          />
          <input
            type="text"
            placeholder="Package Name"
            value={deletepackageName}
            onChange={(e) => setdeletepackageName(e.target.value)}
            style={{ width: 300 }}
          />
        </p>
        <MDBBtn onClick={toggleShowDeletePackageModal} style={{ fontSize: 16 }}>
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
                <MDBIcon fas icon="exclamation-triangle" /> You will not be able
                to recover {deletepackagenamespaceName}/{deletepackageName}{" "}
                package after you delete it.
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
        <h4>Delete user</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="User Name"
            value={deleteuserName}
            onChange={(e) => setdeleteuserName(e.target.value)}
            style={{ width: 300 }}
          />
        </p>
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
                <MDBIcon fas icon="exclamation-triangle" /> You will not be able
                to recover {deleteuserName} user after you delete it.
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
        <h4>Delete release</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="Namespace Name"
            value={deletereleasepackageName}
            onChange={(e) => setdeletereleasepackageName(e.target.value)}
            style={{ width: 300 }}
          />
          <input
            type="text"
            placeholder="package Name"
            value={deletereleasenamespaceName}
            onChange={(e) => setdeletereleasenamespaceName(e.target.value)}
            style={{ width: 300 }}
          />
          <input
            type="text"
            placeholder="Release Name"
            value={deletereleaseName}
            onChange={(e) => setdeletereleaseName(e.target.value)}
            style={{ width: 300 }}
          />
        </p>

        <MDBBtn onClick={toggleShowDeleteReleaseModal} style={{ fontSize: 16 }}>
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
                <MDBIcon fas icon="exclamation-triangle" /> You will not be able
                to recover {deletereleasenamespaceName}/
                {deletereleasepackageName}/{deletereleaseName} release after you
                delete it.
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
        <h4>Change password</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="User Name"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            style={{ width: 300 }}
          />
        </p>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            style={{ width: 300 }}
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
                <MDBIcon fas icon="exclamation-triangle" /> You will not be able
                to recover {userName} user's password after you change password.
              </MDBModalBody>
              <MDBModalFooter>
                <MDBBtn
                  color="secondary"
                  onClick={toggleShowChangePasswordModal}
                >
                  Close
                </MDBBtn>
                <MDBBtn onClick={handleChangePassword}>Change Password</MDBBtn>
              </MDBModalFooter>
            </MDBModalContent>
          </MDBModalDialog>
        </MDBModal>
      </div>
    </Container>
  );
};

export default AdminSection;
