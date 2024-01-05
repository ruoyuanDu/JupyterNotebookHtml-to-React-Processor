import os
import json
import argparse

def reactProcessor(input):
    inputName = str(input)
    folder_path = './output/'
    with open(folder_path+input, 'r') as input:
        beginning = [
            "import React from 'react'; \n",
            "import useCustomEffect from '../../../useCustomEffect'; \n",
            # capitalize the first letter of the filename for the function component
            "export default function " +"Python"+inputName.split('_')[1].capitalize()+"(){\n", 
            "useCustomEffect()\n",
            "return ( <div>\n"  
        ]
        htmlLines = input.readlines()
        ending = [
            "</div>\n)}"
        ]
        lines = beginning + htmlLines+ending
        text = ''.join(lines)
    with open('./outputReact/'+inputName+'_react.js', 'w') as output:
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
                    dataList.append(
                        {'component': "<Python"+filename.split('_')[1].capitalize()+" />", 'path':'', 'title':filename.split('_')[0]}
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