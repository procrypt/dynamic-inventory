#!/usr/bin/env python
from jinja2 import Template
from itertools import izip


with open('variable.txt') as variable:
    content = variable.readlines()
content = [x.strip() for x in content]

variables = {}
for i in content:
    data = i.split("=")
    data[1] = data[1].strip('"')
    variables.update({data[0]: data[1]})

with open('OSE.yml') as file_:
    template = Template(file_.read())
    data = template.render(variables)

with open("data.yml", "wb") as fh:
    fh.write(data)


