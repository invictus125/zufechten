CREATE DATABASE Zufechten;

--User and Club basic entity setup--

CREATE TABLE User (
    id          bigint GENERATED ALWAYS AS IDENTITY,
    username    varchar(64) NOT NULL CONSTRAINT uniq_username UNIQUE,
    auth_hash   varchar(64),
    email       varchar(64) NOT NULL CONSTRAINT uniq_email UNIQUE,
    first_name  varchar(64) NOT NULL,
    surname     varchar(64) NOT NULL,
    pronouns    varchar(16),
    bio_info    text,
);

CREATE TABLE Club (
    id              bigint GENERATED ALWAYS AS IDENTITY,
    owner_id        bigint references User(id) NOT NULL,
    name            varchar(128) NOT NULL CONSTRAINT uniq_name UNIQUE,
    address         json,
    phone_number    varchar(11),
    email           varchar(64),
    info            text,
);

CREATE TABLE UserClub (
    id          bigint GENERATED ALWAYS AS IDENTITY,
    user_id     bigint references User(id) NOT NULL,
    club_id     bigint references Club(id) NOT NULL,
    permissions json NOT NULL DEFAULT '{}',
    UNIQUE(user_id, club_id)
);

--Tournament basic entity setup--

CREATE TABLE Tournament (
    id              bigint GENERATED ALWAYS AS IDENTITY,
    organizer_id    bigint references User(id) NOT NULL,
    name            varchar(64) NOT NULL CONSTRAINT uniq_name UNIQUE,
    date            timestamp NOT NULL,
    config          json NOT NULL DEFAULT '{}',
    info            text,
    status          int NOT NULL DEFAULT 0,
    location        json NOT NULL DEFAULT '{}',
);

CREATE TABLE TournamentClub (
    id              bigint GENERATED ALWAYS AS IDENTITY,
    name            varchar(64) NOT NULL,
    tournament_id   bigint references Tournament(id) NOT NULL,
    club_id         bigint references Club(id),
    UNIQUE(name, tournament_id)
);

CREATE TABLE Event (
    id              bigint GENERATED ALWAYS AS IDENTITY,
    name            varchar(64) NOT NULL,
    tournament_id   bigint references Tournament(id) NOT NULL,
    date            timestamp NOT NULL,
    config          json NOT NULL DEFAULT '{}',
    status          int NOT NULL DEFAULT 0
);

CREATE TABLE Pool (
    id          bigint GENERATED ALWAYS AS IDENTITY,
    event_id    bigint references Event(id) NOT NULL
);

CREATE TABLE Eliminations (
    id          bigint GENERATED ALWAYS AS IDENTITY,
    event_id    bigint references Event(id) NOT NULL,
    config      json NOT NULL DEFAULT '{}'
);

CREATE TABLE Match (
    id      bigint GENERATED ALWAYS AS IDENTITY,
    status  int NOT NULL DEFAULT 0
);

CREATE TABLE Fencer (
    id                  bigint GENERATED ALWAYS AS IDENTITY,
    alias               varchar(64) NOT NULL,
    user_id             bigint references User(id),
    tournament_id       bigint references Tournament(id) NOT NULL,
    club_affiliation    bigint references TournamentClub(id)
);

--Relation type setup--

CREATE TABLE PoolMatch (
    id          bigint GENERATED ALWAYS AS IDENTITY,
    pool_id     bigint references Pool(id) NOT NULL,
    match_id    bigint references Match(id) NOT NULL,
    UNIQUE(pool_id, match_id)
);

CREATE TABLE ElimMatch (
    id          bigint GENERATED ALWAYS AS IDENTITY,
    elim_id     bigint references Eliminations(id) NOT NULL,
    match_id    bigint references Match(id) NOT NULL,
    UNIQUE(elim_id, match_id)
);

CREATE TABLE MatchFencer (
    id          bigint GENERATED ALWAYS AS IDENTITY,
    match_id    bigint references Match(id) NOT NULL,
    fencer_id   bigint references Fencer(id) NOT NULL,
    status      int NOT NULL DEFAULT 0,
    UNIQUE(match_id, fencer_id)
);

CREATE TABLE EventFencer (
    id          bigint GENERATED ALWAYS AS IDENTITY,
    event_id    bigint references Event(id) NOT NULL,
    fencer_id   bigint references Fencer(id) NOT NULL,
    status      int NOT NULL DEFAULT 0,
    UNIQUE(event_id, fencer_id)
);

--Match record setup--

CREATE TABLE MatchUpdate (
    id              bigint GENERATED ALWAYS AS IDENTITY,
    type            varchar(32) NOT NULL,
    match_fencer_id bigint references MatchFencer(id) NOT NULL,
    match_id        bigint references Match(id) NOT NULL,
    value           double precision NOT NULL DEFAULT 0,
    new_match_state json NOT NULL
);

CREATE INDEX match_update_fencer_type ON MatchUpdate(type, match_fencer_id, match_id);

CREATE TABLE MatchFencerPenalty (
    id              bigint GENERATED ALWAYS AS IDENTITY,
    type            varchar(32) NOT NULL,
    match_fencer_id bigint references MatchFencer(id) NOT NULL,
    count           int NOT NULL DEFAULT 0,
    UNIQUE(type, match_fencer_id)
);

CREATE INDEX penalty_fencer_type ON MatchFencerPenalty(type, match_fencer_id);