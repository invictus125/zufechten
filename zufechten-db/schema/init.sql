--User and Club basic entity setup--

CREATE TABLE IF NOT EXISTS ZufechtenUser (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username    varchar(64) NOT NULL UNIQUE,
    auth_hash   varchar(64),
    email       varchar(64) NOT NULL UNIQUE,
    first_name  varchar(64) NOT NULL,
    surname     varchar(64) NOT NULL,
    pronouns    varchar(16),
    bio_info    text
);

CREATE TABLE IF NOT EXISTS Club (
    id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner_id        bigint references ZufechtenUser(id) NOT NULL,
    name            varchar(128) NOT NULL UNIQUE,
    address         json,
    phone_number    varchar(11),
    email           varchar(64),
    info            text
);

CREATE TABLE IF NOT EXISTS UserClub (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id     bigint references ZufechtenUser(id) NOT NULL,
    club_id     bigint references Club(id) NOT NULL,
    permissions json NOT NULL DEFAULT '{}',
    UNIQUE(user_id, club_id)
);

--Tournament basic entity setup--

CREATE TABLE IF NOT EXISTS Tournament (
    id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    organizer_id    bigint references ZufechtenUser(id) NOT NULL,
    name            varchar(64) NOT NULL UNIQUE,
    date            timestamp NOT NULL,
    config          json NOT NULL DEFAULT '{}',
    info            text,
    status          int NOT NULL DEFAULT 0,
    location        json NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS TournamentClub (
    id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name            varchar(64) NOT NULL,
    tournament_id   bigint references Tournament(id) NOT NULL,
    club_id         bigint references Club(id),
    UNIQUE(name, tournament_id)
);

CREATE TABLE IF NOT EXISTS Event (
    id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name            varchar(64) NOT NULL,
    tournament_id   bigint references Tournament(id) NOT NULL,
    date            timestamp NOT NULL,
    config          json NOT NULL DEFAULT '{}',
    status          int NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Pool (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_id    bigint references Event(id) NOT NULL
);

CREATE TABLE IF NOT EXISTS Eliminations (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_id    bigint references Event(id) NOT NULL,
    config      json NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS Match (
    id      bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    status  int NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Fencer (
    id                  bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    alias               varchar(64) NOT NULL,
    user_id             bigint references ZufechtenUser(id),
    tournament_id       bigint references Tournament(id) NOT NULL,
    club_affiliation    bigint references TournamentClub(id)
);

--Relation type setup--

CREATE TABLE IF NOT EXISTS PoolMatch (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pool_id     bigint references Pool(id) NOT NULL,
    match_id    bigint references Match(id) NOT NULL,
    UNIQUE(pool_id, match_id)
);

CREATE TABLE IF NOT EXISTS ElimMatch (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    elim_id     bigint references Eliminations(id) NOT NULL,
    match_id    bigint references Match(id) NOT NULL,
    UNIQUE(elim_id, match_id)
);

CREATE TABLE IF NOT EXISTS MatchFencer (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    match_id    bigint references Match(id) NOT NULL,
    fencer_id   bigint references Fencer(id) NOT NULL,
    status      int NOT NULL DEFAULT 0,
    UNIQUE(match_id, fencer_id)
);

CREATE TABLE IF NOT EXISTS EventFencer (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_id    bigint references Event(id) NOT NULL,
    fencer_id   bigint references Fencer(id) NOT NULL,
    status      int NOT NULL DEFAULT 0,
    UNIQUE(event_id, fencer_id)
);

--Match record setup--

CREATE TABLE IF NOT EXISTS MatchUpdate (
    id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    timestamp       timestamp NOT NULL DEFAULT now(),
    type            varchar(32) NOT NULL,
    match_fencer_id bigint references MatchFencer(id) NOT NULL,
    match_id        bigint references Match(id) NOT NULL,
    value           double precision NOT NULL DEFAULT 0,
    new_match_state json NOT NULL
);

CREATE INDEX IF NOT EXISTS match_update_fencer_type ON MatchUpdate(type, match_fencer_id, match_id);

CREATE TABLE IF NOT EXISTS MatchFencerPenalty (
    id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type            varchar(32) NOT NULL,
    match_fencer_id bigint references MatchFencer(id) NOT NULL,
    count           int NOT NULL DEFAULT 0,
    UNIQUE(type, match_fencer_id)
);

CREATE INDEX IF NOT EXISTS penalty_fencer_type ON MatchFencerPenalty(type, match_fencer_id);