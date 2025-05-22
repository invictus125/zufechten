from datetime import datetime
from typing import List, Optional

from sqlalchemy import BigInteger, Column, DateTime, Double, ForeignKeyConstraint, Identity, Index, Integer, JSON, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlmodel import Field, Relationship, SQLModel

class Match(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint('id', name='match_pkey'),
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    status: int = Field(sa_column=Column('status', Integer, server_default=text('0')))

    elimmatch: List['Elimmatch'] = Relationship(back_populates='match')
    matchfencer: List['Matchfencer'] = Relationship(back_populates='match')
    poolmatch: List['Poolmatch'] = Relationship(back_populates='match')
    matchupdate: List['Matchupdate'] = Relationship(back_populates='match')


class Zufechtenuser(SQLModel, table=True):
    __table_args__ = (
        PrimaryKeyConstraint('id', name='zufechtenuser_pkey'),
        UniqueConstraint('email', name='zufechtenuser_email_key'),
        UniqueConstraint('username', name='zufechtenuser_username_key')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    username: str = Field(sa_column=Column('username', String(64)))
    email: str = Field(sa_column=Column('email', String(64)))
    first_name: str = Field(sa_column=Column('first_name', String(64)))
    surname: str = Field(sa_column=Column('surname', String(64)))
    auth_hash: Optional[str] = Field(default=None, sa_column=Column('auth_hash', String(64)))
    pronouns: Optional[str] = Field(default=None, sa_column=Column('pronouns', String(16)))
    bio_info: Optional[str] = Field(default=None, sa_column=Column('bio_info', Text))

    club: List['Club'] = Relationship(back_populates='owner')
    tournament: List['Tournament'] = Relationship(back_populates='organizer')
    userclub: List['Userclub'] = Relationship(back_populates='user')
    fencer: List['Fencer'] = Relationship(back_populates='user')


class Club(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['owner_id'], ['zufechtenuser.id'], name='club_owner_id_fkey'),
        PrimaryKeyConstraint('id', name='club_pkey'),
        UniqueConstraint('name', name='club_name_key')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    owner_id: int = Field(sa_column=Column('owner_id', BigInteger))
    name: str = Field(sa_column=Column('name', String(128)))
    address: Optional[dict] = Field(default=None, sa_column=Column('address', JSON))
    phone_number: Optional[str] = Field(default=None, sa_column=Column('phone_number', String(11)))
    email: Optional[str] = Field(default=None, sa_column=Column('email', String(64)))
    info: Optional[str] = Field(default=None, sa_column=Column('info', Text))

    owner: Optional['Zufechtenuser'] = Relationship(back_populates='club')
    tournamentclub: List['Tournamentclub'] = Relationship(back_populates='club')
    userclub: List['Userclub'] = Relationship(back_populates='club')


class Tournament(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['organizer_id'], ['zufechtenuser.id'], name='tournament_organizer_id_fkey'),
        PrimaryKeyConstraint('id', name='tournament_pkey'),
        UniqueConstraint('name', name='tournament_name_key')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    organizer_id: int = Field(sa_column=Column('organizer_id', BigInteger))
    name: str = Field(sa_column=Column('name', String(64)))
    date: datetime = Field(sa_column=Column('date', DateTime))
    config: dict = Field(sa_column=Column('config', JSON, server_default=text("'{}'::json")))
    status: int = Field(sa_column=Column('status', Integer, server_default=text('0')))
    location: dict = Field(sa_column=Column('location', JSON, server_default=text("'{}'::json")))
    info: Optional[str] = Field(default=None, sa_column=Column('info', Text))

    organizer: Optional['Zufechtenuser'] = Relationship(back_populates='tournament')
    event: List['Event'] = Relationship(back_populates='tournament')
    tournamentclub: List['Tournamentclub'] = Relationship(back_populates='tournament')
    fencer: List['Fencer'] = Relationship(back_populates='tournament')


class Event(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['tournament_id'], ['tournament.id'], name='event_tournament_id_fkey'),
        PrimaryKeyConstraint('id', name='event_pkey')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    name: str = Field(sa_column=Column('name', String(64)))
    tournament_id: int = Field(sa_column=Column('tournament_id', BigInteger))
    date: datetime = Field(sa_column=Column('date', DateTime))
    config: dict = Field(sa_column=Column('config', JSON, server_default=text("'{}'::json")))
    status: int = Field(sa_column=Column('status', Integer, server_default=text('0')))

    tournament: Optional['Tournament'] = Relationship(back_populates='event')
    eliminations: List['Eliminations'] = Relationship(back_populates='event')
    pool: List['Pool'] = Relationship(back_populates='event')
    eventfencer: List['Eventfencer'] = Relationship(back_populates='event')


class Tournamentclub(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['club_id'], ['club.id'], name='tournamentclub_club_id_fkey'),
        ForeignKeyConstraint(['tournament_id'], ['tournament.id'], name='tournamentclub_tournament_id_fkey'),
        PrimaryKeyConstraint('id', name='tournamentclub_pkey'),
        UniqueConstraint('name', 'tournament_id', name='tournamentclub_name_tournament_id_key')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    name: str = Field(sa_column=Column('name', String(64)))
    tournament_id: int = Field(sa_column=Column('tournament_id', BigInteger))
    club_id: Optional[int] = Field(default=None, sa_column=Column('club_id', BigInteger))

    club: Optional['Club'] = Relationship(back_populates='tournamentclub')
    tournament: Optional['Tournament'] = Relationship(back_populates='tournamentclub')
    fencer: List['Fencer'] = Relationship(back_populates='tournamentclub')


class Userclub(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['club_id'], ['club.id'], name='userclub_club_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['zufechtenuser.id'], name='userclub_user_id_fkey'),
        PrimaryKeyConstraint('id', name='userclub_pkey'),
        UniqueConstraint('user_id', 'club_id', name='userclub_user_id_club_id_key')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    user_id: int = Field(sa_column=Column('user_id', BigInteger))
    club_id: int = Field(sa_column=Column('club_id', BigInteger))
    permissions: dict = Field(sa_column=Column('permissions', JSON, server_default=text("'{}'::json")))

    club: Optional['Club'] = Relationship(back_populates='userclub')
    user: Optional['Zufechtenuser'] = Relationship(back_populates='userclub')


class Eliminations(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['event_id'], ['event.id'], name='eliminations_event_id_fkey'),
        PrimaryKeyConstraint('id', name='eliminations_pkey')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    event_id: int = Field(sa_column=Column('event_id', BigInteger))
    config: dict = Field(sa_column=Column('config', JSON, server_default=text("'{}'::json")))

    event: Optional['Event'] = Relationship(back_populates='eliminations')
    elimmatch: List['Elimmatch'] = Relationship(back_populates='elim')


class Fencer(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['club_affiliation'], ['tournamentclub.id'], name='fencer_club_affiliation_fkey'),
        ForeignKeyConstraint(['tournament_id'], ['tournament.id'], name='fencer_tournament_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['zufechtenuser.id'], name='fencer_user_id_fkey'),
        PrimaryKeyConstraint('id', name='fencer_pkey')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    alias: str = Field(sa_column=Column('alias', String(64)))
    tournament_id: int = Field(sa_column=Column('tournament_id', BigInteger))
    user_id: Optional[int] = Field(default=None, sa_column=Column('user_id', BigInteger))
    club_affiliation: Optional[int] = Field(default=None, sa_column=Column('club_affiliation', BigInteger))

    tournamentclub: Optional['Tournamentclub'] = Relationship(back_populates='fencer')
    tournament: Optional['Tournament'] = Relationship(back_populates='fencer')
    user: Optional['Zufechtenuser'] = Relationship(back_populates='fencer')
    eventfencer: List['Eventfencer'] = Relationship(back_populates='fencer')
    matchfencer: List['Matchfencer'] = Relationship(back_populates='fencer')


class Pool(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['event_id'], ['event.id'], name='pool_event_id_fkey'),
        PrimaryKeyConstraint('id', name='pool_pkey')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    event_id: int = Field(sa_column=Column('event_id', BigInteger))

    event: Optional['Event'] = Relationship(back_populates='pool')
    poolmatch: List['Poolmatch'] = Relationship(back_populates='pool')


class Elimmatch(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['elim_id'], ['eliminations.id'], name='elimmatch_elim_id_fkey'),
        ForeignKeyConstraint(['match_id'], ['match.id'], name='elimmatch_match_id_fkey'),
        PrimaryKeyConstraint('id', name='elimmatch_pkey'),
        UniqueConstraint('elim_id', 'match_id', name='elimmatch_elim_id_match_id_key')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    elim_id: int = Field(sa_column=Column('elim_id', BigInteger))
    match_id: int = Field(sa_column=Column('match_id', BigInteger))

    elim: Optional['Eliminations'] = Relationship(back_populates='elimmatch')
    match: Optional['Match'] = Relationship(back_populates='elimmatch')


class Eventfencer(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['event_id'], ['event.id'], name='eventfencer_event_id_fkey'),
        ForeignKeyConstraint(['fencer_id'], ['fencer.id'], name='eventfencer_fencer_id_fkey'),
        PrimaryKeyConstraint('id', name='eventfencer_pkey'),
        UniqueConstraint('event_id', 'fencer_id', name='eventfencer_event_id_fencer_id_key')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    event_id: int = Field(sa_column=Column('event_id', BigInteger))
    fencer_id: int = Field(sa_column=Column('fencer_id', BigInteger))
    status: int = Field(sa_column=Column('status', Integer, server_default=text('0')))

    event: Optional['Event'] = Relationship(back_populates='eventfencer')
    fencer: Optional['Fencer'] = Relationship(back_populates='eventfencer')


class Matchfencer(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['fencer_id'], ['fencer.id'], name='matchfencer_fencer_id_fkey'),
        ForeignKeyConstraint(['match_id'], ['match.id'], name='matchfencer_match_id_fkey'),
        PrimaryKeyConstraint('id', name='matchfencer_pkey'),
        UniqueConstraint('match_id', 'fencer_id', name='matchfencer_match_id_fencer_id_key')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    match_id: int = Field(sa_column=Column('match_id', BigInteger))
    fencer_id: int = Field(sa_column=Column('fencer_id', BigInteger))
    status: int = Field(sa_column=Column('status', Integer, server_default=text('0')))

    fencer: Optional['Fencer'] = Relationship(back_populates='matchfencer')
    match: Optional['Match'] = Relationship(back_populates='matchfencer')
    matchfencerpenalty: List['Matchfencerpenalty'] = Relationship(back_populates='match_fencer')
    matchupdate: List['Matchupdate'] = Relationship(back_populates='match_fencer')


class Poolmatch(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['match_id'], ['match.id'], name='poolmatch_match_id_fkey'),
        ForeignKeyConstraint(['pool_id'], ['pool.id'], name='poolmatch_pool_id_fkey'),
        PrimaryKeyConstraint('id', name='poolmatch_pkey'),
        UniqueConstraint('pool_id', 'match_id', name='poolmatch_pool_id_match_id_key')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    pool_id: int = Field(sa_column=Column('pool_id', BigInteger))
    match_id: int = Field(sa_column=Column('match_id', BigInteger))

    match: Optional['Match'] = Relationship(back_populates='poolmatch')
    pool: Optional['Pool'] = Relationship(back_populates='poolmatch')


class Matchfencerpenalty(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['match_fencer_id'], ['matchfencer.id'], name='matchfencerpenalty_match_fencer_id_fkey'),
        PrimaryKeyConstraint('id', name='matchfencerpenalty_pkey'),
        UniqueConstraint('type', 'match_fencer_id', name='matchfencerpenalty_type_match_fencer_id_key'),
        Index('penalty_fencer_type', 'type', 'match_fencer_id')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    type: str = Field(sa_column=Column('type', String(32)))
    match_fencer_id: int = Field(sa_column=Column('match_fencer_id', BigInteger))
    count: int = Field(sa_column=Column('count', Integer, server_default=text('0')))

    match_fencer: Optional['Matchfencer'] = Relationship(back_populates='matchfencerpenalty')


class Matchupdate(SQLModel, table=True):
    __table_args__ = (
        ForeignKeyConstraint(['match_fencer_id'], ['matchfencer.id'], name='matchupdate_match_fencer_id_fkey'),
        ForeignKeyConstraint(['match_id'], ['match.id'], name='matchupdate_match_id_fkey'),
        PrimaryKeyConstraint('id', name='matchupdate_pkey'),
        Index('match_update_fencer_type', 'type', 'match_fencer_id', 'match_id')
    )

    id: Optional[int] = Field(default=None, sa_column=Column('id', BigInteger, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True))
    timestamp: datetime = Field(sa_column=Column('timestamp', DateTime, server_default=text('now()')))
    type: str = Field(sa_column=Column('type', String(32)))
    match_fencer_id: int = Field(sa_column=Column('match_fencer_id', BigInteger))
    match_id: int = Field(sa_column=Column('match_id', BigInteger))
    value: float = Field(sa_column=Column('value', Double(53), server_default=text('0')))
    new_match_state: dict = Field(sa_column=Column('new_match_state', JSON))

    match_fencer: Optional['Matchfencer'] = Relationship(back_populates='matchupdate')
    match: Optional['Match'] = Relationship(back_populates='matchupdate')
