/* database creation */
drop table if exists news;
drop table if exists member;

/* create tables */
create table member(
    member_id integer primary key autoincrement not null,
    name text not null,
    email text not null unique,
    password text not null,
    authorisation integer not null
);


create table news(
    news_id integer primary key autoincrement not null,
    title text not null unique,
    subtitle text not null unique,
    content text not null unique,
    newsdate date not null,
    member_id integer not null,
    foreign key(member_id) references member(member_id)
);


insert into member(name, email, password, authorisation)
values('Julie', 'julie.bowen@gmail.com', 'temp', 0);
insert into member(name, email, password, authorisation)
values('Babette', 'babette.mccalman@yahoo.com', 'temp', 0);
insert into member(name, email, password, authorisation)
values('Simon', 'simon.li@hotmail.com', 'temp', 1);
insert into member(name, email, password, authorisation)
values('John', 'john.turner@outlook.com', 'temp', 1);


insert into news(title, subtitle, content, newsdate, member_id)
values('KB Player Named in NZ Team',
        'Congratulations!',
        'A huge congratulations to our very own Eason Young named to represent Team New Zealand in the 23rd BWF ' ||
        'World Junior Championships. Eason will be travelling to Spokane, USA, with his teammates and coaches from ' ||
        '25th September to the 8th October this year. Eason is a member of the NZ under19 training squad, KB senior ' ||
        'division team 1 & KB U19 team 1. Well done Eason!',
        '2023-08-03 08:57:41',
        (select member_id from member where name='Julie' )
);

insert into news(title, subtitle, content, newsdate, member_id)
values('Successful July for KB Juniors',
        'Well done to the U17 team!',
        'July has always been a busy month for our Juniors, especially with the biggest badminton competition in ' ||
        'New Zealand running. This year it was the 40th year anniversary for the New Zealand Junior Team '||
        'Championships. Across New Zealand 74 teams competed in Palmerston North''s Fly Arena. Wellington North '||
        'entered a team in U15, U17 and two teams in U19. Our U17s were undefeated in Division 2 of the NZ Junior ' ||
        'Teams Championships and proudly took home gold!',
        '2023-07-19 16:31:56',
        (select member_id from member where name='Simon' )
);

insert into news(title, subtitle, content, newsdate, member_id)
values('The Future of Court Hire',
        'Introducing the Stadium Pass',
        'Karori Badminton is launching a brand-new product, the Stadium Pass, that allows members and players to ' ||
        'play more badminton, more often. The Stadium Pass intends to provide a cost-effective way for players to '||
        'access courts, play amongst their friends, and practice badminton more often. The Stadium Pass allows pass '||
        'holders to have unlimited* access to our badminton courts for a month at a set price, without additional ' ||
        'court hire cost. This new court hire model is similar to squash and tennis, as well as comparable to a gym ' ||
        'membership. We will begin trialing this product later this year in October!',
        '2023-07-19 16:31:56',
        (select member_id from member where name='Babette' )
);