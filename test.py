text = "<div><span></span><span>#</span>"
last_index = text.rindex("</span>")
print("Using rindex:", last_index)

text = "<span class='ansi-red-fg'>TypeError</span>: &#39;&gt;&#39; not supported between instances of &#39;str&#39; and &#39;int&#39;</pre>"

modified_line = '<span>' + text
last_index = text.rindex("</pre>")
print(last_index)
modified_line_final = modified_line[:last_index - 1] + '</span>' + modified_line[last_index + 6:] + '\n'

print(modified_line_final)

import re
line = 'PetalLengthCm    6.9'
pattern = r"^[0-9a-zA-Z].*(?<!</pre>)$"
if re.match(pattern, line):
    print('<br />'+ line)