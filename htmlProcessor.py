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
        text = ''.join(lines)
        
        for i, line in enumerate(lines):
            if '<span ' in line and not line.lstrip().startswith('<div '):
                modified_line = '<span>' + line
                last_index = modified_line.rindex('>')
                modified_line_final = modified_line[:last_index + 1] + '</span>' + modified_line[last_index + 8:] + '\n'
                # modified_line_final = modified_line[:last_index] + '</span>'+ modified_line[last_index:] + '\n'
                # text = text.replace(line, modified_line_final)
                lines[i] = modified_line_final
            elif '<span ' in line and line.lstrip().startswith('<div '):
                index = line.find('<span ')
                modified_line = line[:index] + '<span>' + line[index:]
                last_index = modified_line.rindex('>')
                modified_line_final = modified_line[:last_index + 1] + '</span>' + modified_line[last_index + 8:] + '\n'
                # text = text.replace(line, modified_line_final)
                lines[i] = modified_line_final
            elif line.strip().startswith('<pre>'):
                index = line.find('<pre>')
                # #  new
                # ending_index = line.find('</pre>')
                # add <span> inside <pre></pre>, e.g the line starts with <pre><span>....</span>, that's why it uses +5 to add <span> after <pre> tag
                modified_line = line[:index + 5] + '<span>' + line[index + 5:] + '</span>'
                # #  new
                # if not ending_index:
                #     modified_line = line[:index + 5] + '<span>' + line[index + 5:] + '</span>'
                # else:
                #     modified_line = line[:index + 5] + '<span>' + line[index + 5:ending_index] + '</span>' + line[ending_index:]
                # text = text.replace(line, modified_line)
                lines[i] = modified_line
   
            # Add <br /> to Spark DataFrame output
            if line.strip().startswith('<pre>+') or line.strip().startswith('+') or line.strip().startswith('|'):
                line_after = line[:] + '<br />'
                text = text.replace(line, line_after)
                lines[i] = line + '<br />'
                if lines[i+1].strip()=="":
                    lines[i+1] = '<span></span>'
            # Add <br />br /> to empty line to add space between two code lines.
            if line.strip()=="":
                lines[i] = line + '<br />'
            
        text = ''.join(lines)
        # Remove empty <span></span>
        pattern = r'<span></span>'
        text = re.sub(pattern, '', text)
        
        # Add <pre> and <code> 
        pattern = r'<pre>(.*?)</pre>'
        replacement = r"<pre className='demo-highlight python'><code className='sourceCode'>\1</code></pre>"
        text = re.sub(pattern, replacement, text, flags=re.DOTALL)
        
        # Replace { and } with '&#123;' and '&#125;'
        text = text.replace('{', '&#123;').replace('}', '&#125;')
        
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
 
