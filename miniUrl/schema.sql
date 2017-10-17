drop table if exists miniUrls;
create table miniUrls (
   id integer primary key autoincrement,
   createdTimestamp integer not null
);

drop table if exists targetTypes;
create table targetTypes (
   id integer primary key autoincrement,
   type text not null
);

drop table if exists targetUrls;
create table targetUrls (
   miniUrlId integer not null,
   targetUrl text not null,
   typeId integer not null,
   hits integer not null default 0,
   foreign key (miniUrlId) references miniUrls(id),
   foreign key (typeId) references targetTypes(id),
   primary key (miniUrlId, typeId)
);

insert into targetTypes(type) values ('default'), ('mobile'), ('tablet');