#!/usr/bin/env python3
"""
Convert latitude/longitude to Maidenhead Grid Square locator.
Supports 2, 4, 6, 8, or 10-character precision.
"""


def latlon_to_grid(lat, lon, precision=10):
	"""
	Convert latitude and longitude to Maidenhead Grid Square.

	Args:
	    lat (float): Latitude in decimal degrees (-90 to 90)
	    lon (float): Longitude in decimal degrees (-180 to 180)
	    precision (int): Number of characters in the grid (2, 4, 6, 8, or 10)

	Returns:
	    str: Maidenhead grid square string.
	"""
	# Validate inputs
	if not (-90 <= lat <= 90):
		raise ValueError('Latitude must be between -90 and 90 degrees.')
	if not (-180 <= lon <= 180):
		raise ValueError('Longitude must be between -180 and 180 degrees.')
	if precision not in (2, 4, 6, 8, 10):
		raise ValueError('Precision must be 2, 4, 6, 8, or 10 characters.')

	# Shift coordinates to positive values
	lon += 180
	lat += 90

	# First pair: Fields (A-R)
	field_lon = int(lon // 20)
	field_lat = int(lat // 10)
	grid = chr(field_lon + ord('A')) + chr(field_lat + ord('A'))

	if precision >= 4:
		# Second pair: Squares (0-9)
		square_lon = int((lon % 20) // 2)
		square_lat = int((lat % 10) // 1)
		grid += str(square_lon) + str(square_lat)

	if precision >= 6:
		# Third pair: Sub-squares (a-x)
		subsq_lon = int(((lon % 2) / 2) * 24)
		subsq_lat = int(((lat % 1) / 1) * 24)
		grid += chr(subsq_lon + ord('a')) + chr(subsq_lat + ord('a'))

	if precision >= 8:
		# Fourth pair: Extended digits (0-9)
		ext_lon = int(((((lon % 2) / 2) * 24) % 1) * 10)
		ext_lat = int(((((lat % 1) / 1) * 24) % 1) * 10)
		grid += str(ext_lon) + str(ext_lat)

	if precision == 10:
		# Fifth pair: Extra subsquares (a-x)
		fine_lon = int(((((((lon % 2) / 2) * 24) % 1) * 10) % 1) * 24)
		fine_lat = int(((((((lat % 1) / 1) * 24) % 1) * 10) % 1) * 24)
		grid += chr(fine_lon + ord('a')) + chr(fine_lat + ord('a'))

	return grid


# Example usage
if __name__ == '__main__':
	try:
		# Example: Kuala Lumpur (lat=3.1390, lon=101.6869)
		lat = float(input('Enter latitude (-90 to 90): '))
		lon = float(input('Enter longitude (-180 to 180): '))
		precision = int(input('Enter precision (2, 4, 6, 8, or 10): '))

		grid_square = latlon_to_grid(lat, lon, precision)
		print(f'Maidenhead Grid Square ({precision} chars): {grid_square}')

	except ValueError as e:
		print(f'Error: {e}')
	except Exception as e:
		print(f'Unexpected error: {e}')
