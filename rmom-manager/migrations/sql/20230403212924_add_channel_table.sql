CREATE TABLE channel (
    id            UUID PRIMARY KEY,
    queue_id      UUID NOT NULL,
    topic         VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    updated_at    TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    CONSTRAINT    fk_queue FOREIGN KEY(queue_id) REFERENCES queue(id) ON DELETE CASCADE
);