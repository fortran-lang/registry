import React, { useEffect, useState } from "react";
import { Container } from "react-bootstrap";
import Button from "react-bootstrap/Button";
import { useDispatch, useSelector } from "react-redux";
import {
  MDBModal,
  MDBModalDialog,
  MDBModalContent,
  MDBModalHeader,
  MDBModalTitle,
  MDBModalBody,
  MDBModalFooter,
  MDBIcon,
} from "mdb-react-ui-kit";
import {
  adminAuth,
  deleteUser,
  deleteNamespace,
  deletePackage,
  deleteRelease,
  deprecatePackage,
} from "../store/actions/adminActions";
import NoPage from "./404";

const AdminSection = () => {
  const uuid = useSelector((state) => state.auth.uuid);
  const dispatch = useDispatch();
  const message = useSelector((state) => state.admin.message);
  const statuscode = useSelector((state) => state.admin.statuscode);
  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);
  const isAdmin = useSelector((state) => state.admin.isAdmin);

  useEffect(() => {
    dispatch(adminAuth(uuid));
  }, [isAuthenticated, uuid]);

  useEffect(() => {
    if (statuscode != null) {
      openModal(statuscode + " Status Code", message, null);
    }
  }, [statuscode, message]);

  const [formData, setFormData] = useState({
    namespaceName: "",
    packageName: "",
    releaseName: "",
    userName: "",
    newPassword: "",
  });

  const [modalData, setModalData] = useState({
    showModal: false,
    modalTitle: "",
    modalMessage: "",
    modalAction: null,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const openModal = (title, message, action) => {
    setModalData({
      showModal: true,
      modalTitle: title,
      modalMessage: message,
      modalAction: action,
    });
  };

  const toggleShowModal = () => {
    setModalData({ ...modalData, showModal: !modalData.showModal });
  };

  const isEmpty = (...values) => {
    if (values.some((value) => value === "")) {
      openModal("Empty Fields", "Please fill out all fields.", () => {
        toggleShowModal();
      });
      return true;
    }
    return false;
  };

  const handleAction = () => {
    if (modalData.modalAction) {
      modalData.modalAction();
    }
    toggleShowModal();
  };

  const handleDeletePackage = () => {
    if (!isEmpty(formData.namespaceName, formData.packageName)) {
      openModal(
        "Delete Package",
        `You will not be able to recover ${formData.namespaceName}/${formData.packageName} package after you delete it.`,
        () => {
          dispatch(
            deletePackage(formData.namespaceName, formData.packageName, uuid)
          );
        }
      );
    }

    // clear the form data
    setFormData({
      namespaceName: "",
      packageName: "",
    });
  };

  const handleDeleteRelease = () => {
    if (
      !isEmpty(
        formData.namespaceName,
        formData.packageName,
        formData.releaseName,
        uuid
      )
    ) {
      openModal(
        "Delete Release",
        `You will not be able to recover ${formData.namespaceName}/${formData.packageName}/${formData.releaseName} release after you delete it.`,
        () => {
          dispatch(
            deleteRelease(
              formData.namespaceName,
              formData.packageName,
              formData.releaseName,
              uuid
            )
          );
        }
      );
    }

    // clear the form data
    setFormData({
      namespaceName: "",
      packageName: "",
      releaseName: "",
    });
  };

  const handleDeleteUser = () => {
    if (!isEmpty(formData.userName, uuid)) {
      openModal(
        "Delete User",
        `You will not be able to recover ${formData.userName} user after you delete it.`,
        () => {
          dispatch(deleteUser(formData.userName, uuid));
        }
      );
    }

    // clear the form data
    setFormData({
      userName: "",
    });
  };

  const handleDeleteNamespace = () => {
    if (!isEmpty(formData.namespaceName, uuid)) {
      openModal(
        "Delete Namespace",
        `You will not be able to recover ${formData.namespaceName} namespace after you delete it.`,
        () => {
          dispatch(deleteNamespace(formData.namespaceName, uuid));
        }
      );
    }

    // clear the form data
    setFormData({
      namespaceName: "",
    });
  };

  const handleDeprecatePackage = () => {
    if (!isEmpty(formData.namespaceName, formData.packageName, uuid)) {
      openModal(
        "Delete Package",
        `You will not be able to recover ${formData.namespaceName}/${formData.packageName} package after you delete it.`,
        () => {
          dispatch(
            deprecatePackage(formData.namespaceName, formData.packageName, uuid)
          );
        }
      );
    }

    // clear the form data
    setFormData({
      namespaceName: "",
      packageName: "",
    });
  };

  //   const changePassword = () => {   // TODO: Enable this feature
  //     console.log("Changing password for user:", formData.userName);
  //     // Add the logic to change the password
  //     // clear the form data
  //     setFormData({
  //       userName: "",
  //       newPassword: "",
  //     });
  //   };

  return isAdmin? ( 
    <Container>
      <br></br>
      <h2 style={{ textAlign: "left" }}>Admin Settings</h2>
      <div>
        <h4>Delete package</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="Namespace Name"
            name="namespaceName"
            value={formData.namespaceName}
            onChange={handleInputChange}
            style={{ width: 300 }}
          />
          <input
            type="text"
            placeholder="Package Name"
            name="packageName"
            value={formData.packageName}
            onChange={handleInputChange}
            style={{ width: 300 }}
          />
        </p>
        <Button onClick={handleDeletePackage} style={{ fontSize: 16 }}>
          Delete Package
        </Button>
      </div>
      <div>
        <br></br>
        <h4>Delete package version</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="Namespace Name"
            name="namespaceName"
            value={formData.namespaceName}
            onChange={handleInputChange}
            style={{ width: 300 }}
          />
          <input
            type="text"
            placeholder="Package Name"
            name="packageName"
            value={formData.packageName}
            onChange={handleInputChange}
            style={{ width: 300 }}
          />
          <input
            type="text"
            placeholder="Release Name"
            name="releaseName"
            value={formData.releaseName}
            onChange={handleInputChange}
            style={{ width: 300 }}
          />
        </p>
        <Button onClick={handleDeleteRelease} style={{ fontSize: 16 }}>
          Delete Release
        </Button>
      </div>
      <div>
        <br></br>
        <h4>Deprecate package</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="Namespace Name"
            name="namespaceName"
            value={formData.namespaceName}
            onChange={handleInputChange}
            style={{ width: 300 }}
          />
          <input
            type="text"
            placeholder="Package Name"
            name="packageName"
            value={formData.packageName}
            onChange={handleInputChange}
            style={{ width: 300 }}
          />
        </p>
        <Button onClick={handleDeprecatePackage} style={{ fontSize: 16 }}>
          Deprecate Package
        </Button>
      </div>
      <div>
        <br></br>
        <h4>Delete Namespace</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="Namespace Name"
            name="namespaceName"
            value={formData.namespaceName}
            onChange={handleInputChange}
            style={{ width: 300 }}
          />
        </p>
        <Button onClick={handleDeleteNamespace} style={{ fontSize: 16 }}>
          Delete Namespace
        </Button>
      </div>
      <div>
        <br></br>
        <h4>Delete user</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="User Name"
            name="userName"
            value={formData.userName}
            onChange={handleInputChange}
            style={{ width: 300 }}
          />
        </p>
        <Button onClick={handleDeleteUser} style={{ fontSize: 16 }}>
          Delete User
        </Button>
      </div>
      {/* <div>            // TODO: Enable this feature
        <br></br>
        <h4>Change password</h4>
        <p style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="User Name"
            name="userName"
            value={formData.userName}
            onChange={handleInputChange}
            style={{ width: 300 }}
          />
          <input
            type="text"
            placeholder="New Password"
            name="newPassword"
            value={formData.newPassword}
            onChange={handleInputChange}
            style={{ width: 300 }}
          />
        </p>
        <Button
          onClick={() =>
            openModal(
              "Change Password",
              `You will not be able to recover ${formData.userName} user's password after you change password.`,
              changePassword
            )
          }
          style={{ fontSize: 16 }}
        >
          Change Password
        </Button>
      </div> */}
      <MDBModal show={modalData.showModal} tabIndex="-1">
        <MDBModalDialog>
          <MDBModalContent>
            <MDBModalHeader>
              <MDBModalTitle>{modalData.modalTitle}</MDBModalTitle>
              <Button
                className="btn-close"
                color="none"
                onClick={toggleShowModal}
              ></Button>
            </MDBModalHeader>
            <MDBModalBody>
              <MDBIcon fas icon="exclamation-triangle" />{" "}
              {modalData.modalMessage}
            </MDBModalBody>
            <MDBModalFooter>
              <Button color="secondary" onClick={toggleShowModal}>
                Close
              </Button>
              <Button onClick={handleAction}>Delete</Button>
            </MDBModalFooter>
          </MDBModalContent>
        </MDBModalDialog>
      </MDBModal>
    </Container>
  ):(<NoPage/>);
};

export default AdminSection;
