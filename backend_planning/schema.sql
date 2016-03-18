CREATE TABLE students (
    studentid serial PRIMARY KEY,
    firstname citext,
    lastname citext,
    email citext,
    UNIQUE (email)
);

CREATE TABLE days (
    dayid           serial PRIMARY KEY,
    day             date,
    holiday         text,
    UNIQUE          (day)
);

CREATE TABLE orders (
    orderid         serial PRIMARY KEY,
    studentid       integer REFERENCES students,
    day             date,
    price           money,
    restaurant      citext,
    order_data      jsonb,
    UNIQUE          (studentid, day)
);

