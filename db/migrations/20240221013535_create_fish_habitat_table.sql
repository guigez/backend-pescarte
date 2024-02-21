-- migrate:up

CREATE TABLE fish_habitat (
    fish_id UUID NOT NULL,
    habitat_id UUID NOT NULL,
    PRIMARY KEY (fish_id, habitat_id),
    CONSTRAINT fk_fish_habitat_fish FOREIGN KEY (fish_id) REFERENCES fish (id),
    CONSTRAINT fk_fish_habitat_habitat FOREIGN KEY (habitat_id) REFERENCES habitat (id)
);

-- migrate:down

DROP TABLE IF EXISTS fish_habitat;
