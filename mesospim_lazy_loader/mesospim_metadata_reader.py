import re
from datetime import datetime


def read(meta_filename):
    """Read mesoSPIM metadata into a dictionary, processing some field for
       ease of handling

    Purpose
    -------
    mesoSPIM metadata are stored in plain text files with a custom format that goes
    along these lines:

    [SECTION NAME]
    [some key] value
    [some_other_key] value

    So all section names and keys and square brackets and there is no consistency
    regarding whether or not these have underscores or spaces. This function
    converts everything to underscores. It also imports numeric values as numbers
    rather than strings. All dates are converted into a datetime object.


    Arguments
    ---------
    meta_filename : str
      Relative or absolute path to a mesoSPIM metadata file


    Outputs
    -------
    dictionary containing data processed from the metadata file

    """

    section_name = ""
    verbose = False
    out = {}

    with open(meta_filename, "r") as meta_file:
        while True:
            t_line = meta_file.readline()

            if not t_line:
                break

            t_line = t_line.rstrip()  # Strip trailing white space and new line

            # Skip empty lines
            if len(t_line) == 0:
                continue

            # Is the current line a heading?
            t_re = re.compile("\[(.*)\]$")
            matches = t_re.findall(t_line)
            if len(matches) > 0:
                section_name = tidy_string(matches[0])

            # Do not attempt to store data if we have not yet pulled in a section
            if len(section_name) == 0:
                continue

            t_re = re.compile("\[(.*)\] (.*)")
            matches = t_re.findall(t_line)

            if len(matches) == 0:
                continue

            # This line must therefore be a key/value pair
            key = tidy_string(matches[0][0])  # Tidy the key name
            value = matches[0][1]

            # Convert values to numbers if needed
            if (
                section_name == "POSITION"
                or section_name == "GALVO_PARAMETERS"
                or key.find("Pixelsize_") >= 0
                or key.find("etl_") >= 0
                or key.find("exposure") >= 0
                or key.find("line_interval") >= 0
                or key.find("_pixels") >= 0
                or key.find("_rate") >= 0
                or key.find("Intensity_") >= 0
            ):
                value = eval(value)

            # Convert times to datetime
            if key.find("Started_") >= 0 or key.find("Stopped_") >= 0:
                value = datetime.strptime(value, "%Y%m%d-%H%M%S")

            # If we are here, then we have a section and a key/value pair
            if verbose:
                print("%s.%s <- %s" % (section_name, key, value))

            # Add the values to the dictionary
            if section_name in out.keys():
                out[section_name].update({key: value})
            else:
                out[section_name] = {key: value}

    return out


def tidy_string(t_str):
    """Tidy strings by replacing spaces with underscores and removing colons

    Purpose
    -------
    Some section names and keys in the mesoSPIM config file contain spaces, which
    is annoying. This function replaces those with underscores. In addition there
    was one key in older versions of the acquisition software that contained a ":".
    This is also stripped out here.


    Arguments
    ---------
    t_str : str
       String to process


    Outputs
    -------
    Processed string

    """

    t_str = t_str.replace(" ", "_")
    t_str = t_str.replace(":", "")

    return t_str
