from measurement.measures import Weight, Volume


def zero_weight():
    return Weight(kg=0)


def zero_volume():
    return Volume(Litre=0)


def convert_weight(weight: Weight, unit: str) -> Weight:
    converted_weight = getattr(weight, unit)
    weight = Weight(**{unit: converted_weight})
    weight.value = round(weight.value, 3)
    return weight


def convert_volume(volume: Volume, unit: str) -> Volume:
    converted_volume = getattr(volume, unit)
    volume = Volume(**{unit: converted_volume})
    volume.value = round(volume.value, 3)
    return volume

