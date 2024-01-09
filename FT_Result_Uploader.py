import os
import shutil
import configparser
import csv
import schedule
import time
import logging
import sys
import ctypes

# Version info
''' 
### Change Note ###
- Version: 1.0
- Initial release

'''

# Set up logging
log_file_path = 'log.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')


# Function to read information from config file
def read_config(config_dir):
    config = configparser.ConfigParser(inline_comment_prefixes=('#', '%')) # Ignore any comments from the config file
    config.read(config_dir)

    if "General" in config:
        data_dir = config["General"].get("data_dir")
        pc_name = config["General"].get("pc_name")
        rig_name = config["General"].get("rig_name")
        db_dir = config["General"].get("db_dir")
        frequency = config["General"].get("frequency")
        
        return data_dir, pc_name, rig_name, db_dir, frequency
    else:
        print("Error: Invalid information in Config file.")
        log_entry = f"Error: Invalid information in Config file."
        logging.info(log_entry)
        return None

# Function to read csv files
def read_csv_files(data_dir, db_dir, rig_name):
    sn_list = [] # List to store serial numbers
    timestamp_list = [] # List to store timestamp
    file_count = 0
    print('Reading csv files in progress...')
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.startswith("Summary_") and file.endswith(".csv"):
                file_path = os.path.join(root, file)
                
                # Extract the serial number from the file path
                sn, timestamp = extract_serial_number(file_path)
                if sn:
                    sn_list.append(sn)
                    timestamp_list.append(timestamp)
                    file_count += 1
                    process_csv_file(file_path, db_dir, rig_name, sn, file_count)
                
# Function to process csv files
def process_csv_file(file_path, db_dir, rig_name, sn, file_count):
    # Create a new file name by appending [SN] to the original file name
    base_name = os.path.basename(file_path)
    new_name = f"{sn}_{rig_name}_{base_name}"

   # Check if the file already exists in the destination directory
    destination_path = os.path.join(db_dir, new_name)
    
    if not os.path.exists(destination_path):
        # Copy the CSV file to the specified database directory with the new name
        shutil.copy(file_path, destination_path)
        print(f"File copied to {destination_path}")
        log_entry = f"SN added: {sn}"
        logging.info(log_entry)
    else:
        print(f"Checking file #{file_count}")

def extract_serial_number(file_path):
    # Split the file path using backslashes
    path_parts = file_path.split(os.path.sep)

    # Find the index of the last element in the list
    last_index = len(path_parts) - 1

    # Extract the serial number from the second-to-last element
    if last_index > 0:
        sn = path_parts[last_index - 2]
        time_stamp = path_parts[last_index - 1]
        return sn, time_stamp
    else:
        return None

def main():
    # Set default directory
    config_dir = 'C:/Finisar/Process Engineering/config.ini'
    # Read configuration from the file
    config_data = read_config(config_dir)

    if config_data:
        data_dir, pc_name, rig_name, db_dir, frequency = config_data

        # Use the configuration values in your script
        print("Data Directory:", data_dir)
        print("PC Name:", pc_name)
        print("Rig Name:", rig_name)
        print("FT DB Directory:", db_dir)
        print("Frequency of Reading (in hrs):", frequency)
        
        read_csv_files(data_dir, db_dir, rig_name)
        
        # Schedule a future job to read and process CSV files based on the frequency in the config file (eg. every 24 hours)
        schedule.every(int(frequency)).hours.do(lambda: read_csv_files(data_dir, db_dir, rig_name))
    
        # Run the scheduled jobs
        while True:
            schedule.run_pending()



if __name__ == "__main__":
    version = 1.0
    print(f"Executable Version: {version}")
    log_entry = f"Executable Version: {version}"
    logging.info(log_entry)
    main()
    