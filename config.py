# Game Configuration Settings

# Robot movement speed (seconds per step)
# Lower values = faster movement
# Recommended range: 0.01 to 1.0
MOVE_SPEED = 0.5

# Map selection
# Corresponds to map files in maps/ directory
MAP_NUMBER = '0'

# Grid size (N x N)
GRID_SIZE = 10

# Window size (pixels)
WINDOW_SIZE = 640

# Calculate cell size based on window and grid
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Time to display win screen (seconds)
WIN_DISPLAY_TIME = 5

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80
BUTTON_COLOR = (50, 200, 50)  # Green
BUTTON_HOVER_COLOR = (70, 220, 70)  # Lighter green
BUTTON_TEXT_COLOR = (255, 255, 255)  # White

# Colors
GRID_COLOR_1 = (240, 240, 240)  # Light gray
GRID_COLOR_2 = (220, 220, 220)  # Slightly darker gray
GRID_LINE_COLOR = (200, 200, 200)  # Grid lines
BACKGROUND_COLOR = (255, 255, 255)  # White 