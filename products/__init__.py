default_app_config = "products.apps.ProductsConfig"


class ProductMediaTypes:
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"

    CHOICES = [
        (IMAGE, "An uploaded image or an URL to an image"),
        (VIDEO, "A URL to an external video"),
    ]


class ProductTypeKind:
    NORMAL = "normal"
    GIFT_CARD = "gift_card"
    FOOD = "food"
    DRUG = "drug"
    GROCERY = "grocery"
    OTHERS = "others"

    CHOICES = [
        (NORMAL, "A standard product type."),
        (GIFT_CARD, "A gift card product type."),
        (FOOD, "A food product type"),
        (DRUG, "A drug product type"),
        (GROCERY, "A grocery product type"),
        (OTHERS, "Other product types"),
    ]
