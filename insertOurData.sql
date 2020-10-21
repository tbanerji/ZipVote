-- inserts people, dates, questions, and more into tables

--politicians
load data local infile 'data/new Politicians.csv'
into table politicians
fields terminated by ','
lines terminated by '\n';

-- area and districts 
load data local infile 'data/newOffices.csv'
into table offices
fields terminated by ','
lines terminated by '\n';

--zipcode data
load data local infile 'data/newZipcodes.csv'
into table zipcodes
fields terminated by ','
lines terminated by '\n';

--whovotes
load data local infile 'data/whovotes_.csv'
into table whovotes
fields terminated by ','
lines terminated by '\n';

--policies
load data local infile 'data/policies.csv'
into table policies
fields terminated by ','
lines terminated by '\n';