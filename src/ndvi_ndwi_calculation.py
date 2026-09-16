import numpy as np
import rasterio
import matplotlib.pyplot as plt

B4_PATH = 'data/B4.tif'
B5_PATH = 'data/B5.tif'
B3_PATH = 'data/B3.tif'

NDVI_OUTPUT = 'docs/ndvi_calculated.png'
NDWI_OUTPUT = 'docs/ndwi_calculated.png'

RADIANCE_MULT = 0.0000275
RADIANCE_ADD = -0.2


def read_band(path):
    with rasterio.open(path) as src:
        band = src.read(1).astype(np.float32)
        nodata = src.nodata
        if nodata is not None:
            band[band == nodata] = np.nan
    return band


def normalize(band):
    return band * RADIANCE_MULT + RADIANCE_ADD


def calculate_index(a, b):
    with np.errstate(divide='ignore', invalid='ignore'):
        index = (a - b) / (a + b)
    index[np.isinf(index)] = np.nan
    return index


def save_map(index, path, title, cmap):
    plt.figure(figsize=(10, 6))
    plt.imshow(index, cmap=cmap, vmin=-1, vmax=1)
    plt.colorbar(label='Значение индекса')
    plt.title(title)
    plt.axis('off')
    plt.savefig(path, dpi=200, bbox_inches='tight')
    plt.close()


b4 = normalize(read_band(B4_PATH))
b5 = normalize(read_band(B5_PATH))
b3 = normalize(read_band(B3_PATH))

ndvi = calculate_index(b5, b4)
ndwi = calculate_index(b3, b5)

print(f'NDVI: min={np.nanmin(ndvi):.4f}, max={np.nanmax(ndvi):.4f}, mean={np.nanmean(ndvi):.4f}')
print(f'NDWI: min={np.nanmin(ndwi):.4f}, max={np.nanmax(ndwi):.4f}, mean={np.nanmean(ndwi):.4f}')

save_map(ndvi, NDVI_OUTPUT, 'Вегетационный индекс NDVI', 'RdYlGn')
save_map(ndwi, NDWI_OUTPUT, 'Влажностный индекс NDWI', 'Blues')

print('Карты сохранены:', NDVI_OUTPUT, NDWI_OUTPUT)