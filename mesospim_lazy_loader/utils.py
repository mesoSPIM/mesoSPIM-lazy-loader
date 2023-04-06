def laser_wavelength_to_colormap(laser_wavelength):
    """Convert a laser wavelength to a napari colormap name

    Purpose
    -------
    We wish to automatically color-code channels as they are loaded
    into napari. For this purpose will will (simplistically) map
    laser line names to a colormap name.


    Arguments
    ---------
    laser_wavelength : str
       This is a string defining the laser wavelength. e.g. '647 nm'


    Output
    ------
    String that defines a napari colormap name. e.g. red
    """

    if laser_wavelength == "647 nm":
        colormap = "red"
    elif laser_wavelength == "561 nm":
        colormap = "green"
    elif laser_wavelength == "488 nm":
        colormap = "blue"
    elif laser_wavelength == "405 nm":
        colormap = "magenta"

    return colormap
