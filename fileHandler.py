import pickle


def file_load(file):
    try:
        with open(file, 'rb') as handle:
            poses = pickle.load(handle)
        return poses
    except Exception as e:
        print(f"Error Loading File {file}")
        print(e)