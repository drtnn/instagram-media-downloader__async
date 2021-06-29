CREATE TABLE users
(
    id          SERIAL  NOT NULL,
    user_id     INTEGER NOT NULL UNIQUE,
    username    VARCHAR(128),
    first_name  VARCHAR(128),
    referral    INTEGER,
    balance     INTEGER DEFAULT 0 NOT NULL
)

alter table users
    owner to postgres;

create unique index users_id_index
    on users (id);

create unique index users_user_id_index
    on users (user_id);