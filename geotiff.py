import rasterio
import numpy as np

def write(path, image, transparency_mask, left_corner_x, left_corner_y, pixel_size_in_m):
  transform = rasterio.transform.from_origin(left_corner_x, left_corner_y, pixel_size_in_m, pixel_size_in_m)

  new_image = np.moveaxis(image, [0, 1, 2], [2, 1, 0])

  new_dataset = rasterio.open(
    path,
    'w',
    driver='GTiff',                  
    height = new_image.shape[1],
    width = new_image.shape[2],
    count=3,
    dtype=str(new_image.dtype),
    crs=rasterio.crs.CRS.from_epsg(32634),
    transform=transform
  )

  new_dataset.write_mask(np.moveaxis(transparency_mask, [0, 1], [1, 0]))
  new_dataset.write(new_image)
  new_dataset.close()

  # Other transform 
  # transform = rasterio.transform.from_bounds(start_x, start_y, end_x, end_y, new_image.shape[1], new_image.shape[2]) # (west, south, east, north, width, height)
