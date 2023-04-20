import React from "react";
import { Container } from "react-bootstrap";

import "../home.css";

const Home = () => {
  return (
    <Container className="home-container">
      <h2>Fortran</h2>
      <h2>High-performance parallel programming language</h2>
      <div className="features-list">
        <h2 className="heading-features">Features</h2>
        <h4>High Performance</h4>
        <p>
          Fortran has been designed from the ground up for computationally
          intensive applications in science and engineering. Mature and
          battle-tested compilers and libraries allow you to write code that
          runs close to metal, fast.
        </p>
        <h4>Statically and strongly typed</h4>
        <p>
          Fortran is statically and strongly typed, which allows the compiler to
          catch many programming errors early on for you. This also allows the
          compiler to generate efficient binary code.
        </p>
        <h4>Easy to learn and use</h4>
        <p>
          Fortran is a relatively small language that is surprisingly easy to
          learn and use. Expressing most mathematical and arithmetic operations
          over large arrays is as simple as writing them as equations on a
          whiteboard.
        </p>
        <h4>Versatile</h4>
        <p>
          Fortran allows you to write code in a style that best fits your
          problem: imperative, procedural, array-oriented, object-oriented, or
          functional.
        </p>
        <h4>Natively parallel</h4>
        <p>
          Fortran is a natively parallel programming language with intuitive
          array-like syntax to communicate data between CPUs. You can run almost
          the same code on a single CPU, on a shared-memory multicore system, or
          on a distributed-memory HPC or cloud-based system. Coarrays, teams,
          events, and collective subroutines allow you to express different
          parallel programming patterns that best fit your problem at hand.
        </p>
      </div>
    </Container>
  );
};

export default Home;
