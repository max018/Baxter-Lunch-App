CREATE TABLE orders (
    orderid         serial PRIMARY KEY,
    studentid       integer REFERENCES students,
    day             date,
    price           money,
    restaurant      citext,
    order_data      jsonb,
    UNIQUE          (studentid, day)
);

CREATE TABLE days (
    dayid           serial PRIMARY KEY,
    day             date,
    holiday         text,
    UNIQUE          (day)
);

