1. Put all original html file in <input folder>  
2. In terminal run: python3 htmlProcessor_python.py --input_folder_path './input'  
    a. this will process all html files under the input folder and save processed files to the output folder.  
    b. To process a single file in the input folder, use htmlProcessor.py --input_fiel <file_name(no path needed as long as it's in the input folder)>. The file should be in the input folder too.
3. In terminal run: python3 reactProcessor_python.py --input_folder_path './output'  
    a. this will take files from the output folder and create new react.js files in the outputReact folder.  
    b. To process a single file in the input folder, use reactProcessor.py --input_fiel <file_name(no path needed as long as it's in the output folder)>. The file should be in the output folder too.



htmlProcessor_python.py is for python scripts


For PySpark: 
python3 htmlProcessor_pyspark.py --input_folder_path './input'  
python3 reactProcessor_pyspark.py --input_folder_path './output' 