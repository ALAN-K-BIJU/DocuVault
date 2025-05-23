CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    password_hash TEXT
);

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    owner VARCHAR(100),
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE versions (
    id SERIAL PRIMARY KEY,
    document_id INT,
    s3_version_id VARCHAR(255),
    comment TEXT,
    uploaded_by VARCHAR(100),
    FOREIGN KEY (document_id) REFERENCES documents(id)
);
