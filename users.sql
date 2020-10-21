-- Creates a table that stores user passwords 
drop table if exists userpass;

create table userpass(
       uid int auto_increment,
       username varchar(50) not null,
       hashed char(60),
       unique(username),
       index(username),
       primary key (uid)
)
Engine = InnoDB;
select * from userpass;

drop table if exists user_favs;
-- contains info on a user's favourite politicians
create table user_favs (
	username varchar(50) not null,
       person_id int unsigned auto_increment, 
       name varchar (50),
       feeling enum('supports', 'strongly supports', 'opposes', 'strongly opposes'),
	foreign key (person_id) references politicians(person_id),
       foreign key (username) references userpass(username)

)

Engine = InnoDB;