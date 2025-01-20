import datetime
import cv2
from PIL import ImageGrab
import numpy as np
from .input_control import *

"""
Color Matching Functions
"""


def get_point_color(point):
    """
    Get the color of a specific point on the screen.

    Parameters:
        point (tuple): Coordinates of the point (x, y).

    Returns:
        np.ndarray: RGB values of the pixel at the specified point.
    """
    img = grab_rect_to_cv2(None, if_gray=False)
    img = np.array(img)
    pixel_color = img[point[1], point[0], :3]
    return pixel_color


def match_point(point, color, tolerance=(10, 10, 10), region=None):
    """
    Match the color of a specific point within a given tolerance.

    Parameters:
        point (tuple): Coordinates of the point (x, y).
        color (tuple): RGB color to match.
        tolerance (tuple): Tolerance for each color channel (default is (10, 10, 10)).
        region (tuple, optional): Region to grab (x1, y1, x2, y2). Default is None for full screen.

    Returns:
        bool: True if the color matches, False otherwise.
    """
    img = grab_rect_to_cv2(region, if_gray=False)
    img = np.array(img)
    pixel_color = img[point[1], point[0], :3]
    tolerance = np.array(tolerance)
    lower_bound = color - tolerance
    upper_bound = color + tolerance
    return np.all(lower_bound <= pixel_color) and np.all(pixel_color <= upper_bound)


def match_points(region, base_color, tolerance, *offset_colors):
    """
    Match a series of colors starting from a base color and offsets.

    Parameters:
        region (tuple): Region to search in (x1, y1, x2, y2).
        base_color (tuple): Base RGB color.
        tolerance (tuple): Tolerance for each color channel.
        offset_colors (list): List of tuples with offsets and colors [(offset, color)].

    Returns:
        tuple: Coordinates of the first matching position, or [0, 0] if not found.
    """
    result = [0, 0]
    img = grab_rect_to_cv2(region, if_gray=False)
    height, width, _ = img.shape
    rgb_values = img
    base_color = np.array(base_color)
    tolerance = np.array(tolerance)
    matches = np.all(np.abs(rgb_values - base_color) <= tolerance, axis=-1)
    for y, x in zip(*np.where(matches)):
        matched = True
        for offset, color in offset_colors:
            color = np.array(color)
            dx, dy = offset
            new_x, new_y = x + dx, y + dy
            if not (0 <= new_x < width and 0 <= new_y < height):
                matched = False
                break
            if not np.all(np.abs(rgb_values[new_y, new_x] - color) <= tolerance):
                matched = False
                break
        if matched:
            return (x + region[0], y + region[1])
    return result


def match_all_points(region, base_color, tolerance, *offset_colors):
    """
    Match all points that satisfy the color and offset criteria.

    Parameters:
        region (tuple): Region to search in (x1, y1, x2, y2).
        base_color (tuple): Base RGB color.
        tolerance (tuple): Tolerance for each color channel.
        offset_colors (list): List of tuples with offsets and colors [(offset, color)].

    Returns:
        list: List of all matching coordinates, or [[0, 0]] if none are found.
    """
    result = []
    img = grab_rect_to_cv2(region, if_gray=False)
    height, width, _ = img.shape
    rgb_values = img
    base_color = np.array(base_color)
    tolerance = np.array(tolerance)
    matches = np.all(np.abs(rgb_values - base_color) <= tolerance, axis=-1)
    for y, x in zip(*np.where(matches)):
        matched = True
        for offset, color in offset_colors:
            color = np.array(color)
            dx, dy = offset
            new_x, new_y = x + dx, y + dy
            if not (0 <= new_x < width and 0 <= new_y < height):
                matched = False
                break
            if not np.all(np.abs(rgb_values[new_y, new_x] - color) <= tolerance):
                matched = False
                break
        if matched:
            result.append([x + region[0], y + region[1]])
    if not result:
        return [[0, 0]]
    return result
# Wait for a specific color
def wait_for_color(pos, rgb, cast=(10, 10, 10), rect=None):
    while not match_point(pos, rgb, cast, rect):
        continue


# Wait for a specific color to disappear
def wait_no_color(pos, rgb, cast=(10, 10, 10), rect=None):
    while match_point(pos, rgb, cast, rect):
        continue


