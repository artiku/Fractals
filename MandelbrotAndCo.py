from PIL import Image, ImageDraw


class Fractal:
    """Class for drawing fractal."""

    def __init__(self, size, scale, computation):
        """Constructor.

        Arguments:
        size -- the size of the image as a tuple (x, y)
        scale -- the scale of x and y as a list of 2-tuple
                 [(minimum_x, minimum_y), (maximum_x, maximum_y)]
        computation -- the function used for computing pixel values as a function
        """
        self.scale = scale
        self.size = size
        self.computation = computation
        self.coordinate_step_for_x = abs(self.scale[0][0] - self.scale[1][0]) / self.size[0]
        self.coordinate_step_for_y = abs(self.scale[0][1] - self.scale[1][1]) / self.size[1]
        self.iteration_for_pixel_dict = dict()
        self.im = Image.new("RGB", self.size)

    def compute(self):
        """Create the fractal by computing every pixel value."""
        d = ImageDraw.Draw(self.im)

        for y_num, y in enumerate([self.scale[1][1] - self.coordinate_step_for_y * a for a in range(self.size[1])]):  # Calculate Y
            print("{} of {}".format(y_num, self.size[1]))

            for x_num, x in enumerate([self.scale[0][0] + self.coordinate_step_for_x * b for b in range(self.size[0])]):  # Calculate X
                key = self.pixel_value((x, y))  # both iteration calculation
                if self.iteration_for_pixel_dict.get(key) is None:
                    value = [(x_num, y_num)]
                else:
                    self.iteration_for_pixel_dict.get(key).append((x_num, y_num))  # add one more coord pair as cortege
                self.iteration_for_pixel_dict.setdefault(key, value)

        for iteration in self.iteration_for_pixel_dict.keys():
            m = self.iteration_for_pixel_dict.get(iteration)

            red = (iteration / len(self.iteration_for_pixel_dict)) * 50  # 50 + 50 / (len(self.iteration_for_pixel_dict) - iteration) didn't work for me
            green = 0
            blue = (iteration / len(self.iteration_for_pixel_dict)) * 100  # iteration * 0.5 + iteration
            color_string = "rgb({}%,{}%,{}%)".format(str(int(red)), str(green), str(int(blue)))
            d.point(m, fill=color_string)

            # if iteration == 0:
            #     d.point(m, fill="black")
            # elif iteration == 1:
            #     d.point(m, fill="black")
            # elif iteration % 2 == 0:
            #     d.point(m, fill="#0985e5")
            # elif iteration % 3 == 0:
            #     d.point(m, fill="#ed4a61")
            # else:
            #     d.point(m, fill="#1e1148")

    def pixel_value(self, pixel):
        """
        Return the number of iterations it took for the pixel to go out of bounds.

        Arguments:
        pixel -- the pixel coordinate (x, y)

        Returns:
        the number of iterations of computation it took to go out of bounds as integer.
        """
        return self.computation(pixel)

    def save_image(self, filename):
        """
        Save the image to hard drive.

        Arguments:
        filename -- the file name to save the file to as a string.
        """
        self.im.save(filename)
        self.im.show()


if __name__ == "__main__":

    def mandelVrot_computation(pixel):
        """Mandelbrot set computation 2nd variant."""
        z = 0
        a = complex(pixel[0], pixel[1])  # or (x + 1j * y)

        for n in range(1, 100):
            z = z ** 2 + a
            if abs(z) > 2:
                return n
        return 0

    def julia_computation(pixel):
        """Mandelbrot set computation 2nd variant."""
        z = complex(pixel[0], pixel[1])
        a = -0.85j

        for n in range(1, 100):
            z = z ** 2 + a
            if abs(z) > 2:
                return n
        return 0

    mandelbrot = Fractal((1000, 1000), [(-2, -2), (2, 2)], mandelVrot_computation)
    mandelbrot.compute()
    mandelbrot.save_image("mandelbrot.png")
    # mandelbrot2 = Fractal((1000, 1000), [(-0.74877, 0.065053), (-0.74872, 0.065103)], mandelVrot_computation)
    # mandelbrot2.compute()
    # mandelbrot2.save_image("mandelbrot2.png")
    julia = Fractal((1000, 1000), [(-1, -1), (1, 1)], julia_computation)
    julia.compute()
    julia.save_image("julia2.png")
