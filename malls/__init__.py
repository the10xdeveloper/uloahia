default_app_config = "malls.apps.MallsConfig"


class MallTypeKind:
    SUPERMARKET = "Supermarket"
    RESTAURANT = "Restaurant"
    PHARMACY = "Pharmacy"
    OTHERS = "Others"

    CHOICES = [
        (SUPERMARKET, "Supermarket"),
        (RESTAURANT, "Restaurant"),
        (PHARMACY, "Pharmacy"),
        (OTHERS, "Others")
    ]
