-- migrate:up

CREATE TABLE gear (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) UNIQUE NOT NULL
);

-- migrate:down

DROP TABLE IF EXISTS gear;
