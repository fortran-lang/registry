import React from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Container, InputGroup, FormControl } from "react-bootstrap";
import { searchPackage, setQuery } from "../store/actions/searchActions";

import "../home.css";

const Home = () => {
  return (
    <Container id="home-container">
      <div id="fpm-logo">
        <img src="https://raw.githubusercontent.com/fortran-lang/assets/main/fpm/logo/2-color-alt/png/full-color-alt.png" />
      </div>

      <HomeSearchField type="text" placeholder="Search package" />
      <p id="fpm-subscript">The official registry for fpm packages</p>
    </Container>
  );
};

export default Home;

function HomeSearchField(props) {
  const query = useSelector((state) => state.search.query);
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const search = () => {
    if (query.trim().length !== 0) {
      dispatch(searchPackage(query, 0));
      navigate("/search");
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      search();
    }
  };

  return (
    <InputGroup>
      <FormControl
        type={props.type}
        placeholder={props.placeholder}
        id="home-search"
        onKeyDown={handleKeyDown}
        onChange={(event) => dispatch(setQuery(event.target.value))}
      />
    </InputGroup>
  );
}
