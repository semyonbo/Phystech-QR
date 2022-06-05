DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS stats;

CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    original_url TEXT NOT NULL,
    clicks INTEGER NOT NULL DEFAULT 0,
    last_use TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stats (
    id_session INTEGER PRIMARY KEY AUTOINCREMENT,
    id INTEGER NOT NULL,
    time_use TIMESTAMP NOT NULL ,
    country TEXT,
    city TEXT,
    user_id TEXT
);