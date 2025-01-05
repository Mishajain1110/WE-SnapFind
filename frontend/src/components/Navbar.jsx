import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";
import "../styles/Navbar.css";
import Profile3 from "../assets/profile.png";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faUserCircle,
  faCog,
  faEnvelopeOpen,
  faUserShield,
  faSignOutAlt,
} from "@fortawesome/free-solid-svg-icons";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";
import { useAuthentication } from "../auth";

function AppNavbar() {
  const { isAuthorized, logout } = useAuthentication();
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/");
    logout();
  };

  return (
    <Navbar bg="light" expand="lg" className="shadow-sm">
      <Container>
        <Navbar.Brand as={Link} to="/">
          <img src={logo} alt="Logo" className="navbar-logo" />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="navbar-nav" />
        <Navbar.Collapse id="navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/why">
              Why Us?
            </Nav.Link>
            <Nav.Link as={Link} to="/about">
              About
            </Nav.Link>
            <Nav.Link as={Link} to="/contact">
              Contact
            </Nav.Link>
            {isAuthorized && (
              <Nav.Link as={Link} to="/lost-found">
                Lost/Found Item Form
              </Nav.Link>
            )}
          </Nav>
          <Nav className="ms-auto">
            {!isAuthorized ? (
              <>
                <Nav.Link as={Link} to="/login" className="btn btn-primary me-2">
                  Log In
                </Nav.Link>
                <Nav.Link as={Link} to="/register" className="btn btn-outline-primary">
                  Register
                </Nav.Link>
              </>
            ) : (
              <NavDropdown
                title={
                  <img
                    src={Profile3}
                    alt="Profile"
                    className="user-avatar rounded-circle"
                    style={{ width: "40px", height: "40px"}}
                  />
                }
                id="user-dropdown"
                align="end"
                style={{ margin: "0", padding: "0"}}
              >
                <NavDropdown.Item as={Link} to="/profile">
                  <FontAwesomeIcon icon={faUserCircle} className="me-2" />
                  My Profile
                </NavDropdown.Item>
                <NavDropdown.Item>
                  <FontAwesomeIcon icon={faCog} className="me-2" />
                  Settings
                </NavDropdown.Item>
                <NavDropdown.Item>
                  <FontAwesomeIcon icon={faEnvelopeOpen} className="me-2" />
                  Messages
                </NavDropdown.Item>
                <NavDropdown.Item>
                  <FontAwesomeIcon icon={faUserShield} className="me-2" />
                  Support
                </NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item onClick={handleLogout} className="text-danger">
                  <FontAwesomeIcon icon={faSignOutAlt} className="me-2" />
                  Logout
                </NavDropdown.Item>
              </NavDropdown>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default AppNavbar;
