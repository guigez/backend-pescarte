-- migrate:up

CREATE TABLE municipality (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    uf VARCHAR(2),
    CONSTRAINT fk_municipality_uf FOREIGN KEY (uf)
    REFERENCES uf (uf)
);

-- migrate:down

DROP TABLE IF EXISTS municipality;
