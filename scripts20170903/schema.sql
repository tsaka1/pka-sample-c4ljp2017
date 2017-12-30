
create table if not exists pwd (
  email text primary key,
  tstamp text default (datetime('now')),
  salt text not NULL,
  passwd text not NULL,
  status text not NULL
);

create table if not exists pka (
  email text primary key,
  tstamp text default (datetime('now')),
  salt text not NULL,
  pubkey text not NULL,
  status text not NULL
);

