# -*- encoding: utf-8 -*-
import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import Voronoi


def draw_image(width=1500, height=500, nb_spirals=250, width_margin=1000, height_margin=500,
               ratio=0.05, min_dist=0, max_iter=100, color=None, outfile=None):
    """
    Draw the image with the spirals.

    :param width: width of the image.
    :param height: height of the image.
    :param nb_spirals: number of spirals in the image.
    :param width_margin: margin to continue drawing outside of the image.
    :param height_margin: margin to continue drawing outside of the image.
    :param ratio: ratio used to move the next vertex along the edge.
    :param min_dist: stop criterion: minimal distance between two vertices.
    :param max_iter: stop criterion: maximal iteration.
    :param color: color of the spirals as a RGB tuple.
    !:param outfile: Output file for saving the drawing (default: None, image not saved).
    :return:
    """
    # Create the image
    im = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)
    # Compute the vertices and regions
    vertices, regions = create_vertices(width, height, nb_spirals, width_margin, height_margin)
    # Draw the spirals
    for r in regions:
        draw_spiral(draw, vertices[r], ratio=ratio, min_dist=min_dist, max_iter=max_iter, color=color)
    im.show()

    print("{} spirals drawn.".format(len(regions)))

    if outfile:
        im.save(outfile)


def create_vertices(width, height, nb_spirals, width_margin, height_margin):
    """
    Create random vertices and edges.

    The margin aims to avoid empty regions on he border of the image.

    :param width: width of the target image.
    :param height: height of the target image.
    :param nb_spirals: number of spirals.
    :param width_margin: margin to continue drawing outside of the image.
    :param height_margin: margin to continue drawing outside of the image.
    :return: The list of vertices and regions as a tuple.
    """

    x = np.random.random_integers(0 - width_margin, width + width_margin, (nb_spirals, 1))
    y = np.random.random_integers(0 - height_margin, height + height_margin, (nb_spirals, 1))
    points = np.hstack((x, y))

    vor = Voronoi(points)  # use the random points as seeds for the Voronoi diagram.

    # remove regions '-1' and regions and keep regions with at least 3 vertices.
    regions = []
    for reg in vor.regions:
        if reg and -1 not in reg:
            regions.append(reg)
        elif reg:
            reg.remove(-1)
            if len(reg) >= 3:
                regions.append(reg)

    return vor.vertices, regions


def draw_spiral(draw, vertices, ratio=0.05, min_dist=0, max_iter=100, color=None):
    """
    Draw a spiral.

    :param draw: the ImageDraw.Draw object.
    :param vertices: the vertices of the spiral.
    :param ratio: ratio used to move the next vertex along the edge (default: 0.05).
    :param min_dist: stop criterion: minimal distance between two vertices (default: 0).
    :param max_iter: stop criterion: maximal iteration (default: 100).
    :param color: color of the spiral as a RGB tuple (default: random).
    :return:
    """
    assert len(vertices) >= 3

    if not color:
        color = tuple(np.random.randint(0, 255, 3))

    new_vert = vertices
    current_vertex = 0
    loop_count = 0
    while True:
        if current_vertex == 0:
            loop_count += 1
        if loop_count >= max_iter:
            break

        draw.line((new_vert[current_vertex][0],
                   new_vert[current_vertex][1],
                   new_vert[(current_vertex + 1) % len(new_vert)][0],
                   new_vert[(current_vertex + 1) % len(new_vert)][1]),
                  fill=color)

        if loop_count != 0 and not (loop_count == 1 and current_vertex == 0):
            new_vert[current_vertex][0] = (1 - ratio) * new_vert[current_vertex][0] + \
                                          ratio * new_vert[(current_vertex + 1) % len(new_vert)][0]
            new_vert[current_vertex][1] = (1 - ratio) * new_vert[current_vertex][1] + \
                                          ratio * new_vert[(current_vertex + 1) % len(new_vert)][1]

            if np.linalg.norm(np.asarray(new_vert[current_vertex]) -
                              np.asarray(new_vert[(current_vertex + 1) % len(new_vert)])) <= min_dist:
                break

        current_vertex = (current_vertex + 1) % len(new_vert)


if __name__ == "__main__":
    draw_image(width=1500, height=500, nb_spirals=250, width_margin=1000, height_margin=500,
               ratio=0.05, min_dist=0, max_iter=100, color=None,
               outfile=None)
