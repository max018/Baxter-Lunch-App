CREATE TABLE orders (
    orderid         serial PRIMARY KEY,
    userid          integer,
    day             date,
    price           money,
    restaurant      citext,
    order           jsonb,
    UNIQUE          (userid, day)
);

CREATE TABLE days (
    dayid           serial PRIMARY KEY,
    day             date,
    holiday         text,
    UNIQUE          day
);

