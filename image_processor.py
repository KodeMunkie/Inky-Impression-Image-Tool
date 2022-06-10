import sys;

class ImageProcessor:

    TARGET_PALETTE = [
        [0x0c,0x0c,0x0e], # Black
        [0xd2,0xd2,0xd0], # White
        [0x1e,0x60,0x1f], # Green
        [0x1d,0x1e,0xaa], # Blue
        [0x8c,0x1b,0x1d], # Red
        [0xd3,0xc9,0x3d], # Yellow
        [0xc1,0x71,0x2a], # Orange
    ]

    EIGHTH = 1/8

    cache = dict()

    def __init__(self):
        self

    def euclidean_distance(self, source_colour, target_colour):
        red_diff = source_colour[0] - target_colour[0]
        green_diff = source_colour[1] - target_colour[1]
        blue_diff = source_colour[2] - target_colour[2]
        return (red_diff*red_diff) + (green_diff*green_diff) + (blue_diff*blue_diff)

    def get_closest_colour(self, old_pixel):
        closest = self.cache.get(old_pixel, None)
        if (closest != None) :
            return closest

        best_candidate = self.TARGET_PALETTE[0]
        best_distance = sys.maxsize
        for candidate in self.TARGET_PALETTE:
            candidate_distance = self.euclidean_distance(old_pixel, candidate)
            if candidate_distance < best_distance:
                best_distance = candidate_distance
                best_candidate = candidate
        self.cache[old_pixel] = best_candidate
        return best_candidate

    def is_in_bounds(self, output, x, y):
       return x>=0 and y>=0 and x<output.width and y<output.height 

    def clamp(self, value): 
        if (value>255):
            return 255
        if (value<0):
            return 0
        return value

    def calculate_adjusted_rgb(self, old_rgb, new_rgb, diffused_rgb):	
        red = self.clamp(diffused_rgb[0] + (self.EIGHTH*(old_rgb[0] - new_rgb[0])))
        green = self.clamp(diffused_rgb[1] + (self.EIGHTH*(old_rgb[1] - new_rgb[1])))
        blue = self.clamp(diffused_rgb[2] + (self.EIGHTH*(old_rgb[2] - new_rgb[2])))
        return (int(red), int(green), int(blue))


    def distribute_error(self, output, old_pixel, new_pixel, x, y):
        xPlus1 = self.is_in_bounds(output, x+1, y)
        yPlus1 = self.is_in_bounds(output, x, y+1)
        if xPlus1:
            adjPixel = self.calculate_adjusted_rgb(old_pixel, new_pixel, output.getpixel((x+1, y)))
            output.putpixel((x+1, y), adjPixel)
        if self.is_in_bounds(output, x+2, y): 
            adjPixel = self.calculate_adjusted_rgb(old_pixel, new_pixel, output.getpixel((x+2, y)))
            output.putpixel((x+2, y), adjPixel)
        if self.is_in_bounds(output, x-1, y+1):
            adjPixel = self.calculate_adjusted_rgb(old_pixel, new_pixel, output.getpixel((x-1, y+1)))
            output.putpixel((x-1, y+1), adjPixel)

        if yPlus1:
            adjPixel = self.calculate_adjusted_rgb(old_pixel, new_pixel, output.getpixel((x, y+1)))
            output.putpixel((x, y+1), adjPixel)
        if self.is_in_bounds(output, x, y+2):
            adjPixel = self.calculate_adjusted_rgb(old_pixel, new_pixel, output.getpixel((x, y+2)))
            output.putpixel((x, y+2), adjPixel)
        if xPlus1 and yPlus1:
            adjPixel = self.calculate_adjusted_rgb(old_pixel, new_pixel, output.getpixel((x+1, y+1)))
            output.putpixel((x+1, y+1), adjPixel)

    def diffuse_pixel(self, output, x, y):
        oldPixel = output.getpixel((x,y))
        newPixel = self.get_closest_colour(oldPixel)
        output.putpixel((x,y), (newPixel[0], newPixel[1], newPixel[2]))
        self.distribute_error(output, oldPixel, newPixel, x, y)

    def diffuse_image(self, source_image): 
        # Cache should max ~70MB if every colour combo calculated but uncomment if memory issues.
        #self.cache.clear()
        height_range = range(0, source_image.height)
        width_range = range(0, source_image.width)
        for y in height_range:
            for x in width_range:
                self.diffuse_pixel(source_image, x, y)