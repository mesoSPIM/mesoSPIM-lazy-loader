import os

import dask.array
from tifffile import tifffile

from mesospim_lazy_loader import utils


def mesoSPIM_sample_read_dir(path):
    """mesoSPIM reader conribution

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.
    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, str) and utils.is_mesoSPIM_dir(path):
        print("Found mesoSPIM data")
        return reader_function
    else:
        return None


def reader_function(path):
    """
    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.
    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.
    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of layer.
        Both "meta", and "layer_type" are optional. napari will default to
        layer_type=="image" if not provided
    """

    print("Loading mesoSPIM stacks from directory")

    layers = []
    files = utils.return_mesoSPIM_files_in_path(path)

    if len(files) == 0:
        return layers

    for t_file in files:
        # Create a dask array for this file
        full_fname = os.path.join(
            t_file["absolute_path_to_file"], t_file["image_file_name"]
        )
        zarr_store = tifffile.imread(full_fname, aszarr=True)
        data = dask.array.from_zarr(zarr_store)

        layers.append(
            (
                data,
                {
                    "name": t_file["image_file_name"],
                    "rgb": False,
                    "blending": "additive",
                    "colormap": utils.laser_wavelength_to_colormap(
                        t_file["meta_data"]["CFG"]["Laser"]
                    ),
                    "contrast_limits": [0, 2**13],
                },
                "image",
            )
        )

    return layers
