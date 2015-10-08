import PIL.Image
import aalib
import re
import sys

def multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(replacement_function, string)

def multiple_replace(string, *key_values):
    return multiple_replacer(*key_values)(string)

screen = aalib.AsciiScreen(width=20, height=20)
image = PIL.Image.open(sys.argv[1]).convert('L').resize(screen.virtual_size)

#image = image.point(lambda x: x if x != (255, 255, 255, 255) else (255, 255, 255, 0))
#image = image.convert('L')
#.convert('L').resize(screen.virtual_size)
screen.put_image((0, 0), image)
rendered = screen.render()

chars = len(rendered)

used = {}

for i in xrange(0, chars):
	if rendered[i] != " ":
		if rendered[i] not in used:
			used[rendered[i]] = 0
		else:
			used[rendered[i]] += 1

used_by_count = sorted(used.items(), key=lambda x: x[1], reverse=True)

if used_by_count[0][1] > rendered.count(" "):
	rendered = rendered.replace(used_by_count[0][0], " ")
	used_by_count = used_by_count[1:]

replace_map = []

row_number = 0
for row in used_by_count:
	if row_number == 0:
		replace_map.append((row[0], ':parrot:'))
	elif row_number == 1:
		replace_map.append((row[0], ':middleparrot:'))
	elif row_number == 2:
		replace_map.append((row[0], ':rightparrot:'))
	elif row_number % 2 == 0:
		replace_map.append((row[0], ':shuffleparrot:'))
	else:
		replace_map.append((row[0], ':oldtimeyparrot:'))
	row_number += 1

parrot_rendered = "\n".join(map(lambda x: multiple_replace(x, *replace_map), rendered.split("\n")))
print parrot_rendered.replace(" ", "      ")
