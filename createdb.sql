create table daily_rate(
    id integer primary key,
    rate float
);

create table payment_method(
    codename varchar(255) primary key,
    name varchar(255),
    aliases text
);

create table delivery(
    id integer primary key,
    amount float,
    created datetime,
    payment_codename varchar(255),
    rate_id integer,
    raw_text text,
    FOREIGN KEY(payment_codename) REFERENCES payment_method(codename),
    FOREIGN KEY(rate_id) REFERENCES daily_rate(id)
);

insert into daily_rate (rate) values (3.6), (3.1), (3.3), (3.9), (2.8);
insert into payment_method (codename, name, aliases)
values
    ("cash", "наличные", "нал, налик"),
    ("non-cash", "безналичные", "без, безнал, безнальчик"),
    ("paid", "оплачен", "опл, ничего, ниче, оплачено");
