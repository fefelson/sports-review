

def adjust_color_for_readability(color, brightness_adjustment, saturation_adjustment, hue_adjustment):
    adjusted_color = (
        max(0, min(255, color[0] + brightness_adjustment)),
        max(0, min(255, color[1] + saturation_adjustment)),
        max(0, min(255, color[2] + hue_adjustment))
    )
    return adjusted_color

def adjust_readability(background_color, text_color, target_contrast=5, max_iterations=10):

    current_contrast = calculate_contrast_ratio(text_color, background_color)
    iterations = 0

    while current_contrast < target_contrast and iterations < max_iterations:
        # Determine which color is darker and adjust its brightness, saturation, and hue
        if brightness(background_color) > brightness(text_color):
            text_color = adjust_color_for_readability(text_color, -10, -5, 0)
            background_color = adjust_color_for_readability(background_color, 10, 5, 0)
        else:
            text_color = adjust_color_for_readability(text_color, +10, 5, 0)
            background_color = adjust_color_for_readability(background_color, -10, -5, 0)

        # Recalculate the contrast ratio
        current_contrast = calculate_contrast_ratio(text_color, background_color)
        iterations += 1

    return background_color, text_color

def brightness(color):
    # Calculate brightness using the formula: 0.299 * R + 0.587 * G + 0.114 * B
    return 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]


def hex_to_rgb(hex_color):
    # Convert hex color to RGB
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def adjust_gamma(color_component):
    color = color_component / 255.0
    if color <= 0.04045:
        return color / 12.92
    else:
        return ((color + 0.055) / 1.055) ** 2.4

def calculate_relative_luminance(color):
    r, g, b = color
    return 0.2126 * adjust_gamma(r) + 0.7152 * adjust_gamma(g) + 0.0722 * adjust_gamma(b)

def calculate_contrast_ratio(color1, color2):

    luminance1 = calculate_relative_luminance(color1)
    luminance2 = calculate_relative_luminance(color2)

    contrast_ratio = (max(luminance1, luminance2) + 0.05) / (min(luminance1, luminance2) + 0.05)
    return contrast_ratio
