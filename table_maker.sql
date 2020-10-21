use zipvote_db;
 
/*
drop table if exists candidate_answers;
drop table if exists topic;
drop table if exists topic_questions;
*/
 
drop table if exists policies;
drop table if exists whovotes;
drop table if exists runningfor;
drop table if exists zipcodes;
drop table if exists offices;
drop table if exists politicians;
 
 
--politicians is a table with data on all MA elected officials
-- contains basic biographic details as well as links to campaign social media
-- includes link to an image
create table politicians (
   person_id int unsigned auto_increment,
   name varchar(50),
   dob date,
   party enum('Democrat', 'Republican', 'Independent', 'Unknown', 'Other'),
   infolink varchar(50),
   imglink varchar(400),
   primary key (person_id)
)
Engine = InnoDB;
 
-- offices contains info on an office, who it's held by, the data of the next election,etc
create table offices (
   o_id int unsigned auto_increment,
   oname varchar(75),
   ostate varchar(3),
   heldby int,
   tyears int,
   terms int,
   nextvote date,
   -- index (heldby),
   primary key (o_id)
)
Engine = InnoDB;
 
 
-- zipcodes contains details on MA zipcodes, states, town names, counties, etc
create table zipcodes (
   zipcode char(5),
   state varchar(30),
   city_or_town varchar(30),
   county varchar(30),
   primary key (zipcode)
)
Engine = InnoDB;
 
-- runningfor contains info from politicians and offices about who's running for which position
create table runningfor(
   person_id int unsigned,
   o_id int unsigned,
   foreign key (o_id) references offices(o_id),
   foreign key (person_id) references politicians(person_id)
)
Engine = InnoDB;
 
-- whovotes connects politician's ids with what zipcodes they serve
create table whovotes(
   o_id int unsigned,
   zipcode char(5),
   foreign key (o_id) references offices(o_id),
   foreign key (zipcode) references zipcodes(zipcode)
)
Engine = InnoDB;
-- contains info on policies supported by a specific politician
create table policies (
   person_id int unsigned auto_increment,
   policies varchar(150),
   stance enum ('opposes','supports'),
 
   foreign key (person_id) references politicians(person_id)
 
)
 
Engine = InnoDB;
