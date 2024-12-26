USE Prueba;
CREATE TABLE users (
    id INT AUTO_INCREMENT,
    profile_image VARCHAR(255) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    correo VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE post (
    id INT AUTO_INCREMENT,
    title VARCHAR(80) NOT NULL,
    text_color VARCHAR(18) NOT NULL,
    card_color VARCHAR(18) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    content TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    users_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (users_id) REFERENCES users(id)
);

CREATE TABLE tokens_create_account(
    id INT AUTO_INCREMENT,
    correo VARCHAR(50) NOT NULL UNIQUE,
    token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE tokens_password(
    id INT AUTO_INCREMENT,
    user_correo VARCHAR(50) NOT NULL UNIQUE,
    token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_correo) REFERENCES users(correo)
);

