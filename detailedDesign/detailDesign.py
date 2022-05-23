from detailedDesign.classes.Aircraft import Aircraft


def detailDesign():
    aircraft = Aircraft()
    print("Bye World!")

    print(aircraft.WingGroup.Engines.count)


if __name__ == "__main__":
    detailDesign()
