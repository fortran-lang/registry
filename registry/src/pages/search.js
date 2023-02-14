import React, { useState } from "react";
import { useSelector } from "react-redux";

const Search = () => {
  const packages = useSelector((state) => state.search.packages);

  return packages != null ? (
    packages.length == 0 ? (
      <div className="container">
        <div id="result">No packages found.</div>
      </div>
    ) : (
      <div className="container">
        fpm-registry Package Search
        <div id="result">
          {packages.map((result) => (
            <div>
              <h2>{result.name}</h2>
              <p>{result.description}</p>
              <p>{result.author}</p>
              <p>{result.description}</p>
              <p>{result.namespace}</p>
            </div>
          ))}
        </div>
      </div>
    )
  ) : null;
};

export default Search;
