-- migrate:up
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE fish_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fish_id UUID NOT NULL,
    image_data BYTEA NOT NULL,
    content_type VARCHAR(255) NOT NULL,
    CONSTRAINT fk_fish FOREIGN KEY (fish_id) REFERENCES fish (id) ON DELETE CASCADE
);

-- migrate:down
DROP TABLE fish_images;
