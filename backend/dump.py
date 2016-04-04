import export.apps_script_wrapper as aw
import config
import sqlalchemy
import week

next_week = week.Week.from_offset(1)
days = next_week.days()
eng = sqlalchemy.create_engine(config.config['SQLALCHEMY_DATABASE_URI'])

query = 'SELECT * FROM orders LEFT JOIN students USING (studentid)'\
    ' WHERE day = ANY (%(days)s);'
orders = eng.execute(query, days=days).fetchall()

table = []
for order in orders:
    name = order['firstname'] + ' ' + order['lastname']
    day = str(order['day'])
    price = order['price']
    restaurant = order['restaurant']
    row = [name, day, price, restaurant]

    data = order['order_data']
    if 'option' in data:
        row.append(data['option'])
    else:
        row.append(data['meal'])
        choices = []
        for g, cs in data['choices'].items():
            if cs:
                choices.append("{}: {}".format(g, ', '.join(cs)))
        row.append('; '.join(choices))

    table.append(row)

sname = "Lunch Orders: Week of {}".format(next_week.day(0))
args = [sname, table, config.config['ADMIN']]
aw.call(config.config['SCRIPT_ID'], 'newOrderSheet', args)

