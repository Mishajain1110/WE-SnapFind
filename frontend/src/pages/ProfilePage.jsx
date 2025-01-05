import React, { useState, useEffect } from "react";
import moment from "moment";
import Datetime from "react-datetime";
import API from "../api"; // Axios instance for API calls
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCalendarAlt, faUpload } from "@fortawesome/free-solid-svg-icons";
import "react-datetime/css/react-datetime.css";
import "bootstrap/dist/css/bootstrap.min.css";
import {
  Col,
  Row,
  Card,
  Form,
  Button,
  InputGroup,
} from "@themesberg/react-bootstrap";

// Import the default profile image
import Profile3 from "../assets/profile.png";

const ProfilePage = () => {
  const [userDetails, setUserDetails] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    birthday: "",
    gender: "",
    address: "",
    address_number: "",
    country: "",
    state: "",
    city: "",
    profile_image: Profile3,
  });
  const [editing, setEditing] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserDetails((prevState) => ({ ...prevState, [name]: value }));
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    setUserDetails((prevState) => ({
      ...prevState,
      profile_image: file,
    }));
  };

  return (
    <Card border="light" className="bg-white shadow-sm mb-4">
      <Card.Body>
        <Row>
          <Col lg={8}>
            <Card className="shadow-sm mb-4">
              <Card.Body>
                <h5 className="mb-4">General Information</h5>
                <Form>
                  <Row>
                    <Col md={6} className="mb-3">
                      <Form.Group id="firstName">
                        <Form.Label>First Name</Form.Label>
                        <Form.Control
                          required
                          type="text"
                          name="first_name"
                          value={userDetails.first_name}
                          onChange={handleChange}
                          disabled={!editing}
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6} className="mb-3">
                      <Form.Group id="lastName">
                        <Form.Label>Last Name</Form.Label>
                        <Form.Control
                          required
                          type="text"
                          name="last_name"
                          value={userDetails.last_name}
                          onChange={handleChange}
                          disabled={!editing}
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md={6} className="mb-3">
                      <Form.Group id="birthday">
                        <Form.Label>Birthday</Form.Label>
                        <Datetime
                          timeFormat={false}
                          value={
                            userDetails.birthday
                              ? moment(userDetails.birthday).toDate()
                              : ""
                          }
                          onChange={(date) =>
                            setUserDetails((prevState) => ({
                              ...prevState,
                              birthday: moment(date).format("YYYY-MM-DD"),
                            }))
                          }
                          renderInput={(props, openCalendar) => (
                            <InputGroup>
                              <InputGroup.Text>
                                <FontAwesomeIcon icon={faCalendarAlt} />
                              </InputGroup.Text>
                              <Form.Control
                                type="text"
                                value={
                                  userDetails.birthday
                                    ? moment(userDetails.birthday).format(
                                        "MM/DD/YYYY"
                                      )
                                    : ""
                                }
                                onFocus={openCalendar}
                                disabled={!editing}
                                onChange={() => {}}
                              />
                            </InputGroup>
                          )}
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6} className="mb-3">
                      <Form.Group id="gender">
                        <Form.Label>Gender</Form.Label>
                        <Form.Select
                          name="gender"
                          value={userDetails.gender}
                          onChange={handleChange}
                          disabled={!editing}
                        >
                          <option value="">Select Gender</option>
                          <option value="Male">Male</option>
                          <option value="Female">Female</option>
                          <option value="Other">Other</option>
                        </Form.Select>
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col md={6} className="mb-3">
                      <Form.Group id="email">
                        <Form.Label>Email</Form.Label>
                        <Form.Control
                          required
                          type="email"
                          name="email"
                          value={userDetails.email}
                          onChange={handleChange}
                          disabled={!editing}
                        />
                      </Form.Group>
                    </Col>
                    <Col md={6} className="mb-3">
                      <Form.Group id="phone">
                        <Form.Label>Phone</Form.Label>
                        <Form.Control
                          required
                          type="text"
                          name="phone"
                          value={userDetails.phone}
                          onChange={handleChange}
                          disabled={!editing}
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col sm={8} className="mb-3">
                      <Form.Group id="address">
                        <Form.Label>Address</Form.Label>
                        <Form.Control
                          required
                          type="text"
                          name="address"
                          value={userDetails.address}
                          onChange={handleChange}
                          disabled={!editing}
                        />
                      </Form.Group>
                    </Col>
                    <Col sm={4} className="mb-3">
                      <Form.Group id="addressNumber">
                        <Form.Label>Number</Form.Label>
                        <Form.Control
                          required
                          type="text"
                          name="address_number"
                          value={userDetails.address_number}
                          onChange={handleChange}
                          disabled={!editing}
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  <Row>
                    <Col sm={4} className="mb-3">
                      <Form.Group id="country">
                        <Form.Label>Country</Form.Label>
                        <Form.Control
                          required
                          type="text"
                          name="country"
                          value={userDetails.country}
                          onChange={handleChange}
                          disabled={!editing}
                        />
                      </Form.Group>
                    </Col>
                    <Col sm={4} className="mb-3">
                      <Form.Group id="state">
                        <Form.Label>State</Form.Label>
                        <Form.Control
                          required
                          type="text"
                          name="state"
                          value={userDetails.state}
                          onChange={handleChange}
                          disabled={!editing}
                        />
                      </Form.Group>
                    </Col>
                    <Col sm={4} className="mb-3">
                      <Form.Group id="city">
                        <Form.Label>City</Form.Label>
                        <Form.Control
                          required
                          type="text"
                          name="city"
                          value={userDetails.city}
                          onChange={handleChange}
                          disabled={!editing}
                        />
                      </Form.Group>
                    </Col>
                  </Row>
                  <div className="mt-3">
                    <Button
                      variant="primary"
                      onClick={() => setEditing(!editing)}
                    >
                      {editing ? "Cancel" : "Edit"}
                    </Button>
                    {editing && (
                      <Button
                        variant="success"
                        className="ms-2"
                      >
                        Save Changes
                      </Button>
                    )}
                  </div>
                </Form>
              </Card.Body>
            </Card>
          </Col>
          <Col lg={4}>
            <Card className="shadow-sm">
              <Card.Body>
                <h5 className="mb-3 text-center">Profile Photo</h5>
                <div className="d-flex flex-column align-items-center">
                  <div
                    className="profile-photo-box mb-3"
                    style={{
                      width: "150px",
                      height: "150px",
                      border: "2px dashed #ddd",
                      borderRadius: "50%",
                      backgroundImage: `url(${
                        typeof userDetails.profile_image === "string"
                          ? userDetails.profile_image
                          : URL.createObjectURL(userDetails.profile_image)
                      })`,
                      backgroundSize: "cover",
                      backgroundPosition: "center",
                    }}
                  />
                  {editing && (
                    <Form.Group controlId="profilePhoto">
                      <Form.Label className="btn btn-outline-primary">
                        <FontAwesomeIcon icon={faUpload} className="me-2" />
                        Upload Photo
                        <Form.Control
                          type="file"
                          accept="image/*"
                          onChange={handleImageUpload}
                          hidden
                        />
                      </Form.Label>
                    </Form.Group>
                  )}
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};

export default ProfilePage;
