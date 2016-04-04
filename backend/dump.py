import export.apps_script_wrapper as aw
import config
import sqlalchemy
import week

def summarize_order(order_data):
    if 'option' in order_data:
        return order_data['option']
    else:
        choices = []
        for g, cs in order_data['choices'].items():
            if cs:
                s_cs = ', '.join(cs)
                choices.append("{}: {}".format(g, s_cs))
        s_choices = '; '.join(choices)
        meal = order_data['meal']
        return "{} ({})".format(meal, s_choices)

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
    restaurant = order['restaurant']
    s_order = summarize_order(order['order_data'])
    row = [name, day, restaurant, s_order]

    table.append(row)

sname = "Lunch Orders: Week of {}".format(next_week.day(0))
args = [sname, table, config.config['ADMIN']]
aw.call(config.config['SCRIPT_ID'], 'newOrderSheet', args)

