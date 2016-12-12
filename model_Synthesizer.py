#!/usr/bin/python

import re

model_class = 'db.Model'
file_name = 'db/db.sql'
code = 'from flask_sqlalchemy import SQLAlchemy\n\
\n\
db = SQLAlchemy()\n\
\n\n'
ddl = ''


def compose_table_class(columns):
    res = ''
    for line in columns:
        codeline = ''
        if re.match('^PRIMARY KEY\(', line, re.IGNORECASE):
            # Not to process multi primary key first
            continue
        fields = line.split(' ')
        name = fields[0]
        datatype = fields[1]
        attr = None
        if len(fields) >= 3:
            attr = ' '.join(fields[2:])
        name = re.match('^`?(\w*)`?$', name).group(1)
        codeline += '    %s = db.Column(\'%s\', ' % (name, name)
        if re.match('^INT', datatype, re.IGNORECASE):
            codeline += 'db.Integer'
        elif re.match('^FLOAT', datatype, re.IGNORECASE):
            codeline += 'db.Float'
        elif re.match('^TEXT', datatype, re.IGNORECASE):
            codeline += 'db.Text'

        r = re.match('^VARCHAR\((\d*)\)', datatype, re.IGNORECASE)
        if r:
            codeline += 'db.String(%s)' % r.group(1)

        if attr:
            if re.search('NOT NULL', attr, re.IGNORECASE):
                codeline += ', nullable=False'
            if re.search('PRIMARY KEY', attr, re.IGNORECASE):
                codeline += ', primary_key=True'
            if re.search('AUTO_INCREMENT', attr, re.IGNORECASE):
                codeline += ', autoincrement=True'
            s = re.search('DEFAULT (\w*),?', attr, re.IGNORECASE)
            if s:
                codeline += ', default=%s' % s.group(1)
        codeline += ')\n'
        res += codeline
    return res

with open(file_name, 'r') as f:
    ddl = f.read()

columns = list()
is_inside_create_table = False

for l in ddl.splitlines():
    # Trim
    line = l.strip()

    # Push table ddl
    if re.match(r'^\);', l): # End of CREATE_TABLE
        is_inside_create_table = False
        code += compose_table_class(columns)
        del columns[:]
        code += '\n\n'
        continue

    if is_inside_create_table:
        columns.append(l)
        continue

    # Skip comments and empty lines
    if line == '' or re.match('^--', line):
        continue
    r = re.match('^CREATE TABLE (\w*)\s?\(?', line, re.IGNORECASE)
    if r:
        is_inside_create_table = True
        name = r.group(1)
        class_name = name[0].upper() + name[1:]
        code += 'class %s(%s):\n' % (class_name, model_class)
        code += '    __tablename__ = \'%s\'\n' % name
        continue

print code

