"""
Convert the json files by adding a new field IntendedFor which is a list of all the nii.gz files
that are in the same directory as the json file.
"""
import json
import os


def reformat_files(folder, output_folder=None):
    """
    Reformat the json files in the folder
    :param folder: the folder where the json files are
    :param output_folder: the folder where the new json files will be saved, if None, the new files will be saved in the
    same folder as the original files, overwriting the original files

    :return: None
    """
    # Get all the json files
    json_files = [f for f in os.listdir(folder) if f.endswith('.json')]
    # Get all the nii.gz files
    nii_files = [f for f in os.listdir(folder) if f.endswith('.nii.gz')]
    # Loop through the json files
    for json_file in json_files:
        # Get the path to the json file
        json_path = os.path.join(folder, json_file)
        # Open the json file
        with open(json_path, 'r') as f:
            # Parse the json file
            data = json.load(f)
            # Add the IntendedFor field
            data['IntendedFor'] = [os.path.join(folder, nii_file) for nii_file in nii_files]
            # If the output folder is not None, save the new json file in the output folder
            if output_folder is not None:
                # Create the output folder if it does not exist
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                output_path = os.path.join(output_folder, json_file)
            else:
                output_path = json_path
            # Save the new json file
            with open(output_path, 'w') as f:
                json.dump(data, f)


if __name__ == '__main__':
    # Read the arguments: folder where the json and nii.gz files are located, overwrite the json files or output folder
    import argparse
    parser = argparse.ArgumentParser(description='Convert a folder of json and nii.gz files to DVS-lab format.')
    parser.add_argument('-d', '--directory', type=str, help='Folder where the json and nii.gz files are located.')
    # output folder, if default, overwrite the json files
    parser.add_argument('-o', '--output', type=str, default=None, help='Output folder where the json files will be saved.')
    args = parser.parse_args()
    # Reformat the json files
    reformat_files(args.directory, args.output)



