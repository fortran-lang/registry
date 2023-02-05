<Container>Account</Container>
    <Table>
      <tbody>
          <tr><Image src={`https://www.gravatar.com/avatar/${username}`} alt={`Avatar for ${username} from gravatar.com`} title={`Avatar for ${username} from gravatar.com`} ></Image></tr>
          <tr>{ CreatedAt }</tr>
          {console.log(CreatedAt)}
          <tr><h6><MDBIcon fas icon="user-circle" /> {username}</h6></tr>
          <tr></tr>
      </tbody>
    </Table>
    
      {packages.map((element, index) => (
          <Card key={index}>
            <Card.Body>
              <Card.Title>{element.name}</Card.Title>
              <Card.Subtitle className="mb-2 text-muted">
                {element.namespace_name}
              </Card.Subtitle>
              <Card.Text id="card-text">{element.description}</Card.Text>
            </Card.Body>
          </Card>
      ))}



<Container>
      <Form id="login-form" onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <h1>Welcome to fpm Registry!</h1>

          <Form.Label>Email address</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Form.Text className="text-muted">
            We'll never share your email with anyone else.
          </Form.Text>
        </Form.Group>

        <Form.Group className="mb-4" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          Submit
        </Button>
        <Form.Text id="error" className="text-muted">
          {""}
        </Form.Text>
      </Form>
    </Container>

    <form id="login-form" onSubmit={handleSubmit}>
      <h1>Welcome to fpm Registry!</h1>
      <p>Please enter your email and password to log in.</p>
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <p id="error" className="error"></p>
      <input type="submit" value="Log In" />
    </form>