-- migrate:up

CREATE TABLE fish_common_name_by_community (
    common_name VARCHAR(255) NOT NULL,
    fish_id UUID NOT NULL,
    community_id UUID NOT NULL,
    PRIMARY KEY (fish_id, community_id, common_name),
    CONSTRAINT fk_fish_common_name_fish FOREIGN KEY (fish_id) REFERENCES fish (id),
    CONSTRAINT fk_fish_common_name_community FOREIGN KEY (community_id) REFERENCES community (id)
);

-- migrate:down

DROP TABLE IF EXISTS fish_common_name_by_community;
