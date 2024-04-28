-- migrate:up

-- Create ENUM type for status
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'suggested_common_name_status') THEN
        CREATE TYPE suggested_common_name_status AS ENUM ('PENDING', 'APPROVED', 'REJECTED');
    END IF;
END$$;

-- Create suggested_common_names table
CREATE TABLE suggested_common_names (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    suggested_name VARCHAR(255),
    status suggested_common_name_status DEFAULT 'PENDING',
    fish_id UUID,
    community_id UUID,
    CONSTRAINT fk_suggested_common_names_fish FOREIGN KEY (fish_id) REFERENCES fish (id) ON DELETE CASCADE,
    CONSTRAINT fk_suggested_common_names_community FOREIGN KEY (community_id) REFERENCES community (id) ON DELETE CASCADE
);

-- migrate:down

DROP TABLE IF EXISTS suggested_common_names;
DROP TYPE IF EXISTS suggested_common_name_status;
