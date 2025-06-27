-- create schema group1;
create table group1.chats(
	user_id varchar(255) not null,
    date_time DATETIME not null,
    user_prompt varchar(225),
    AI_objective_answer Text,
    AI_personalized_answer Text,
    primary key (user_id, date_time)
);
select * from group1.chats;
-- show databases
drop table group1.chats;



show columns from group1.summaries;
ALTER TABLE group1.summaries RENAME COLUMN date_time TO date;


create table group1.summaries(
	user_id varchar(255) not null,
    date_time datetime not null,
    summary text
);

alter table group1.summaries add primary key(user_id, date);

insert into group1.summaries (user_id, date_time, summary)
values ('user001', '2025-06-24 14:00:00', 'summarysummarysummarysummarysummary');

select * from group1.summaries;

create table group1.summaries(
	user_id varchar(255) not null,
    date_time datetime not null,
    summary text
);

ALTER TABLE group1.summaries MODIFY COLUMN date date;

insert into group1.summaries (user_id, date, summary)
values ('user001', '2025-06-24', 'summarysummarysummarysummarysummary');

delete from group1.summaries where user_id = 'user001';

truncate table group1.summaries;
select * from group1.summaries;

create table group1.EF(
	dimension int not null,
    sub_dimension int,
    detailed_category varcharacter(250),
    class int not null,
    content varcharacter(250) not null
);

insert into group1.EF(dimension, sub_dimension, detailed_category, class, content)
values(1, 1, 'sample_detailed_category', 5, 'sample_content');
alter table group1.EF add primary key(content);
select * from group1.EF;

create table group1.EPRs(
	user_id varchar(255) not null,
    project_name varchar(255) not null,
    start_date date not null,
	goal1 varchar(225),
    goal2 varchar(225),
    goal3 varchar(225),
    goal4 varchar(225),
    goal5 varchar(225)
);

insert into group1.EPRs(user_id, project_name, start_date, goal1, goal2, goal3, goal4)
values('user001', 'sample_project_name', '2025-06-24', 'goal1', 'goal2', 'goal3', 'goal4');
alter table group1.EPRs add primary key(user_id, start_date);
select * from group1.EPRs;

create table group1.quizzes(
	id int not null,
    quiz varchar(225) not null,
    answer varchar(225),
    answer1 varchar(225),
    answer2 varchar(225),
    answer3 varchar(225),
    answer4 varchar(225)
);
alter table group1.quizzes rename column answer1 to choice1;
alter table group1.quizzes rename column answer2 to choice2;
alter table group1.quizzes rename column answer3 to choice3;
alter table group1.quizzes rename column answer4 to choice4;

insert into group1.quizzes(id, quiz, answer, answer1, answer2, answer3, answer4)
values(1, 'sample quizz?', 'correct answer', 'option1', 'option2', 'option3', 'option4');
alter table group1.quizzes add primary key(id);
select * from group1.quizzes;

create table group1.users_last_action_date(
	user_id varchar(225) not null,
    last_login_date date,
    last_quiz_answer_date date
);

insert into group1.users_last_action_date(user_id, last_login_date, last_quiz_answer_date)
values('user001', '2025-06-24', '2025-06-24');
alter table group1.users_last_action_date add primary key(user_id);
select * from group1.users_last_action_date;
-- insert into group1.chats (user_id, date_time, AI_objective_answer, AI_personalized_answer)
-- values ('user001', '2025-06-24 14:00:00', 'samplesamplesamplesample', 'samplesamplesamplesample');


select * from group1.summaries;
select table_name
from information_schema.tables
where table_schema = 'group1';

create table group1.users(
	user_id varchar(225) not null primary key,
    email varcharacter(225) not null,
	class varcharacter(10) null,
    name varcharacter(225)
);

insert into group1.users(user_id, email, class, name)
values('user001', 'sample@emai.com', 'A', 'sample sample');
select * from group1.users;



