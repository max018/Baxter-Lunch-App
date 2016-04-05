import export.apps_script_wrapper as aw
import config
import sqlalchemy
import week

WEEKDAYS = 'Monday Tuesday Wednesday Thursday Friday'.split()
def header_for(week):
    header = ['Name']
    for name, date in zip(WEEKDAYS, week.days()):
        col_heading = "{} ({})".format(name, date)
        header.append(col_heading)
    return header

def summarize_order(order_data):
    if 'option' in order_data:
        pick = order_data['option']
    else:
        choices = []
        for g, cs in order_data['choices'].items():
            if cs:
                s_cs = ', '.join(cs)
                choices.append("{}: {}".format(g, s_cs))
        s_choices = '; '.join(choices)
        meal = order_data['meal']
        pick = "{} ({})".format(meal, s_choices)

    restaurant = order_data['restaurant']
    return "{}: {}".format(restaurant, pick)


next_week = week.Week.from_offset(1)
eng = sqlalchemy.create_engine(config.config['SQLALCHEMY_DATABASE_URI'])

# this is probably awful
query =\
    'SELECT firstname, lastname, '\
        'json_object_agg(day, order_data) AS week_map'\
    ' FROM orders LEFT JOIN students USING (studentid)'\
    ' WHERE day = ANY (%(days)s)'\
    ' GROUP BY (firstname, lastname);'
days = next_week.days()
students = eng.execute(query, days=days).fetchall()

table = [header_for(next_week)]
for student in students:
    week_map = student['week_map']
    if not week_map:
        continue

    name = student['firstname'] + ' ' + student['lastname']
    row = [name]

    for day in map(str, days):
        if day not in week_map:
            row.append(None)
        else:
            order_data = week_map[day]
            s_order = summarize_order(order_data)
            row.append(s_order)

    table.append(row)

sname = "Lunch Orders: Week of {}".format(next_week.day(0))
args = [sname, table, config.config['ADMIN']]
aw.call(config.config['SCRIPT_ID'], 'newOrderSheet', args)

