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
    status ENUM('public', 'private', 'disabled') NOT NULL,
    users_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE CASCADE
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
    FOREIGN KEY (user_correo) REFERENCES users(correo) ON DELETE CASCADE
);

CREATE TABLE comments(
    id INT AUTO_INCREMENT,
    content VARCHAR(300) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    is_public BOOLEAN NOT NULL,
    users_id INT NOT NULL,
    post_id INT NOT NULL,
    parent_comment_id INT DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES post(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_comment_id) REFERENCES comments(id) ON DELETE CASCADE
);