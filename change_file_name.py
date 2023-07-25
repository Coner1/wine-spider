import os


def main():
    for i, file in enumerate(os.listdir("output")):
        os.rename(os.path.join("output", file), os.path.join("output", str(i)))


main()
