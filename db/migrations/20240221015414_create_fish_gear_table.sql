-- migrate:up

CREATE TABLE fish_gear (
    fish_id UUID NOT NULL,
    gear_id UUID NOT NULL,
    PRIMARY KEY (fish_id, gear_id),
    CONSTRAINT fk_fish_gear_fish FOREIGN KEY (fish_id) REFERENCES fish (id),
    CONSTRAINT fk_fish_gear_gear FOREIGN KEY (gear_id) REFERENCES gear (id)
);

-- migrate:down

DROP TABLE IF EXISTS fish_gear;
