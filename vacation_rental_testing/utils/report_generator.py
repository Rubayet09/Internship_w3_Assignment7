# import pandas as pd
# import os

# def save_test_result(test_results, sheet_name):
#     file_path = "reports/test_results.xlsx"
#     # print(test_results)  # This should print a list of dictionaries

#     # Ensure test_results is a list of dictionaries
#     if isinstance(test_results, dict):
#         test_results = [test_results]

#     # Create a DataFrame from the list of test results
#     data = pd.DataFrame(test_results)

#     # Check if the file exists
#     if os.path.exists(file_path):
#         # If the file exists, we will append data to the existing sheet
#         with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
#             # Check if the sheet exists, if not write the header
#             sheet = writer.sheets.get(sheet_name)
#             if sheet is None:
#                 # If the sheet doesn't exist, write the header
#                 data.to_excel(writer, index=False, sheet_name=sheet_name, header=True)
#             else:
#                 # If the sheet exists, append without the header
#                 data.to_excel(writer, index=False, sheet_name=sheet_name, header=False)
#     else:
#         # If the file doesn't exist, create a new Excel file with the results
#         with pd.ExcelWriter(file_path, mode='w', engine='openpyxl') as writer:
#             # Write the data with header for the first time
#             data.to_excel(writer, index=False, sheet_name=sheet_name, header=True)

import pandas as pd
import os

def save_test_result(test_results, sheet_name):
    file_path = "reports/test_results.xlsx"
    
    # Ensure test_results is a list of dictionaries
    if isinstance(test_results, dict):
        test_results = [test_results]

    # Create a DataFrame from the list of test results
    data = pd.DataFrame(test_results)

    # Print for debugging
    print(f"Saving test results to: {file_path}")
    print(f"Test results to save: {data.head()}")

    # Check if the file exists
    if os.path.exists(file_path):
        print(f"File exists. Appending data to sheet: {sheet_name}")
        # If the file exists, we will append data to the existing sheet
        with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            # Check if the sheet exists
            try:
                sheet = writer.sheets[sheet_name]  # This will throw an error if the sheet doesn't exist
                # If the sheet exists, append without the header
                data.to_excel(writer, index=False, sheet_name=sheet_name, header=False, startrow=len(sheet['A'])+1)
                print(f"Data appended to existing sheet {sheet_name}")
            except KeyError:
                # If the sheet doesn't exist, write the header
                data.to_excel(writer, index=False, sheet_name=sheet_name, header=True)
                print(f"Sheet '{sheet_name}' does not exist. Created and added data.")
    else:
        print(f"File does not exist. Creating new file: {file_path}")
        # If the file doesn't exist, create a new Excel file with the results
        with pd.ExcelWriter(file_path, mode='w', engine='openpyxl') as writer:
            # Write the data with header for the first time
            data.to_excel(writer, index=False, sheet_name=sheet_name, header=True)
            print(f"Created new file and added data to sheet '{sheet_name}'")


