import os
import json
import argparse
import re

def reactProcessor(input):
    inputName = str(input)
    folder_path = './output/'
    with open(folder_path+input, 'r') as input:  
        # text = input.read()
        htmlLines = input.readlines()
        text = ''.join(htmlLines)
        pattern = r'<AddAnswers answer="([A-Za-z0-9]+)" />'
        matches = re.findall(pattern, text, flags=re.DOTALL)
        if matches:
            beginning = [

                "import React from 'react'; \n",
                "import {Link} from 'react-router-dom'; \n",
                "import useCustomEffect from '../../../useCustomEffect'; \n",

                "import AddAnswers from '../../../js/addAnswerReveal'; \n\n",
                # capitalize the first letter of the filename for the function component
                "export default function " +"Python"+inputName.split('_')[0].capitalize()+"(){\n", 
                "useCustomEffect()\n\n",
                "return ( <div>\n"  
            ]
        else:
            beginning = [
                "import React from 'react'; \n",
                "import {Link} from 'react-router-dom'; \n",
                "import useCustomEffect from '../../../useCustomEffect'; \n",
                # capitalize the first letter of the filename for the function component
                "export default function " +"Python"+inputName.split('_')[0].capitalize()+"(){\n", 
                "useCustomEffect()\n",
                "return ( <div>\n"  
            ]
            
        # htmlLines = input.readlines()
        ending = [
            "</div>\n)}"
        ]
        
        html_lines = ''.join(htmlLines)
        #change all classname to class
        # add = to exclude replacing classname and class ouside tags
        final_lines = html_lines.replace('classname=', 'class=')
        final_lines = final_lines.replace('class=', 'className=')

        lines = beginning + [final_lines] + ending

        text = ''.join(lines)

    with open('./outputReact/'+"Python"+inputName+'_react.js', 'w') as output:
        output.write(text)
        
def main():
    parser = argparse.ArgumentParser(description="Process an HTML file.")
    parser.add_argument("--input_folder_path", default='')
    parser.add_argument("--input_file", default='',required=False, help="Input HTML file")
    args = parser.parse_args()
    # for single file
    if args.input_file:
        reactProcessor(args.input_file)
    # for folders
    else:
        if args.input_folder_path:
            dataList = []
            files = os.listdir(args.input_folder_path)
            for filename in files:
                if os.path.isfile(os.path.join(args.input_folder_path, filename)):
                    print(filename)
                    reactProcessor(filename)
                    # get titles right before appending to dataList
                    words = []
                    main_title = filename.split('_')[0]
                    start = 0
                    for i in range(1, len(main_title)):
                        if main_title[i].isupper():
                            words.append(main_title[start:i])
                            start = i
                    words.append(main_title[start:])
                    title_correct = ' '.join(words)
                    # get correct path
                    print(words)
                    main_path = '-'.join(words).lower()
                    path_correct = 'python-' + main_path

                    dataList.append(
                        {'component': "<Python"+filename.split('_')[0].capitalize()+" />", 'path':path_correct, 'title':title_correct}
                    )
            # json_data = json.dumps(dataList, indent=2)
            file_path = "data.js"

            with open(file_path, 'w') as json_file:
                json_file.write('const data=[')
                for item in dataList:
                    json_file.write(str(item)+',' + '\n')
                json_file.write(']')


if __name__ == "__main__":
    # folder_path = './output'
    # dataList = []
    # files = os.listdir(folder_path)
    # for filename in files:
    #     if os.path.isfile(os.path.join(folder_path, filename)):
    #         print(filename)
    #         reactProcessor(filename)
    #         dataList.append(
    #             {'component': "<Spark"+filename.split('_')[0].capitalize()+" />", 'path':'', 'title':filename.split('_')[0]}
    #         )
    # json_data = json.dumps(dataList, indent=2)
    # file_path = "data.js"
    

    # with open(file_path, 'w') as json_file:
    #     json_file.write('const data=[')
    #     for item in dataList:
    #         json_file.write(str(item)+',' + '\n')
    #     json_file.write(']')
    main()