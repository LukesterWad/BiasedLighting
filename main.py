from Zone import Zone

# Settings provided by the user.
# In future, these will be read from a configuration file.
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
HORIZONTAL_ZONE_COUNT = 8
VERTICAL_ZONE_COUNT = 5

# Lists of light indexes along each edge.
TOP_LIGHTS = (15, 14, 13, 12, 11, 10, 9, 8, 7, 6)
BOTTOM_LIGHTS = (22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
LEFT_LIGHTS = (16, 17, 18, 19, 20, 21)
RIGHT_LIGHTS = (5, 4, 3, 2, 1, 0)


# Get the values associated with zone spacing.
# This is written as a function as it is required for both axes.
def getAxisValues(axis_length, zone_count) -> tuple[int, int]:
    remaining_space = axis_length % zone_count
    if zone_count == 1:  # Avoid division by zero.
        basal_gap = 0
    else:
        basal_gap = remaining_space // (zone_count - 1)
        remaining_space = remaining_space % (zone_count - 1)
    return (
        basal_gap,
        remaining_space
    )


# Get a list of zone objects that represents the entire screen border.
def makeZones() -> list[Zone]:
    zone_width = SCREEN_WIDTH // HORIZONTAL_ZONE_COUNT
    zone_height = SCREEN_HEIGHT // VERTICAL_ZONE_COUNT

    zones = []

    for edge in ("top", "bottom", "left", "right"):
        # Choose the right values for the horizontal and vertical axes.
        if edge in ("top", "bottom"):
            screen_length = SCREEN_WIDTH
            zone_count = HORIZONTAL_ZONE_COUNT
            zone_length = zone_width
        else:
            screen_length = SCREEN_HEIGHT
            zone_count = VERTICAL_ZONE_COUNT
            zone_length = zone_height
        basal_gap, remaining_space \
            = getAxisValues(screen_length, zone_count)

        # Select the correct list of lights for the current edge.
        lights = list({
            "top": TOP_LIGHTS,
            "bottom": BOTTOM_LIGHTS,
            "left": LEFT_LIGHTS,
            "right": RIGHT_LIGHTS,
        })

        a0 = 0  # Starting variable for position along the axis.
        for index in range(zone_count):
            a1 = a0 + zone_length - 1

            if edge == "top":
                x0 = a0
                y0 = 0
                x1 = a1
                y1 = zone_height - 1
            elif edge == "bottom":
                x0 = a0
                y0 = SCREEN_HEIGHT - zone_height
                x1 = a1
                y1 = SCREEN_HEIGHT - 1
            elif edge == "left":
                x0 = 0
                y0 = a0
                x1 = zone_width - 1
                y1 = a1
            elif edge == "right":
                x0 = SCREEN_WIDTH - zone_width
                y0 = a0
                x1 = SCREEN_WIDTH - 1
                y1 = a1

            zone = Zone(x0, y0, x1, y1)

            zone_lights = []

            # Use -1 and +1 on either bound to account for inconsistent gap size from remaining_space.
            lower_light_bound = a0 - (basal_gap // 2) - 1
            upper_light_bound = a1 + (basal_gap // 2) + 1

            # Iterate through the lights on the current edge.
            for light_index in range(len(lights)):
                # Check that the light isn't being used.
                if lights[light_index] != None:
                    light_position = \
                        (screen_length * (light_index+0.5)) / len(lights)
                    # If the light is approximately in the zone, append the light to the
                    # zone_lights list.
                    if light_position >= lower_light_bound and \
                            light_position <= upper_light_bound:
                        zone_lights.append(lights[light_index])
                        # Mark the zone as used so it isn't chosen by another zone.
                        # Otherwise, there could be conflicts from the bound adjustment
                        # used above.
                        lights[light_index] = None

            zone.setLights(tuple(zone_lights))
            zones.append(zone)

            gap = basal_gap
            # Add 1 to the gap where necessary to fill the axis with zones.
            if index < remaining_space:
                gap += 1

            # Set the staring value for the next zone along the axis.
            a0 = a1 + gap + 1

    return zones
