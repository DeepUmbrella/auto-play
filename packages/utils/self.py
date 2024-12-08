from torch import cuda, version


if __name__ == "__main__":

    print(version.cuda)
    print(cuda.is_available())
    print(cuda.device_count())
