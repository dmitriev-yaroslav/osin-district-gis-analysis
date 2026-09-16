import numpy as np
import rasterio
import matplotlib.pyplot as plt

DEM_PATH = 'data/srtm.tif'
SLOPE_OUTPUT = 'docs/slope_calculated.png'
HIST_OUTPUT = 'docs/slope_histogram.png'


def read_dem(path):
    with rasterio.open(path) as src:
        dem = src.read(1).astype(np.float32)
        nodata = src.nodata
        if nodata is not None:
            dem[dem == nodata] = np.nan
        pixel_size = src.res[0]
    return dem, pixel_size


def calculate_slope(dem, pixel_size):
    dy, dx = np.gradient(dem, pixel_size)
    slope_rad = np.arctan(np.sqrt(dx ** 2 + dy ** 2))
    slope_deg = np.degrees(slope_rad)
    return slope_deg


dem, pixel_size = read_dem(DEM_PATH)
slope = calculate_slope(dem, pixel_size)

print(f'Высоты: min={np.nanmin(dem):.1f}, max={np.nanmax(dem):.1f}')
print(f'Уклоны: min={np.nanmin(slope):.2f}, max={np.nanmax(slope):.2f}, mean={np.nanmean(slope):.2f}')

plt.figure(figsize=(10, 6))
plt.imshow(slope, cmap='YlOrRd', vmin=0, vmax=np.nanmax(slope))
plt.colorbar(label='Уклон, градусы')
plt.title('Карта уклонов')
plt.axis('off')
plt.savefig(SLOPE_OUTPUT, dpi=200, bbox_inches='tight')
plt.close()

plt.figure(figsize=(10, 6))
plt.hist(slope.flatten(), bins=50, color='#c0392b', edgecolor='white')
plt.xlabel('Уклон, градусы')
plt.ylabel('Число пикселей')
plt.title('Распределение уклонов')
plt.grid(alpha=0.3)
plt.savefig(HIST_OUTPUT, dpi=200, bbox_inches='tight')
plt.close()

print('Карта сохранена:', SLOPE_OUTPUT)
print('Гистограмма сохранена:', HIST_OUTPUT)