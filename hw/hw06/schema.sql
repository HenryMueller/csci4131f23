CREATE TABLE contacts (
    user VARCHAR(50) NOT NULL,              -- Name
    id INT NOT NULL AUTO_INCREMENT,         -- ID / Number
    email VARCHAR(50) NOT NULL,             -- EMAIL
    appointment DATE NOT NULL,              -- Appointment date
    qtype VARCHAR(8) NOT NULL,              -- Question, Comment, Concern, or Other
    ssn BOOLEAN NOT NULL DEFAULT FALSE,     -- If SSN is included
    PRIMARY KEY(id)
);

CREATE TABLE sales (
    id INT NOT NULL AUTO_INCREMENT,         -- Number of this sale
    sale TEXT NOT NULL,                     -- Text of the sale
    begins TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,    -- start of the sale
    ends TIMESTAMP DEFAULT NULL,                 -- end of the sale
    PRIMARY KEY(id)
);