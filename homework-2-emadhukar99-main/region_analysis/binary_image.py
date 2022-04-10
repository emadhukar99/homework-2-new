import numpy as np
class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram as a list"""

        hist = [0]*256
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                hist[image[i, j]] = hist[image[i, j]] + 1

        return hist

    def find_otsu_threshold(self, hist):
        """analyses a histogram it to find the otsu's threshold assuming that the input hstogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value (otsu's threshold)"""

        k = len(hist) - 1
        t = int(k/2)
        prev_means = []
        first = True
        while True:

            sum1 = sum(hist[:t])
            sum2 = sum(hist[t:])

            if len(prev_means) != 2:
                u1 = np.average([i + 1 for i in range(0, t)], weights=[i / sum1 for i in hist][:t])
                u2 = np.average([i + 1 for i in range(t, len(hist))], weights=[i / sum2 for i in hist][t:])
                prev_means.append(u1)
                prev_means.append(u2)
            else:
                u1 = np.average([i + 1 for i in range(0, t)], weights=[i / sum1 for i in hist][:t])
                u2 = np.average([i + 1 for i in range(t, len(hist))], weights=[i / sum2 for i in hist][t:])

            t = int((u1 + u2) / 2)

            if not first:
                delta_u1 = u1 - prev_means[0]
                delta_u2 = u2 - prev_means[1]
                prev_means[0] = u1
                prev_means[1] = u2
                if delta_u1 != 0 and delta_u2 != 0:
                    break
            first = False

        return t


    def binarize(self, image):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        take as input
        image: an grey scale image
        returns: a binary image"""

        bin_img = image.copy()
        hist = self.compute_histogram(bin_img)
        t = self.find_otsu_threshold(hist)
        for index, value in np.ndenumerate(image):
            bin_img[index[0]][index[1]] = 255 if value < t else 0

        return bin_img


