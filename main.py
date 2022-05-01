from PIL import Image, ImageDraw

image = Image.open("./cat.jpg")
print("before resize:", image.size)

# Resize the given image into a fixed size of width 500

image.thumbnail((500, 500))
image.show()
print("after:", image.size)

# Apply Luminosity (Contrast) for the given image

red, green, blue = image.split()
redPixel = red.load()
greenPixel = green.load()
bluePixel = blue.load()

# Get min pixel intensity value.
minRed = minGreen = minBlue = float('inf')
for i in range(0, image.width):
    for j in range(0, image.height):
        if redPixel[i, j] <= minRed:
            minRed = redPixel[i, j]
        if greenPixel[i, j] <= minGreen:
            minGreen = greenPixel[i, j]
        if bluePixel[i, j] <= minBlue:
            minBlue = bluePixel[i, j]
minIntensity = min(minRed, minGreen, minBlue)

# Get max pixel intensity value.
maxRed = maxGreen = maxBlue = float('-inf')
for i in range(0, image.width):
    for j in range(0, image.height):
        if redPixel[i, j] >= maxRed:
            maxRed = redPixel[i, j]
        if greenPixel[i, j] >= maxGreen:
            maxGreen = greenPixel[i, j]
        if bluePixel[i, j] >= maxBlue:
            maxBlue = bluePixel[i, j]
maxIntensity = max(maxRed, maxGreen, maxBlue)

# Apply the normalization equation for each intensity level in the image pixel.
for i in range(0, image.width):
    for j in range(0, image.height):
        redPixel[i, j] = int(((redPixel[i, j] - minIntensity)*255)/maxIntensity - minIntensity)
        greenPixel[i, j] = int(((greenPixel[i, j] - minIntensity)*255)/maxIntensity - minIntensity)
        bluePixel[i, j] = int(((bluePixel[i, j] - minIntensity)*255)/maxIntensity - minIntensity)
normalizeIMG = Image.merge('RGB', (red, green, blue))
normalizeIMG.show()
normalizeIMG.save("Normalized.jpg")

# Apply Laplacian filter on the obtained image from the previous step
# (implement a function that takes stride and padding and the filter as parameters)


def apply_filter(applied_filter, img):
    pixels = img.load()
    index = len(applied_filter) // 2
    filterImg = Image.new('RGB', img.size)
    draw = ImageDraw.Draw(filterImg)
    for x in range(index, img.width - index):
        for y in range(index, img.height - index):
            acc = [0, 0, 0]
            for i in range(len(applied_filter)):
                for j in range(len(applied_filter)):
                    xn = x + i - index
                    yn = y + j - index
                    pix = pixels[xn, yn]
                    acc[0] += pix[0] * applied_filter[i][j]
                    acc[1] += pix[1] * applied_filter[i][j]
                    acc[2] += pix[2] * applied_filter[i][j]
                draw.point((x, y), (int(acc[0]), int(acc[1]), int(acc[2])))

    return filterImg


laplacianFilter = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
filteredImg = apply_filter(laplacianFilter, normalizeIMG)
filteredImg.save("filteredImg.jpg")
filteredImg.show()