"""
Image Processing Functions
"""


def grab_rect(rect=None):
    """
    Capture a screenshot and return it as an image object.

    Parameters:
        rect (tuple, optional): The region to capture (x1, y1, x2, y2). Default is None for full screen.

    Returns:
        PIL.Image.Image: The captured image.
    """
    if rect is None:
        return ImageGrab.grab()
    return ImageGrab.grab(rect)


def grab_rect_to_cv2(rect=None, if_gray=True):
    """
    Capture a screenshot and convert it to an OpenCV-compatible format.

    Parameters:
        rect (tuple, optional): The region to capture (x1, y1, x2, y2). Default is None for full screen.
        if_gray (bool): Whether to return a grayscale image. Default is True.

    Returns:
        np.ndarray: The captured image in OpenCV format.
    """
    img = grab_rect(rect)
    img_np = np.array(img)
    if not if_gray:
        return img_np
    return cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY).astype('uint8')


def grab_rect_and_save(path, img_name=None, rect=None, format='jpg'):
    """
    Capture a screenshot and save it to a specified path.

    Parameters:
        path (str): The directory where the image will be saved.
        img_name (str, optional): The name of the image file. Defaults to "screenshot_<timestamp>".
        rect (tuple, optional): The region to capture (x1, y1, x2, y2). Defaults to full screen.
        format (str): The image format, e.g., 'jpg' or 'png'. Default is 'jpg'.

    Returns:
        None
    """
    img = grab_rect(rect)
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if img_name is None:
        img_name = f"screenshot_{current_datetime}.{format}"
    else:
        img_name = f"{img_name}.{format}"
    img.save(f"{path}/{img_name}")


def rect_match_sqdiff(big_img_path: str, threshold=0.05, rect=None):
    """
    Perform template matching using the TM_SQDIFF_NORMED method, suitable for precise matching.

    Parameters:
        big_img_path (str): Path to the large image.
        threshold (float): Matching threshold (default 0.05). Lower values are stricter.
        rect (tuple, optional): Region of the screen to capture as a template.

    Returns:
        float: Matching accuracy, or 0 if the match fails.
    """
    small_img = grab_rect_to_cv2(rect)
    big_img = cv2.imread(big_img_path, 0)
    result = cv2.matchTemplate(small_img, big_img, cv2.TM_SQDIFF_NORMED)
    min_val = cv2.minMaxLoc(result)[0]
    if min_val <= threshold:
        return min_val
    return 0


def rect_match_ccoeff(big_img_path: str, threshold=0.8, rect=None):
    """
    Perform template matching using the TM_CCOEFF_NORMED method, suitable for broader matching.

    Parameters:
        big_img_path (str): Path to the large image.
        threshold (float): Matching threshold (default 0.8). Higher values are stricter.
        rect (tuple, optional): Region of the screen to capture as a template.

    Returns:
        float: Matching accuracy, or 0 if the match fails.
    """
    small_img = grab_rect_to_cv2(rect)
    big_img = cv2.imread(big_img_path, 0)
    result = cv2.matchTemplate(small_img, big_img, cv2.TM_CCOEFF_NORMED)
    max_val = cv2.minMaxLoc(result)[1]
    if max_val >= threshold:
        return max_val
    return 0


def find_img_low_threshold(img_path: str, rect=None, threshold=0.05):
    """
    Search the screen for an image and return its coordinates if found (low threshold).

    Parameters:
        img_path (str): Path to the image to search for.
        rect (tuple, optional): Region of the screen to search in.
        threshold (float): Matching threshold (default 0.05).

    Returns:
        list: Coordinates [x, y] of the found image or [0, 0] if not found.
    """
    img = grab_rect_to_cv2(rect)
    template = cv2.imread(img_path, 0)
    height, width = template.shape
    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
    min_val = cv2.minMaxLoc(result)[0]
    pos = [0, 0]
    if min_val <= threshold:
        upper_left = cv2.minMaxLoc(result)[2]
        lower_right = (upper_left[0] + width, upper_left[1] + height)
        avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))
        if rect is None:
            pos[0] = avg[0]
            pos[1] = avg[1]
        else:
            pos[0] = avg[0] + rect[0]
            pos[1] = avg[1] + rect[1]
    return pos


