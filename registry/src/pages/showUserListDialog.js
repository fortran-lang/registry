import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Card, Modal } from "react-bootstrap";
import { fetchUserListData } from "../store/actions/userListActions";
import { MDBIcon } from "mdbreact";

const ShowUserListDialog = (props) => {
  const users = useSelector((state) => state.userList.users);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(
      fetchUserListData({
        namespaceAdmins: props.admins,
        namespaceMaintainers: props.maintainers,
        namespace: props.namespace,
      })
    );
  }, [props.isListDialogOpen]);

  return (
    <>
      <Modal show={props.show} onHide={props.onHide}>
        <Modal.Header closeButton>
          <Modal.Title>
            {(props.admins && "Namespace Admins") ||
              (props.maintainers && "Namespace Maintainers") ||
              "Package Maintainers"}
          </Modal.Title>
        </Modal.Header>

        <Modal.Body>
          {users.map((user, index) => {
            return (
              <Card
                key={user.id}
                style={{
                  marginBottom: "10px",
                }}
              >
                <Card.Body
                  style={{
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <MDBIcon
                    style={{
                      paddingRight: "10px",
                    }}
                    fas
                    icon="user"
                  />
                  <h6
                    style={{
                      marginBottom: "0",
                    }}
                  >
                    {user.username}
                  </h6>
                </Card.Body>
              </Card>
            );
          })}
        </Modal.Body>
      </Modal>
    </>
  );
};

export default ShowUserListDialog;
