import re
import argparse
from bs4 import BeautifulSoup
import os

def processor(input_file):
    folder_path = './input/'
    with open(folder_path+input_file, 'r', encoding='utf-8') as file, open('./mid/' + input_file.split('.')[0]+'_mid', 'w', encoding='utf-8') as midOutput:
        soup = BeautifulSoup(file, 'html.parser')
        # remove any <style></style> tag in the html
        for style_tag in soup.body.find_all('style'):
            style_tag.decompose()
        # Find and remove inline style attributes from all tags within the <body> tag
        for tag in soup.body.find_all(True):
            if tag.has_attr('style'):
                del tag['style']

        body_content = soup.body.extract()
        midOutput.write(str(body_content))
        
    with open('./mid/' + input_file.split('.')[0]+'_mid', 'r') as midInput,  open('./output/'+input_file.split('.')[0]+'_output', 'w', encoding='utf-8') as output:
        lines = midInput.readlines()[1:-1]
        # text = ''.join(lines)
        
        for i, line in enumerate(lines):
            if '<span ' in line and not line.lstrip().startswith('<div ') and not line.rstrip().endswith('</pre>') and not line.lstrip().startswith('<p'):
                if line.rstrip().endswith('</span>'):
                    # for lines having pattern: (...)<span>....</span>....<span>...</span>
                    # want it to be <span>(...)<span>....</span>....<span>...</span></span>
                    modified_line = '<span>' + line              
                    last_index = modified_line.rindex('</span>')
                    # modified_line_final = modified_line[:last_index - 1] + '</span>' + modified_line[last_index-1:] + '\n'
                    modified_line_final = modified_line[:last_index] + '</span>' + modified_line[last_index:] + '\n'
                    lines[i] = modified_line_final
                else:
                    # for lines having pattern: (...)<span>....</span>....<span>...</span>..... 
                    # want it to be <span>(...)<span>....</span>....<span>...</span>.....</span>
                    modified_line = '<span>' + line              
                    # last_index = modified_line.rindex('</span>')
                    # modified_line_final = modified_line[:last_index - 1] + '</span>' + modified_line[last_index-1:] + '\n'
                    modified_line_final = modified_line + '</span>' + '\n'
                    lines[i] = modified_line_final

            elif '<span ' in line and not line.lstrip().startswith('<div ') and line.rstrip().endswith('</pre>'):
                # for lines having pattern: <span>....</span>....</pre>              
                modified_line = '<span>' + line               
                last_index = modified_line.rindex('</pre>')
                end_index = line.rfind('>')
                modified_line_final = modified_line[:last_index - 1] + '</span>' + modified_line[last_index:end_index+1] + '\n'     
                # print(modified_line_final)        
                lines[i] = modified_line_final
            elif '<span ' in line and line.lstrip().startswith('<div '):
                # for lines having pattern: <div> ....<span>...</span>....
                index = line.find('<span ')
                modified_line = line[:index] + '<span>' + line[index:]
                last_index = modified_line.rindex('>')
                modified_line_final = modified_line[:last_index + 1] + '</span>' + modified_line[last_index+1:] + '\n'
                # text = text.replace(line, modified_line_final)
                lines[i] = modified_line_final
            # elif line.strip().startswith('<pre>') and not line.rstrip().endswith('</pre>'):
            #     # this together with elif above adds <span> </span> to pattern: 
            #     # '''<pre> SepalLengthCm 0.828
            #     # dtype: float64</pre>
            #     # So we get: <pre><span> SepalLengthCm 0.828
            #     # dtype: float64</span></pre>
            #     if not line.strip()=='<pre>':
            #         # exclude where the line has only <pre> without any contents following that.
            #         # For example: exclude Error Output 
            #         index = line.find('<pre>')
            #         end_index = len(line.rstrip())
            #         # add <span> inside <pre></pre>, e.g the line starts with <pre><span>....</span>, that's why it uses +5 to add <span> after <pre> tag
            #         modified_line = line[:index + 5] + '<span>' + line[index + 5:]
            #         # print(modified_line)
            #         lines[i] = modified_line
            #     else:
            #         lines[i] = line
            # elif line.strip().endswith('</pre>') and not line.rstrip().startswith('<pre>'):
            #     # this together with elif above adds <span> </span> to pattern: 
            #     # '''<pre> SepalLengthCm 0.828
            #     # dtype: float64</pre>
            #     # So we get: <pre><span> SepalLengthCm 0.828
            #     # dtype: float64</span></pre>
            #     if not line.strip()=='</pre>':
            #         # exclude where the line has only </pre> without any contents following that.
            #         # exclude Error Output 
            #         index = line.find('</pre>')
            #         modified_line = line[:index] + '</span>' +line[index:]
            #         lines[i] = modified_line
            #         # pattern = r"^[0-9a-zA-Z].*"
            #         # if re.match(pattern, modified_line):
            #         #     lines[i] = "<br />"+modified_line
            #     else:
            #         lines[i] = line
            elif line.strip().startswith('<pre>') and line.rstrip().endswith('</pre>'):
                # for lines with pattern: <pre>......</pre>
                index = line.find('<pre>')
                last_index = line.rfind('</pre>')
                # find the index of the last > of </pre>
                end_index = line.rfind('>')
                modified_line = line[:index+5] + '<span>' + line[index+5: last_index] + '</span>' + line[last_index:end_index+1]
                lines[i] = modified_line          
            # Add <br />br /> to empty line to add space between two code lines.
            if line.strip()=="":
                lines[i] = line + '<br />'
            if line.strip()=="^":
                lines[i] = '<span>' + line + '</span>'
        
        for i, line in enumerate(lines):
            # Add <br /> to patterns:
            '''
                <br />SepalWidthCm     2.0
                <br />PetalLengthCm    1.0
                <br />PetalWidthCm     0.1
            '''
            pattern = r"^[0-9a-zA-Z#&{[(-].*(?<!</p>)$"
            if re.match(pattern, line.strip()):
                lines[i] = "<br />"+line
            if 'Out[' in line:
                # remove lines with Out[]
                lines[i] = '<div></div>'

 

        text = ''.join(lines)


        # pattern =  r"^[0-9a-zA-Z].*"
        # replacement = r"<br />\0"
        # text = re.sub(pattern, replacement, text)
        # print(text)
        
        # Add <pre> and <code> 
        pattern = r'<pre>(.*?)</pre>'
        replacement = r"<pre className='demo-highlight python'><code className='sourceCode'>\1</code></pre>"
        text = re.sub(pattern, replacement, text, flags=re.DOTALL)
        
        # Replace { and } with '&#123;' and '&#125;'
        text = text.replace('{', '&#123;').replace('}', '&#125;')

        # replace <p>The answer is C.</p> with <AddAnswers answer="C"/> component!
        pattern = r'<p>The answer is ([A-Za-z0-9]+).</p>'
        # Define the replacement string
        replacement = r'<AddAnswers answer="\1" />'
        # Use re.sub() to perform the replacement
        text = re.sub(pattern, replacement, text)

        # remove this Error Output In [8] line
        pattern = r'<span class="ansi-cyan-fg">.*?</span><span class="ansi-green-fg">In \[(\d+)\]</span>'
        text = re.sub(pattern, '', text)

        # Remove empty <span></span>
        pattern = r'<span></span>'
        text = re.sub(pattern, '', text)

        # replace <a> tag with <Link>
        # pattern = r'<a\s+href="([^#].*?)">([^<]+)<\/a>'
        pattern = r'<a\s+href="(?!.*?id="downloadData")(?!#)([^"]*)">(.*?)<\/a>'
        replacement = r'<Link to="\1">\2</Link>'
        text = re.sub(pattern, replacement, text)

        output.write(text)
        

def main():
    parser = argparse.ArgumentParser(description="Process an HTML file.")
    parser.add_argument("--input_folder_path", default='')
    parser.add_argument("--input_file", default='', help="Input HTML file")
    args = parser.parse_args()
    if args.input_file:
        processor(args.input_file)
    else:
        if args.input_folder_path:
            files = os.listdir(args.input_folder_path)
            for filename in files:
                if os.path.isfile(os.path.join(args.input_folder_path, filename)):
                    print(filename)
                    processor(filename)


if __name__ == "__main__":
    main()
    # folder_path = './input'
    # files = os.listdir(folder_path)
    # for filename in files:
    #     if os.path.isfile(os.path.join(folder_path, filename)):
    #         print(filename)
    #         processor(filename)
 
