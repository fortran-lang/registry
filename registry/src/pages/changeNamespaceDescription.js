// import { useState } from "react";
// import { useDispatch, useSelector } from "react-redux";
// import Modal from "react-bootstrap/Modal";
// import Button from "react-bootstrap/Button";
// // import {
// //   addNamespaceAdmin,
// //   resetMessages,
// // } from "../store/actions/namespaceAdminsActions";         # fix this

// const ChangeNamespaceDescriptionFormDialog = (props) => {
//   const [description, setDescription] = useState("");
//   const [validationError, setValidationError] = useState("");
//   const uuid = useSelector((state) => state.auth.uuid);
//   // const successMessage = useSelector(                                 # fix this
//   //   (state) => state.addRemoveNamespaceAdmin.successMessage
//   // );
//   // const errorMessage = useSelector(
//   //   (state) => state.addRemoveNamespaceAdmin.errorMessage
//   // );

//   const dispatch = useDispatch();

//   const onSubmit = (event) => {
//     dispatch(resetMessages());
//     event.preventDefault();

//     // If the form input is not valid. Do not proceed.
//     if (!validateForm()) {
//       return;
//     }

//     // dispatch(                                    # fix this
//     //   addNamespaceAdmin(
//     //     {
//     //       uuid: uuid,
//     //       namespace: props.namespace,
//     //       username_to_be_added: username,
//     //     },
//     //     currUsername
//     //   )
//     // );
//   };

//   const resetData = () => {
//     setDescription("");
//     setValidationError("");
//     dispatch(resetMessages());
//   };

//   const validateForm = () => {
//     if (!username) {
//       setValidationError("Desccription is required");
//       return false;
//     }

//     setValidationError("");
//     return true;
//   };

//   return (
//     <form id="change-description-form">
//       <Modal
//         {...props}
//         size="md"
//         aria-labelledby="contained-modal-title-vcenter"
//         centered
//         onExit={resetData}
//       >
//         <Modal.Header closeButton>
//           <Modal.Title id="contained-modal-title-vcenter">
//             Change Namespace Description
//           </Modal.Title>
//         </Modal.Header>
//         <Modal.Body>
//           <label>Enter Namespace Description</label>
//           <input
//             type="text"
//             name="description"
//             placeholder="description"
//             value={description}
//             id="change-description-input"
//             onChange={(e) => setDescription(e.target.value)}
//           />
//           {validationError && (
//             <p id="change-description-error">{validationError}</p>
//           )}
//           {successMessage && (
//             <p id="change-description-success">{successMessage}</p>
//           )}
//           {errorMessage && <p id="change-description-error">{errorMessage}</p>}
//         </Modal.Body>
//         <Modal.Footer>
//           <Button variant="success" onClick={onSubmit}>
//             Change
//           </Button>
//         </Modal.Footer>
//       </Modal>
//     </form>
//   );
// };

// export default ChangeNamespaceDescriptionFormDialog;
