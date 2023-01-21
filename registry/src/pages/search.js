import React, { useState } from "react";
import "./search.css";

const Search = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSubmit = (event) => {
    event.preventDefault();
    const url = `http://127.0.0.1:9090/packages?query=${encodeURIComponent(query)}`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        setResults(data["packages"]);
      });
  };

  return (
    <div class="container">
     fpm-registry Package Search
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          id="query"
          name="query"
          placeholder="Enter your search query"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
        <button type="submit">Search</button>
      </form>
      <div id="result">
        {results.map((result) => (
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
  );
};

export default Search;