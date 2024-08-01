class TransformerImage:
    def __init__(self, image, transform):
        self.image = image
        self.transform = transform

    def transform_image(self):
        # Apply the transform to the image
        transformed_image = self.transform(self.image)

        return transformed_image
