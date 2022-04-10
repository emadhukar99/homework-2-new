import numpy as np

class Rle:
    def __init__(self):
        pass

    def encode_image(self,binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """

        pixels = binary_image.flatten()
        rle_code = [pixels[0]]
        pixel_count = len(pixels)
        count = 1

        for i in range(1,pixel_count):

            if pixels[i] == pixels[i-1]:
                count += 1
            else:
                rle_code.append(count)
                count = 1

        rle_code.append(count)

        return rle_code  # replace zeros with rle_code

    def decode_image(self, rle_code, height , width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """

        pixel_rate = rle_code[0]
        run_value = rle_code[1:]
        image = []
        for i in run_value:
            p = [pixel_rate]*i
            image += p
            if pixel_rate == 0 :
                pixel_rate = 255 
            else :
                pixel_rate = 0

        image = np.asarray(image)

        return image.reshape(height, width)  # replace zeros with image reconstructed from rle_Code





        




