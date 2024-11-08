import os
import shutil

def model_data_versioning(version, ratings_folder, model_folder):
    """Create copies of data and model files with
        the version numbers. This can be uploaded
        to a remote storage using dvc. But, we are
        storing it locally for now."""
    
    shutil.copy(os.path.join(ratings_folder, "cleaned_rating.csv"), \
    os.path.join(ratings_folder,"versioning", f"cleaned_rating_{version}.csv"))

    # For now using model.pkl.dvc
    # because we do not have big enough storage to keep hundred copies of 2GB
    # models either locally or on remote. Assuming our system runs for multiple days.

    shutil.copy(os.path.join(model_folder, "model.pkl.dvc"), \
    os.path.join(model_folder,"versioning", f"model_{version}.pkl.dvc"))



# model_data_versioning(3,"/home/team-4/team-4/app/data", "/home/team-4/team-4/app/model")


    