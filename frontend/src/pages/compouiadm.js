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
          <MDBModal show={deprecateModal} setShow={setdeprecateModal} tabIndex="-1">
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
                  able to recover {deprecatepackageName} package after you delete it.
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