text = """
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">var_1</span> <span class="o">=</span> <span class="s1">&#39;My user ID is: &#39;</span>
<span class="n">ID</span> <span class="o">=</span> <span class="mi">23412</span>

<span class="nb">print</span><span class="p">(</span><span class="n">var_1</span> <span class="o">+</span> <span class="nb">str</span><span class="p">(</span><span class="n">ID</span><span class="p">))</span>
</pre></div>
"""

# last_index = text.rindex("</span>") 
# print("Using rindex:", last_index)
# print(text[:last_index])


# modified_line = '<span>' + text              
# last_index = modified_line.rindex('</span>')
# print(last_index)
# # modified_line_final = modified_line[:last_index] + '</span>' + modified_line[last_index:] + '\n'
# modified_line_final = modified_line + '</span>' + '\n'
# print(modified_line_final)

import re
# line = 'PetalLengthCm    6.9'
# pattern = r"^[0-9a-zA-Z].*(?<!</pre>)$"
# if re.match(pattern, line):
#     print('<br />'+ line)

pattern = r'<pre>(.*?)</pre>'
replacement = r"<pre className='demo-highlight python'><code className='sourceCode'>\1</code></pre>"
text = re.sub(pattern, replacement, text, flags=re.DOTALL)
print(text)