def find_all_img_low_threshold(img_path: str, rect=None, threshold=0.05):
    """
    Search the screen for all occurrences of an image (low threshold) and return their coordinates.

    Parameters:
        img_path (str): Path to the image to search for.
        rect (tuple, optional): Region of the screen to search in.
        threshold (float): Matching threshold (default 0.05).

    Returns:
        list: List of coordinates [[x1, y1], [x2, y2], ...] of the found images, or an empty list if none are found.
    """
    img = grab_rect_to_cv2(rect)
    template = cv2.imread(img_path, 0)
    height, width = template.shape
    result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
    matches = []

    while True:
        min_val, _, min_loc, _ = cv2.minMaxLoc(result)
        if min_val > threshold:
            break

        upper_left = min_loc
        lower_right = (upper_left[0] + width, upper_left[1] + height)
        avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))

        if rect is None:
            pos = [avg[0], avg[1]]
        else:
            pos = [avg[0] + rect[0], avg[1] + rect[1]]

        matches.append(pos)

        # Black out the matched region to avoid detecting it again
        cv2.rectangle(img, upper_left, lower_right, (0, 0, 0), -1)

        # Recalculate the result for the next match
        result = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)

    return matches


def find_img_high_threshold(img_path: str, rect=None, threshold=0.8):
    """
    Search the screen for an image and return its coordinates if found (high threshold).

    Parameters:
        img_path (str): Path to the image to search for.
        rect (tuple, optional): Region of the screen to search in.
        threshold (float): Matching threshold (default 0.8).

    Returns:
        list: Coordinates [x, y] of the found image or [0, 0] if not found.
    """
    img = grab_rect_to_cv2(rect)
    template = cv2.imread(img_path, 0)
    height, width = template.shape
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    max_val = cv2.minMaxLoc(result)[1]
    pos = [0, 0]
    if max_val >= threshold:
        upper_left = cv2.minMaxLoc(result)[3]
        lower_right = (upper_left[0] + width, upper_left[1] + height)
        avg = (int((upper_left[0] + lower_right[0]) / 2), int((upper_left[1] + lower_right[1]) / 2))
        if rect is None:
            pos[0] = avg[0]
            pos[1] = avg[1]
        else:
            pos[0] = avg[0] + rect[0]
            pos[1] = avg[1] + rect[1]
    return pos


def find_img_pyautogui(img_path, rect=None, confidence=0.9):
    """
    Use pyautogui to find an image on the screen.

    Parameters:
        img_path (str): Path to the image to search for.
        rect (tuple, optional): Region of the screen to search in.
        confidence (float): Confidence threshold for the match (default 0.9).

    Returns:
        Box: Bounding box of the found image, or None if not found.
    """
    if rect is None:
        return pyautogui.locateOnScreen(img_path, confidence=confidence)
    return pyautogui.locateOnScreen(img_path, confidence=confidence, region=rect)


def if_image_exists(image_path: str, threshold=0.05):
    """
    Check if an image exists on the screen using the TM_SQDIFF_NORMED method.

    Parameters:
        image_path (str): Path to the image to search for.
        threshold (float): Matching threshold (default 0.05).

    Returns:
        bool: True if the image exists, False otherwise.
    """
    return rect_match_sqdiff(image_path, threshold)


def click_image(image_path, threshold=0.05, delay=1):
    """
    Click on the center of an image if found on the screen.

    Parameters:
        image_path (str): Path to the image to search for.
        threshold (float): Matching threshold (default 0.05).
        delay (int): Delay in seconds after clicking (default 1).

    Returns:
        None
    """
    pos = find_img_low_threshold(image_path, threshold=threshold)
    if pos != [0, 0]:
        click(pos)
        time.sleep(delay)


def wait_for_image(image_path: str, threshold=0.05, duration=0.1, delay=1):
    """
    Wait for an image to appear on the screen.

    Parameters:
        image_path (str): Path to the image to search for.
        threshold (float): Matching threshold (default 0.05).
        duration (float): Time in seconds between checks (default 0.1).
        delay (int): Time in seconds to wait after the image appears (default 1).

    Returns:
        None
    """
    while True:
        if rect_match_sqdiff(image_path, threshold):
            time.sleep(delay)
            break
        time.sleep(duration)
