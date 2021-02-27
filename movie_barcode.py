import matplotlib.pyplot as plt
from PIL import Image, ImageStat
import math
import numpy as np
import cv2
import time
import io
import datetime

# OpenCV property identifiers
# https://www.ccoderun.ca/programming/doxygen/opencv/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d


def image_of_color(average_values):
    SIZE = 100
    average_values = (average_values[0], average_values[1], average_values[2])
    data = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    for i in range(SIZE):
        for j in range(SIZE):
            data[j, i] = average_values

    return data


def get_average_color(image):
    """
    Do not use, too slow. ImageStat rms is much better.
    """

    pixels = image.load()
    width = image.size[0]
    height = image.size[1]
    red = 0
    green = 0
    blue = 0
    for i in range(width):
        for j in range(height):
            pixel = pixels[i, j]
            red += pixel[0] * pixel[0]
            green += pixel[1] * pixel[1]
            blue += pixel[2] * pixel[2]

    num_pixels = height * width
    average_values = (math.sqrt(red/num_pixels),
                      math.sqrt(green/num_pixels), math.sqrt(blue/num_pixels))

    return average_values


def squeeze_barcode(video_capture, n_frames, bar_width, stop):
    """
    Creates a movie barcode by squeezing each frame to a width of bar_width pixels.

    This is just a helper method and shouldn't be explicitly called.
    See barcode() documentation for more info.

    Input
    -----
    video_capture: The VideoCapture object of the video to be made into a barcode.
    n_frames: Integer, take every n frames. Default is 1.
        If not specified, then considers only value for n_seconds parameter.
    bar_width: Integer, how many pixels wide to make each bar in the barcode. Default is 1.
    stop: Float, how far into the video to stop the bar code. Default is 1.
        Used mainly for debugging.

    Returns
    -------
    The movie barcode as a numpy array. Note this array is not the final barcode. Additional
    manipulation is done inside the barcode() function.
    """

    # number of frames in video file
    MAX_FRAMES = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    HEIGHT = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    barcode = []
    curr_frame = 0
    while(video_capture.isOpened() and curr_frame <= int(MAX_FRAMES * stop)):
        video_capture.set(1, curr_frame)
        ret, frame = video_capture.read()  # read each frame
        if ret:
            resized = Image.fromarray(frame).resize(
                (bar_width, int(HEIGHT)))
            transpose = np.transpose(resized, (1, 0, 2))
            barcode.append(transpose)
        curr_frame += n_frames
    return barcode


def average_barcode(video_capture, n_frames, bar_width, stop):
    """
    Creates a movie barcode by taking the average color of each frame.

    This is just a helper method and shouldn't be explicitly called.
    See barcode() documentation for more info.

    Input
    -----
    video_capture: The VideoCapture object of the video to be made into a barcode.
    n_frames: Integer, take every n frames. Default is 1.
        If not specified, then considers only value for n_seconds parameter.
    bar_width: Integer, how many pixels wide to make each bar in the barcode. Default is 1.
    stop: Float, how far into the video to stop the bar code. Default is 1.
        Used mainly for debugging.

    Returns
    -------
    The movie barcode as a numpy array. Note this array is not the final barcode. Additional
    manipulation is done inside the barcode() function.
    """

    # number of frames in video file
    MAX_FRAMES = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    HEIGHT = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    barcode = []
    curr_frame = 0

    curr_frame = 0
    while(video_capture.isOpened() and curr_frame <= int(MAX_FRAMES * stop)):
        video_capture.set(1, curr_frame)
        ret, frame = video_capture.read()  # read each frame
        if ret:
            color = ImageStat.Stat(Image.fromarray(frame)).rms
            color = (int(color[0]), int(color[1]), int(color[2]))
            bar = Image.new('RGB', (int(HEIGHT), bar_width), color)
            barcode.append(bar)
        curr_frame += n_frames
    return barcode


def barcode(video_file, bar_type, n_frames=-1, n_seconds=1, bar_width=1, stop=1,
            save_fig=False):
    """
    Creates a movie barcode of the input video file. This can take a while depending on the video file.

    Saves a png of the barcode with the following name:
    filename_bar_type_n_seconds_stop.png

    Changing the parameters does not affect the speed, since the majority of the time is spent
    on the VideoCapture.read() function which is called for every frame regardless of parameters.
    As such, only reducing the stop parameter value will decrease run time speed.

    Input
    -----
    video_file: String of video file, including path in necessary.
    bar_type: String, 'average' if each bar is the mean color of that frame; 'squeeze' if each bar
        is the frame squeeze.
    n_frames: Integer, take every n frames. Default is 1.
        If not specified, then considers only value for n_seconds parameter.
    n_seconds: Integer, take frame every n seconds. Default is 1.
        If n_frames value is also specified then this value is taken to be default.
    bar_width: Integer, how many pixels wide to make each bar in the barcode. Default is 1.
    stop: Float, how far into the video to stop the bar code. Default is 1.
        Used mainly for debugging.
    save_fig: Boolean, specify to save the matplotlib movie barcode. Default is False.
        Saves as png in current directory, and given the name 'movie_barcode'. It will get overwritten
        if not renamed.

    Returns
    -------
    The movie barcode as a matplotlib figure.
    """

    print("Creating movie barcode. This may take a few minutes...")
    start = time.time()  # keep track of how long it takes

    cap = cv2.VideoCapture(video_file)

    FPS = cap.get(cv2.CAP_PROP_FPS)  # frames per second
    # used later in resizing the barcode image
    WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    if n_frames == -1:
        n_frames = int(FPS) * n_seconds
    else:
        n_seconds = 1

    barcode = []
    if bar_type == 'average':
        barcode = average_barcode(cap, n_frames, bar_width, stop)
    elif bar_type == 'squeeze':
        barcode = squeeze_barcode(cap, n_frames, bar_width, stop)
    else:
        print("Incorrect bar_type parameter value.")
        return

    frames_used = len(barcode)

    cap.release()
    cv2.destroyAllWindows()

    barcode = np.concatenate(barcode)

    # color channels got swapped so put them back, and transpose
    barcode_image = Image.fromarray(
        np.transpose(barcode, (1, 0, 2))[:, :, ::-1])
    # resize barcode to be length of frame
    barcode_image = barcode_image.resize((int(WIDTH), int(HEIGHT)))

    # display barcode
    fig = plt.figure()
    plt.imshow(barcode_image)
    plt.axis('off')

    end = time.time()
    print(str((end - start) / 60) + ' minutes elapsed')
    print(str(frames_used) + " frames were used.")

    if save_fig:
        # save the figure with no white border so there is no extra whitespace if it is
        # plotted later with matplotlib
        savename = "barcode_" + bar_type + "_" + \
            str(n_seconds) + ".png"
        plt.savefig(savename, pad_inches=0, bbox_inches='tight')
        print("Movie barcode saved as '" + savename)

    return fig


file = "/Users/michael/Desktop/Lord.Of.The.Rings.The.Two.Towers.2002.720p.BrRip.264.YIFY.mp4"
print("average")
barcode(file, "average", n_seconds=30,
        bar_width=1, stop=1, save_fig=True)

print("squeeze")
barcode(file, "squeeze", n_seconds=30,
        bar_width=1, stop=1, save_fig=True)
