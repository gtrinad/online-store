from django.db import models


def category_image_directory_path(instance: "CategoryIcon", filename: str) -> str:
    if instance.category.parent:
        return "icons/category/{parent}/{category}/{filename}".format(
            parent=instance.category.parent,
            category=instance.category,
            filename=filename,
        )
    else:
        return "icons/category/{category}/{filename}".format(
            category=instance.category,
            filename=filename,
        )


def product_image_directory_path(instance: "ProductImage", filename: str) -> str:
    return "images/product_{id}/{filename}".format(
        id=instance.product.pk,
        filename=filename,
    )


class Category(models.Model):
    """Represents a category in the system."""

    title = models.CharField(max_length=128, unique=True, db_index=True)
    is_active = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="subcategories",
        db_index=True,
    )
    favourite = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["pk"]

    def __str__(self):
        return "{title}".format(title=self.title)


class CategoryIcon(models.Model):
    src = models.ImageField(
        upload_to=category_image_directory_path, verbose_name="Category link"
    )
    alt = models.CharField(
        max_length=128,
        verbose_name="Category icon description",
        default="Category icon description",
    )
    category = models.OneToOneField(
        Category, null=True, blank=True, on_delete=models.CASCADE, related_name="image"
    )

    class Meta:
        verbose_name = "Category icon"
        verbose_name_plural = "Category icons"
        ordering = ["pk"]

    def __str__(self):
        return "Icon of {title}".format(title=self.category.title)


class Tag(models.Model):
    """Represents a tag in the system."""

    name = models.CharField(max_length=128, unique=True, db_index=True)

    def __str__(self):
        return "{name}".format(name=self.name)


class Product(models.Model):
    """Represents a product in the system."""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product_category"
    )
    title = models.CharField(max_length=128, null=False, blank=False)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    fullDescription = models.TextField(null=True, blank=True)
    freeDelivery = models.BooleanField(default=True)
    limited_edition = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, related_name="product_tags")
    specifications = models.ManyToManyField(
        "Specification",
        through="SpecificationValue",
        related_name="product_specifications",
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["pk"]

    def __str__(self):
        return "{title}".format(title=self.title)


class Specification(models.Model):
    """Represents a specification in the system."""

    name = models.CharField(max_length=128)

    def __str__(self):
        return "{name}".format(name=self.name)


class SpecificationValue(models.Model):
    """Represents a value for a specific product specification."""

    specification = models.ForeignKey(
        Specification, on_delete=models.CASCADE, related_name="specification_values"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_values"
    )
    value = models.CharField(max_length=128)

    def __str__(self):
        return "{specification}: {value}".format(
            specification=self.specification,
            value=self.value
        )


class ProductImage(models.Model):
    """Represents an image associated with a product."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    src = models.ImageField(
        upload_to=product_image_directory_path, verbose_name="Image link"
    )
    alt = models.CharField(
        max_length=128,
        verbose_name="Image description",
        default="Image description"
    )

    class Meta:
        verbose_name = "Product image"
        verbose_name_plural = "Product images"
        ordering = ["pk"]

    def __str__(self):
        """
        Returns a string representation of the image description.
        """

        return "{alt}".format(alt=self.alt)


class Review(models.Model):
    """Represents a review for a product."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    author = models.CharField(max_length=128, default="Anonymous")
    email = models.EmailField()
    text = models.TextField()
    rate = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["pk"]

    def __str__(self):
        """
        Returns a string representation of the author's name.
        """

        return "{author}".format(author=self.author)


class Sale(models.Model):
    """Represents a sale for a product."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dateFrom = models.DateField(blank=True, null=True)
    dateTo = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

    def __str__(self):
        """
        Returns a string representation of the sale, using the product title.
        """
        return "{title}".format(title=self.product.title)
