a = [['bla', 'blub', 'bloeb']]
a.append(['da', 'die', 'dumm'])
print a
for row in a:
    _row = ''
    for item in row:
        _row += item
    print row