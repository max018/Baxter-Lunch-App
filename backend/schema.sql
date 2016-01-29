CREATE TABLE users (
    userid          serial PRIMARY KEY,
    username        citext,
    firstname       text,
    lastname        text,
    UNIQUE          username
);

CREATE TABLE orders (
    orderid         serial PRIMARY KEY,
    username        citext,
    day             date,
    price           money,
    restaurant      citext,
    order           jsonb,
    UNIQUE          (username, day)
);

CREATE TABLE days (
    dayid           serial PRIMARY KEY,
    day             date,
    holiday         text,
    UNIQUE          day
);

