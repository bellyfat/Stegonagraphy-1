from PIL import Image

#trailBits - how many bits per byte of the secret image should be hidden
#cover - cover image path
#secret - secret image path
def embed(trailBits, cover, secret):
    leadBits = 8-trailBits
    img = Image.open(cover, mode='r')
    sec = Image.open(secret, mode='r')
    width, height = img.size

    #get the bytes of the images and begin a new byte array to be added to
    imgBytes = img.tobytes()
    secBytes = sec.tobytes()
    newImg = bytearray(len(imgBytes))

    #loop through each image, byte by byte
    #n = number of trailBits
    #add the n most significant bits from the secret image as the n least significant bits in the new embedded image
    #add the 8 - n most significant bits from the cover image as the most significant bits in the new image
    for i in range(len(imgBytes)):
        str = "{0:08b}".format(imgBytes[i])[:leadBits] + "{0:08b}".format(secBytes[i])[:trailBits]
        newImg[i] = int(str, 2)

    #get the bytes of the byte array and create the embedded png
    newImgBytes = bytes(newImg)
    image = Image.frombytes("RGB", (width, height), newImgBytes)
    image.save("embedded.png")

#trailBits - how many bits per byte of the secret image have been hidden
#image - the image to extract from
def extract(trailBits, image):
    endBits = 8 - trailBits
    img = Image.open(image, mode='r')
    width, height = img.size

    #get the bytes of the embedded image and create a byte array to place the extracted bytes in
    imgBytes = img.tobytes()
    newImg = bytearray(len(imgBytes))

    #loop through every byte of the embedded image
    #n = trailBits
    #copy the n least significant bits into a new binary string as the n most significant bits
    for i in range(len(imgBytes)):
        str = "{0:08b}".format(imgBytes[i])[endBits:]
        #add the required amount of 0s to ensure 8 bits in every byte
        for j in range(0, endBits):
            str += "0"
        newImg[i] = int(str, 2)

    #get the bytes of the byte array and create the extracted png
    recoveredImgBytes = bytes(newImg)
    image = Image.frombytes("RGB", (width, height), recoveredImgBytes)
    image.save("extracted.png")

def main():
    embed(4, "steg_cover.png", "steg_secret.png")
    extract(4, "embedded.png")

if __name__ == "__main__":
    main()