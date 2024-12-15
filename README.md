# Pill Position Validator

A PyTorch-based tool for validating the position of pill indicators in medical symptom tracking graphs. This tool analyzes graph images to verify if medication indicators (pills) are placed at the correct time positions.

## Features

- Tensor-based image processing for efficient pill detection
- Validates pill positions against expected time markers
- Supports both time and vertical position validation
- Includes visualization tools for validation results
- GPU acceleration support (when available)
- Configurable tolerance settings for position validation

## Prerequisites

- Python 3.7+
- PyTorch
- torchvision
- Pillow (PIL)
- matplotlib

## Installation

1. Clone this repository:

```bash
git clone https://github.com/vinit-creo/pill-position-validator.git
cd pill-position-validator
```

2. Install required packages:

```bash
pip install torch torchvision pillow matplotlib
```

## Usage

### Basic Usage

```python
from pill_validator import PillPositionValidator

# Create validator instance
validator = PillPositionValidator()

# Validate a single image
is_valid, message = validate_graph_image("path_to_graph.png", "8:00 PM")
print(f"Validation result: {'Valid' if is_valid else 'Invalid'}")
print(message)
```

### Batch Processing

```python
# Validate multiple images
image_paths = [
    "slowness_graph.png",
    "shaking_graph.png",
    "wiggling_graph.png",
    "feet_glued_graph.png"
]

for image_path in image_paths:
    print(f"\nValidating {image_path}...")
    is_valid, message = validate_graph_image(image_path, "8:00 PM")
    print(f"Validation result: {'Valid' if is_valid else 'Invalid'}")
    print(message)
```

## Configuration

The validator can be configured with different parameters:

```python
validator = PillPositionValidator(
    device='cuda'  # Use 'cpu' for CPU-only processing
)

# Adjust validation tolerance
is_valid, message = validator.validate_position(
    detected_pos,
    expected_time,
    image_size,
    tolerance_minutes=5  # Adjust time tolerance
)
```

## Class Description

### PillPositionValidator

Main class for pill position validation.

#### Methods

- `load_image(image_path)`: Loads and preprocesses the graph image
- `detect_red_pill(tensor_image)`: Detects red pill indicator in the image
- `find_pill_position(red_mask)`: Calculates pill position from detection mask
- `validate_position(detected_pos, expected_time, image_size)`: Validates pill position
- `visualize_validation(image_path, detected_pos, expected_time)`: Creates visualization

## Validation Criteria

The validator checks two main criteria:

1. Time Position (X-axis):
   - Converts pixel position to time
   - Compares with expected time within tolerance

2. Vertical Position (Y-axis):
   - Validates if pill is in the correct vertical range
   - Typically expects pill in top 15% of graph

## Visualization

The validator provides visualization tools to help understand the validation results:

- Original image overlay
- Detected pill position (green marker)
- Expected position (red marker)
- Time alignment indicators

## Error Messages

Common error messages and their meaning:

- "No pill detected": Failed to find red pill in image
- "Invalid time position": Pill not at expected time
- "Invalid Y position": Pill not at correct height

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions and support, please open an issue in the GitHub repository.
