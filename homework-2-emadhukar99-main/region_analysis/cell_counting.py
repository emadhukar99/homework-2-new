import numpy as np
import cv2

class CellCounting:
    def __init__(self):
        pass

    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes a input:
        image: binary image
        return: a list/dict of regions"""

        regions = dict()
        region_number = 1
        r = np.zeros(image.shape, np.uint32)

        for (i, j), val in np.ndenumerate(image):
            if val == 255:
                if i - 1 >= 0 and j - 1 >= 0:
                    if image[i, j - 1] == 0 and image[i - 1, j] == 0:
                        r[i, j] = region_number
                        region_number += 1
                    if image[i, j - 1] == 0 and image[i - 1, j] == 255:
                        r[i, j] = r[i - 1, j]
                    if image[i, j - 1] == 255 and image[i - 1, j] == 0:
                        r[i, j] = r[i, j - 1]

                    if image[i, j - 1] == 255 and image[i - 1, j] == 255:
                        r[i, j] = r[i-1, j]
                        r[i, j-1] = r[i-1, j]
                        d = 2
                        flag = 0
                        while flag == 0:
                            if image[i, j - d] != 0:
                                r[i, j-d] = r[i, j - d + 1]
                                d += 1
                            else:
                                flag = 1

                if i == 0 and j > 0:
                    if image[i, j - 1] == 0:
                        r[i, j] = region_number
                        region_number += 1
                    if image[i, j - 1] == 255:
                        r[i, j] = r[i, j - 1]

                if j == 0 and i > 0:
                    if image[i - 1, j] == 255:
                        r[i, j] = r[i - 1, j]
                    if image[i - 1, j] == 0:
                        r[i, j] = region_number
                        region_number += 1

        for (i, j), val in np.ndenumerate(image):
            if r[i, j] != 0:
                if r[i, j] in regions:
                    regions[r[i, j]].append([i, j])
                else:
                    regions[r[i, j]] = [[i, j]]

        return regions

    def compute_statistics(self, region):
        """Compute cell statistics area and location
        takes as input
        region: a list/dict of pixels in a region
        returns: region statistics"""

        # Please print your region statistics to stdout
        # <region number>: <location or center>, <area>
        # print(stats)

        red_regions = {m: s for m, s in region.items() if len(s) >= 15}

        stats = {}

        for region, points in red_regions.items():
            x = [p[0] for p in points]
            y = [p[1] for p in points]
            centroid = ((sum(x) / len(points)), (sum(y) / len(points)))
            stats[region] = ((int(centroid[0]), int(centroid[1])), len(points))
            print('{0}: <center: ({1:.2f}, {2:.2f})>, <area: {3} pixels>'.format(region, centroid[0], centroid[1], len(points)))

        return stats

    def mark_image_regions(self, image, stats):
        """Creates a new image with computed stats
        Make a copy of the image on which you can write text. 
        takes as input
        image: a list/dict of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""

        img = image.copy()
        img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        for i in stats:

            region_area = str(i) + ',' + str(stats[i][1])
            cv2.putText(img, "*", (stats[i][0][1] - 4, stats[i][0][0] + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 1, 16)
            cv2.putText(img, region_area, (stats[i][0][1], stats[i][0][0]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.22, (255, 170, 20), 1, 5)

        return img

