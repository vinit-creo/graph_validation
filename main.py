from validate_pills import PillPositionValidator

validator = PillPositionValidator()

images = [
    "assets/asset_1.jpg",
    "assets/asset_2.jpg",
    "assets/asset_3.jpg",
    "assets/asset_4.jpg",
]
# will have to fetch from the api in the appium drive file.
expected_time = ["8:00 PM", "9:00 PM", "12:00 PM", "10:00 AM"]

# Run validation for each image
for image_path in images:
    print(f"\nValidating {image_path}...")

    tensor_image, image_size = validator.load_image(image_path)

    red_mask = validator.detect_red_pill(tensor_image)

    detected_pos = validator.find_pill_position(red_mask)

    is_valid, message = validator.validate_position(
        detected_pos, "8:00 PM", image_size  # Expected time
    )
    print(f"Validation result: {'Valid' if is_valid else 'Invalid'}")
    print(message)

    validator.visualize_validation(image_path, detected_pos, "8:00 PM")
