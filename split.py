import re
splitLen = 20000
outputBase = 'proza'

input = open('./proza.csv', 'r', encoding='utf-8')
re_for_russian_letters = re.compile(
    r'[^.,:?!1234567890АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя\-\(\) ]',
    re.U
)
count = 0
at = 0
dest = None
for line in input:
    tex = re.sub(re_for_russian_letters, '', line)
    if count % splitLen == 0:
        if dest: dest.close()
        dest = open(outputBase + str(at) + '.csv', 'w')
        at += 1
    dest.write(tex)
    count += 1
