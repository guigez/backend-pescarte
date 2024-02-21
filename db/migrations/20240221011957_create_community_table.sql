-- migrate:up

CREATE TABLE community (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    municipality_id UUID,
    CONSTRAINT fk_community_municipality FOREIGN KEY (municipality_id)
    REFERENCES municipality (id)
);

-- migrate:down

DROP TABLE IF EXISTS community;
