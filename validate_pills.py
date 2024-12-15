import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


class PillPositionValidator:
    def __init__(self, device="cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        self.transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

    def load_image(self, image_path):
        """Load and preprocess image."""
        image = Image.open(image_path).convert("RGB")
        tensor_image = self.transform(image).unsqueeze(0).to(self.device)
        return tensor_image, image.size

    def detect_red_pill(self, tensor_image):
        """Detect red pill in the image using color thresholding."""
        # Convert normalized tensor back to 0-1 range
        image = tensor_image * torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1).to(
            self.device
        )
        image = image + torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1).to(
            self.device
        )

        # Create red mask
        red_mask = (image[:, 0] > 0.6) & (image[:, 1] < 0.4) & (image[:, 2] < 0.4)

        return red_mask

    def find_pill_position(self, red_mask):
        """Find pill position from binary mask."""
        # Get indices of red pixels
        y_indices, x_indices = torch.where(red_mask[0])

        if len(y_indices) == 0:
            return None

        # Calculate center of mass
        x_center = x_indices.float().mean()
        y_center = y_indices.float().mean()

        return torch.tensor([x_center, y_center])

    def time_to_x_position(self, time_str, image_width):
        """Convert time string to expected x position."""
        time_obj = datetime.strptime(time_str, "%I:%M %p")
        hours = time_obj.hour + time_obj.minute / 60
        return (hours / 24) * image_width

    def validate_position(
        self, detected_pos, expected_time, image_size, tolerance_minutes=5
    ):
        """Validate detected pill position."""
        if detected_pos is None:
            return False, "No pill detected"

        width, height = image_size

        # Convert expected time to x position
        expected_x = self.time_to_x_position(expected_time, width)

        # Calculate tolerance in pixels
        x_tolerance = (tolerance_minutes / (24 * 60)) * width

        # Check x position (time)
        x_diff = abs(detected_pos[0] - expected_x)
        time_valid = x_diff <= x_tolerance

        # Check y position (should be in top 15% of graph)
        y_valid = detected_pos[1] <= height * 0.15

        is_valid = time_valid and y_valid

        # Calculate actual time from position
        actual_hours = (detected_pos[0] / width) * 24
        actual_hour = int(actual_hours)
        actual_minute = int((actual_hours - actual_hour) * 60)
        actual_time = f"{actual_hour:02d}:{actual_minute:02d}"

        message = f"""
        Time position: {"Valid" if time_valid else "Invalid"}
        Expected time: {expected_time}
        Detected time: {actual_time}
        X difference: {x_diff:.2f} pixels (tolerance: {x_tolerance:.2f})
        Y position: {"Valid" if y_valid else "Invalid"} ({detected_pos[1]:.2f})
        """

        return is_valid, message

    def visualize_validation(self, image_path, detected_pos, expected_time):
        """Visualize the validation results."""
        # Load original image
        image = Image.open(image_path).convert("RGB")
        plt.figure(figsize=(12, 6))

        # Plot original image
        plt.imshow(image)

        if detected_pos is not None:
            # Plot detected position
            plt.plot(
                detected_pos[0], detected_pos[1], "go", markersize=10, label="Detected"
            )

            # Plot expected position
            expected_x = self.time_to_x_position(expected_time, image.size[0])
            plt.plot(expected_x, detected_pos[1], "ro", markersize=10, label="Expected")

            # Add legend
            plt.legend()

        plt.title("Pill Position Validation")
        plt.axis("on")
        plt.show()


def validate_graph_image(image_path, expected_time):
    """Validate pill position in a graph image."""
    validator = PillPositionValidator()

    # Load and process image
    tensor_image, image_size = validator.load_image(image_path)

    # Detect pill
    red_mask = validator.detect_red_pill(tensor_image)

    # Find pill position
    detected_pos = validator.find_pill_position(red_mask)

    # Validate position
    is_valid, message = validator.validate_position(
        detected_pos, expected_time, image_size
    )

    # Visualize results
    validator.visualize_validation(image_path, detected_pos, expected_time)

    return is_valid, message


# Example usage
if __name__ == "__main__":
    # Example validation for your graph images
    for image_path in ["slowness.png", "shaking.png", "wiggling.png", "feet_glued.png"]:
        print(f"\nValidating {image_path}...")
        is_valid, message = validate_graph_image(image_path, "8:00 PM")
        print(f"Validation result: {'Valid' if is_valid else 'Invalid'}")
        print(message)
