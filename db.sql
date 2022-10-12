create table economy (
  id bigint not null primary key,
  wallet bigint,
  bank bigint
);

create table guild_settings (
  id bigint not null primary key,
  leveling boolean,
  logging bigint,
  welcoming bigint,
  autorole bigint
);

