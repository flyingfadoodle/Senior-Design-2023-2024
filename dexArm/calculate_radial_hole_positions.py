import math

def calculate_and_index_hole_positions(radius, dx, num_holes=5, num_rows=6, dy=25):
    """
    Calculate and index the positions of holes on multiple arcs stacked vertically.
    
    Parameters:
    - radius (float): Radius of the arc in mm.
    - dx (float): Horizontal separation between the centers of the holes in mm.
    - num_holes (int): Number of holes per row.
    - num_rows (int): Total number of rows.
    - dy (float): Vertical separation between rows in mm.

    Returns:
    - dict: A dictionary with keys as (row, col) tuples and values as (x, y) coordinates.
    """
    indexed_positions = {}
    theta_increment = dx / radius  # Angular increment in radians
    origin_index = num_holes // 2  # Index of the central hole
    
    for row in range(num_rows):
        y_offset = row * dy  # Calculate the y offset for the current row
        for i in range(num_holes):
            angle = (i - origin_index) * theta_increment
            x = radius * math.sin(angle)
            y = radius * math.cos(angle) + y_offset
            indexed_positions[(row + 1, i + 1)] = (x, y)
    
    return indexed_positions

# Example Usage
radius = 230  # radius of the arc in mm
dx = 28.574  # horizontal separation between holes in mm
positions = calculate_and_index_hole_positions(radius, dx)
for index, coord in sorted(positions.items()):
    print(f"Index {index}: (x={coord[0]:.2f}, y={coord[1]:.2f})")
