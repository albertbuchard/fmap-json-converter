"""
    Converts the json files in the fmap directory of a session folder
    by adding a new field IntendedFor which is a list of all the nii.gz
    files in the func directory.
"""
import json
import os


def reformat_files(folder, output_folder=None):
    """
    Reformat the json files in the subject folder

    The structure of the folder should be:
    - sub-x : subject_folder x
    - sub-x/ses-y : session_folder y
    - sub-x/ses-y/fmap : fmap_folder with the json files
    - sub-x/ses-y/func : func_folder with the nii.gz files


    :param folder: the folder where the sub-x folders are
    :param output_folder: the folder where the new json files will be saved, if None, the new files will be saved in the
    same folder as the original files, overwriting the original files

    :return: None
    """
    for subject_folder in os.listdir(folder):
        if not subject_folder.startswith('sub-'):
            continue
        subject_folder_path = os.path.join(folder, subject_folder)
        for session_folder in os.listdir(subject_folder_path):
            if not session_folder.startswith('ses-'):
                continue
            session_folder_path = os.path.join(subject_folder_path, session_folder)

            # get the json files
            fmap_folder_path = os.path.join(session_folder_path, 'fmap')
            json_files = [os.path.join(fmap_folder_path, f) for f in os.listdir(fmap_folder_path) if f.endswith('.json')]

            # get the nii.gz files
            func_folder_path = os.path.join(session_folder_path, 'func')
            nii_files = [os.path.join(func_folder_path, f) for f in os.listdir(func_folder_path) if f.endswith('.nii.gz')]

            # reformat the json files
            for json_file in json_files:
                with open(json_file, 'r') as f:
                    # Parse the json file
                    data = json.load(f)

                # Add the IntendedFor field
                data['IntendedFor'] = nii_files
                # If the output folder is not None, save the new json file in the output folder
                if output_folder is not None:
                    # Create the output folder if it does not exist
                    # Keeping the subject and session folders structure
                    output_folder_path = os.path.join(output_folder, subject_folder, session_folder)
                    if not os.path.exists(output_folder_path):
                        os.makedirs(output_folder_path)
                    output_path = os.path.join(output_folder_path, os.path.basename(json_file))
                else:
                    output_path = json_file

                # Save the new json file
                with open(output_path, 'w') as f:
                    json.dump(data, f, indent=4)




if __name__ == '__main__':
    # Read the arguments: folder where the json and nii.gz files are located, overwrite the json files or output folder
    import argparse
    parser = argparse.ArgumentParser(description='Convert a json files in a fmap folder of a session to DVS-lab format.')
    parser.add_argument('-d', '--directory', type=str, help='Folder where the subject folders located.')
    # output folder, if default, overwrite the json files
    parser.add_argument('-o', '--output', type=str, default=None, help='Output folder where the json files will be saved.')
    args = parser.parse_args()
    # Reformat the json files
    reformat_files(args.directory, args.output)
    print('Done!')


