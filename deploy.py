import os
from datetime import datetime
from shutil import copyfile

dirs = [
    "wine-spider-combine-breed-area_breed_0",
    "wine-spider-combine-breed-area_breed_100",
    "wine-spider-combine-breed-area_breed_200",
    "wine-spider-combine-breed-area_breed_300",
    "wine-spider-combine-breed-area_breed_400",
    "wine-spider-combine-breed-area_breed_500",
    "wine-spider-combine-breed-area_breed_600",
]

file_name = "vivino_zh.py"


def deploy(root_dir):
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
        print(datetime.now(), f"Directory '{root_dir}' created successfully.")
    file_path = os.path.join(root_dir, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        copyfile(file_name, file_path)
        print(datetime.now(), f"{root_dir} copy done")
    else:
        copyfile(file_name, file_path)
        print(datetime.now(), f"{root_dir} copy done")

    os.system(f"setsid python3 {file_path} &>> {root_dir}/out.log$(date \"+%d_%H%M\") 2>&1 & ")


def main():
    if not os.path.exists(file_name):
        print(datetime.now(), f"error : find nothing {file_name}")
        return
    os.system(f"kill -9 $(pgrep -f '{file_name}')")
    for root_dir in dirs:
        deploy(root_dir)

    # os.remove(file_name)
    # os.system(f"touch {file_name}")
    print(datetime.now(), "deploy done")
    os.system(f"ps aux|grep {file_name}")


main()
