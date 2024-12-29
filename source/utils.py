import imagehash
from PIL import Image


def format_timestamp(timestamp):
    hr = int(timestamp // 3600000)
    min = int((timestamp % 3600000) // 60000)
    sec = int((timestamp % 60000) // 1000)
    msec = int(timestamp % 1000)
    return hr, min, sec, msec

def are_images_similar(image1, image2, hash_size=8, threshold=10):
    hash1 = imagehash.average_hash(Image.fromarray(image1), hash_size=hash_size)
    hash2 = imagehash.average_hash(Image.fromarray(image2), hash_size=hash_size)

    return abs(hash1 - hash2) <= threshold
