
from packages.dnf import Dnf


if __name__ == "__main__":
    dnf = Dnf(
        scaling=1,
        fps=10,
        dev_model=True,
        # model="runs/jianmo1/weights/best.pt"
        model="runs/jianmo3/weights/last.pt"

    )
    dnf.start()
