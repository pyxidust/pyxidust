# pyxidust library utils module
# Gabriel Peck 2023 (MIT license)

###############################################################################

# -------------
# MODULE INDEX:
# -------------

# pyxidust.utils.change_name()
# pyxidust.utils.clear_folder()
# pyxidust.utils.collapse_path()
# pyxidust.utils.file_parse()
# pyxidust.utils.get_letters()
# pyxidust.utils.get_metadata()
# pyxidust.utils.get_numbers()
# pyxidust.utils.get_time()
# pyxidust.utils.join_csv()
# pyxidust.utils.new_serial()
# pyxidust.utils.session_args()
# pyxidust.utils.session_in()
# pyxidust.utils.session_out()
# pyxidust.utils.trim_scale()
# pyxidust.utils.validate_serial()
# pyxidust.utils.validate_string()

###############################################################################

def change_name(extension, directory, serial_file):
    """Renames files in a folder via incremental serial numbers per a certain
    file extension.
    -----------
    PARAMETERS:
    -----------
    extension: str
        file extension to search for in the directory
    directory: path
        path to a directory containing files of a certain extension
    serial_file: path
        text file containing the starting serial number to increment
    ------
    USAGE:
    ------
    from pyxidust.utils import change_name
    change_name(extension='.jpg', directory=r'\\folder',
        serial_file=r'\\Serials.txt')
    """

    import os
    os.chdir(directory)

    with open(serial_file, 'r') as file:
        serial = int(file.read())

    for root, dirs, files in os.walk(directory):
        for photo in files:
            if photo.endswith(extension):
                serial += 1
                text = str(serial)
                os.rename(photo, f'{serial}{extension}')
                with open(serial_file, 'w') as file:
                    file.write(text)

###############################################################################

# needs tested...
def clear_folder(directory, option):
    """Removes all files or files/folders in a directory.
    -----------
    PARAMETERS:
    -----------
    directory: str
        path to a folder containing files/folders to be deleted
    option: str
        'all' - all files/folders in the directory will be deleted
        'files' - only files in the root of the directory will be deleted
    """
    import os
    import shutil
    for root, folders, files in os.walk(directory):
        if option == 'all':
            for folder in folders:
                shutil.rmtree(os.path.join(root, folder))
            for file in files:
                os.remove(os.path.join(root, file))
        if option == 'files':
            for file in files:
                os.remove(os.path.join(root, file))

###############################################################################

# needs tested...
def collapse_path(path):
    """Corrects the placement of slashes in WindowsOS network paths.
    -----------
    PARAMETERS:
    -----------
    path: str
        path to a network location
    """
    import os
    path = os.path.normpath(path)
    path = (rf'\{path}')
    return path

###############################################################################

# needs tested...
def file_parse(option, read_file, write_file=None, find_chars=None,
    replace_chars=None, split_chars=None):
    """Swiss Army knife for reading/writing files.
    -----------
    PARAMETERS:
    -----------
    option: str    
        '1' - read file/return contents
        '2' - read file/split at character/return contents
        '3' - read file/split at newlines/return contents
        '4' - read file/find/replace/split at character/return contents
        '5' - read file/find/replace/split at newlines/return contents
        '6' - read file/split at character/write to new file
        '7' - read file/split at newlines/write to new file
        '8' - read file/find/replace/split at character/write to new file
        '9' - read file/find/replace/split at newlines/write to new file
    read_file: str
        path to a .txt file to read-in to memory
    write_file: str
        path to a .txt file to write the results to
    find_chars: str
        string to be replaced in find/replace operations
    replace_chars: str
        string to replace the find_chars value
    split_chars: str
        string to indicate where the text from the read_file will be broken at
    ------
    USAGE:
    ------    
    file_parse('1','text.txt')
    file_parse('2','text.txt',split_chars=',')
    file_parse('3','text.txt')
    file_parse('4','text.txt',find_chars='s',replace_chars='#',split_chars=',')
    file_parse('5','text.txt',find_chars='s',replace_chars='#')
    file_parse('6','text.txt',write_file='output.txt',split_chars=',')
    file_parse('7','text.txt',write_file='output.txt')
    file_parse('8','text.txt',write_file='output.txt',find_chars='s',
        replace_chars='#',split_chars=',')
    file_parse('9','text.txt',write_file='output.txt',find_chars='s',
        replace_chars='#')
    """

    # read file/return contents
    if option == '1':
        with open(read_file, 'r') as file:
            text = file.read()
        return text

    # read file/split at character/return contents
    if option == '2':
        with open(read_file, 'r') as file:
            text = file.read().split(split_chars)
        return text
    
    # read file/split at newlines/return contents
    if option == '3':
        with open(read_file, 'r') as file:
            text = file.read().splitlines()
        return text
    
    # read file/find/replace/split at character/return contents
    if option == '4':
        with open(read_file, 'r') as file:
            text = file.read().replace(find_chars, replace_chars).split(split_chars)
        return text
    
    # read file/find/replace/split at newlines/return contents
    if option == '5':
        with open(read_file, 'r') as file:
            text = file.read().replace(find_chars, replace_chars).splitlines()
        return text
    
    # read file/split at character/write to new file
    if option == '6':
        with open(read_file, 'r') as file:
            text = file.read().split(split_chars)
        with open(write_file, 'w+') as file:
            for i in text:
                file.write(i)
                file.write('\n')
        return text
    
    # read file/split at newlines/write to new file
    if option == '7':
        with open(read_file, 'r') as file:
            text = file.read().splitlines()
        with open(write_file, 'w+') as file:
            for i in text:
                file.write(i)
                file.write('\n')
        return text
    
    # read file/find/replace/split at character/write to new file
    if option == '8':
        with open(read_file, 'r') as file:
            text = file.read().replace(find_chars, replace_chars).split(split_chars)
        with open(write_file, 'w+') as file:
            for i in text:
                file.write(i)
                file.write('\n')
        return text
    
    # read file/find/replace/split at newlines/write to new file
    if option == '9':
        with open(read_file, 'r') as file:
            text = file.read().replace(find_chars, replace_chars).splitlines()
        with open(write_file, 'w+') as file:
            for i in text:
                file.write(i)
                file.write('\n')
        return text

###############################################################################

def get_letters(string):
    """Infinite generator that yields unique letter combinations for file
    operations that do not support numbers.
    -----------
    PARAMETERS:
    -----------
    string: str
        Base string that will have a unique letter combination appended;
        yields a unique filename combination with each iteration; include
        an underbar for readability if desired
        (A, B, ..., _AA, _BB, ...)
    ------
    USAGE:
    ------
    from pyxidust.utils import get_letters
    generator = get_letters(string='filename_')
    next(generator) -> 'filename_A'
    next(generator) -> 'filename_B'
    """

    from string import ascii_uppercase as UPPER

    loops = 1
    while loops > 0:
        for letter in UPPER:
            text = (f'{string}{letter * loops}')
            yield text
            if letter.startswith('Z'):
                loops += 1

###############################################################################

def get_metadata(extension, directory):
    """Crawls a directory and returns metadata per a certain file extension.
    -----------
    PARAMETERS:
    -----------
    extension: str
        file extension to search for in the directory
    directory: path
        path to a directory containing files of a certain extension
    ------
    USAGE:
    ------
    from pyxidust.utils import get_metadata
    get_metadata(extension='.jpg', directory=r'\\folder')
    """
    
    import datetime
    import os
    import pandas
    
    name = []
    path = []
    time = []
    
    catalog = (f'{directory}\\Catalog.csv')

    # loop through directory returning the fully qualified path name to a file
    # filtered by its extension
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                # get full path of file
                location = os.path.join(root, file)
                # write file path to list
                path.append(location)
                # write file name to list
                name.append(file)
                # get UNIX time in seconds elapsed
                unix_time = os.path.getmtime(location)
                # convert UNIX time to UTC time
                utc_time = datetime.datetime.utcfromtimestamp(unix_time)
                # write UTC time to list
                time.append(utc_time)
                # read name list into data frame
                df1 = pandas.DataFrame(name, columns=['FILE_NAME'])
                # read path list into data frame
                df2 = pandas.DataFrame(path, columns=['FILE_PATH'])
                # read time list into data frame
                df3 = pandas.DataFrame(time, columns=['LAST_MODIFIED'])
                # combine data frames 1-3
                df4 = pandas.concat([df1, df2, df3], axis='columns')
                # shift index to start at one during initial crawl
                # increment this index anytime you change file type
                # or directory location to maintain a global ID
                df4.index += 1
                # set global 'ID' field name
                df4.index.name = 'ID'
                # write output to file
                df5 = df4.to_csv(catalog)

###############################################################################

def get_numbers(string):
    """Infinite generator that yields unique number combinations for file
    operations that do not support letters.
    -----------
    PARAMETERS:
    -----------
    string: str
        Base string that will have a unique number combination appended;
        yields a unique filename combination with each iteration; include
        an underbar for readability if desired
        (1, 2, ..., _3, _4, ...)
    ------
    USAGE:
    ------
    from pyxidust.utils import get_numbers
    generator = get_numbers(string='filename_')
    next(generator) -> 'filename_1'
    next(generator) -> 'filename_2'
    """

    count = 1
    while count > 0:
        text = (f'{string}{str(count)}')
        yield text
        count += 1

###############################################################################

# needs tested...
def get_time(option):
    """Get current timestamp and convert to desired type and format.
    -----------
    PARAMETERS:
    -----------
    option: str
        '1' - return two previous years (YYYY, YYYY)
        '2' - return date/time (MM/DD/YY, HH:MM:SS)
        '3' - return date/time pretty version
        '4' - return current date as one string (MMDDYY)
    -----------
    time.strftime() formatting reference:
    %a - short day name (Wed)
    %A - long day name (Wednesday)
    %b - short month name (Oct)
    %B - long month name (October)
    %c - short date/time (Wed Oct 12 10:13:46 2022)
    %d - day of the month (12)
    %H - hour in 24-hour format (10)
    %I - hour in 12-hour format (10)
    %j - day of the year in 365-format (285)
    %m - month of the year (10)
    %M - minute (13)
    %p - noon position (AM)
    %S - second (46)
    %U - week of the year first day Sunday (41)
    %w - day of the week (3)
    %W - week of the year first day Monday (41)
    %x - day/month/year (10/12/22)
    %X - hours/minutes/seconds (10:13:46)
    %y - short year (22)
    %Y - long year (2022)
    %z - time zone offset from UTC/GMT in +/-HHMM (-0400)
    %Z - time zone name (Eastern Daylight Time)
    """

    # required modules
    import time

    # current time per logged-on user request
    current = time.localtime()

    if option == '1':
        # return current time as YYYY
        timestamp = int(time.strftime('%Y', current))
        # return values for the last two years
        (year_one, year_two) = str(timestamp - 1), str(timestamp - 2)
        # return values to user
        return year_one, year_two

    if option == '2':
        # return current time as MM/DD/YY,HH:MM:SS
        timestamp = time.strftime('%m/%d/%y,%H:%M:%S', current)
        # return values to user
        return timestamp

    if option == '3':
        # suffix dictionary
        suffixes = {'st': (1, 21, 31), 'nd': (2, 22), 'rd': (3, 23),
        'th': (4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
        19, 20, 24, 25, 26, 27, 28, 29, 30)}
        # get current day as day of the month
        day = int(time.strftime('%d'))
        # loop values; then loop tuples
        for key, value in suffixes.items():
            for i in value:
                if day == i:
                    suffix = key
        # return current time as HH:MM AM/PM, long day, long month, day of the
        # month, # suffix, YYYY
        string1 = time.strftime('%I:%M %p, %A, %B %d', current)
        string2 = time.strftime(', %Y', current)
        timestamp = (f'{string1}{suffix}{string2}')
        # return values to user
        return timestamp

    if option == '4':
        # return current time as MMDDYY
        timestamp = time.strftime('%m%d%y', current)
        # return values to user
        return timestamp

###############################################################################

# needs tested...
def join_csv(directory, join_file):
    """Reads multiple .csv files from a directory and joins them based on a
    global ID field.
    -----------
    PARAMETERS:
    -----------
    directory: str
        folder structure containing the .csv files to merge/join
    join_file: str
        output file from the get_metadata() function that contains file
        metadata information to join to each global ID in the .csv files located in the directory; the join_file should be located in a separate directory from the directory variable to ensure it is not parsed in the os.walk loop
    ------
    USAGE:
    ------
    get_metadata('.mxd', r'\\folder')
    join_csv(r'\\folder1', r'\\folder2\\.csv')
    """
    
    # required modules
    import os
    import glob
    import pandas
    from pandas import concat, merge, read_csv
    
    # enter directory
    os.chdir(directory)
    
    # start file naming suffix
    counter = 0
    
    # loop through directory returning the
    # fully qualified path name to a file
    # filtered by its extension
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                # increment file name suffix
                counter += 1
                # file metadata
                df_info = read_csv(join_file, ',', index_col='ID')
                # mxd layers
                df_layers = read_csv(file, '|', index_col='ID')
                # join mxd layers to file metadata via global ID
                df_merge = merge(df_layers, df_info, how='left', on=None,
                    left_on='ID', right_on='ID')
                # output joined data to .csv
                df_merge.to_csv(f'{directory}\\LayersJoined{counter}.csv')
                # delete mxd layer files
                os.remove(file)
    
    # fully qualified paths to joined files with wildcard suffix
    file_paths = os.path.join(directory, 'LayersJoined*.csv')
    # create list of joined file paths
    file_list = glob.glob(file_paths)
    # combine all joined files into one pandas dataframe
    df_joined = concat(map(read_csv, file_list), ignore_index=True)
    # output final product to .csv
    df_joined.to_csv(f'{directory}\\JoinedCatalog.csv')

###############################################################################

def new_serial(serial_file, serial_number=None):
    """With systems that implement a serial number for record ID, compares user
    input to a .txt file containing a base serial number and increments the
    user input accordingly.
    -----------
    PARAMETERS:
    -----------
    serial_file: path
        Fully-qualified/raw file path to a .txt file containing one-line of
        text representing a base serial number in format 'YYYYRRRR' where
        'YYYY' is the four-digit year and 'RRRR' is the global ID.
    serial_number: str
        Serial number in format 'YYYYRRRR' or 'YYYYRRRR-CCCC' where 'YYYY' is
        the four-digit year, 'RRRR' is the global ID, and 'CCCC' is a counter
        for multiple records belonging to the same project. If serial_number
        is equal to None, a new serial number will be generated using the base
        number in the .txt file. Supports '-0000' counter values up to 9999. At
        9999, a new serial number will be generated using a '-0001' suffix.
    ------
    USAGE:
    ------
    from pyxidust.utils import new_serial
    new_serial(serial_file=r'\\.txt', serial_number='20231234-0001')
    """

    from pyxidust.gui import launch_message
    from pyxidust.utils import validate_serial

    def _get_serial(serial_file):
        """Read/increment serial number in nested scope."""
        with open(serial_file, 'r') as file:
            serial_base = str(int(file.read()) + 1)
        return serial_base

    if serial_number == None:
        serial_base = _get_serial(serial_file)
        with open(serial_file, 'w+') as file:
            file.write(serial_base)
        serial_new = (f'{serial_base}-0001')

    # validate user input
    if serial_number != None:
        validate_serial(string=serial_number)

    # increment base serial number
    if serial_number != None and len(serial_number) == 8:
        serial_new = (f'{serial_number}-0001')

    # increment '-' serial number
    elif serial_number != None and len(serial_number) == 13:
        base, suffix = serial_number.split('-')
        suffix_int = (int(suffix)) + 1
        suffix_new = str(suffix_int).zfill(4)
        if suffix_int > 9999:
            serial_base = _get_serial(serial_file)
            with open(serial_file, 'w+') as file:
                file.write(serial_base)
            serial_new = (f'{serial_base}-0001')
        else:
            serial_new = (f'{base}-{suffix_new}')

    return serial_new

###############################################################################

# needs tested...
def session_args(*args, **kwargs):
    """Creates a dictionary of arguments.
    ------
    USAGE:
    ------
    args = session_args(name, number, ...)
    session_out(arguments=args, session_data=r'.csv')
    """
    return locals()

###############################################################################

# needs tested...
def session_in(session_data):
    """Reads results from previous session and returns as a tuple.
    -----------
    PARAMETERS:
    -----------
    session_data: str
        path to a .csv file that contains stored values from session_out()
    ------
    USAGE:
    ------
    name, number = session_in(session_data=r'.csv')
    """
    import pickle
    arguments = pickle.load(open(session_data, 'rb'))
    for key, value in arguments.items():
        return value

###############################################################################

# needs tested...
def session_out(arguments, session_data):
    """Writes function results to bytes for use by next session.
    -----------
    PARAMETERS:
    -----------
    arguments: dict
        function results to persist to next session
    session_data: str
        path to a .csv file that will contain stored values for session_in()
    ------
    USAGE:
    ------
    args = session_args(name, number, ...)
    session_out(arguments=args, session_data=r'.csv')
    """
    import pickle
    pickle.dump(arguments, open(session_data, 'wb'))

###############################################################################

# needs tested...
def trim_scale(csv_in, csv_out, columns, index, scale):
    """Drops decimal places in floating point values to specified scale.
    -----------
    PARAMETERS:
    -----------
    csv_in: str
        path to the input .csv file; file will be deleted during execution
        which permits the same file path to be used for the csv_in and
        csv_out arguments
    csv_out:str
        path to the output .csv file
    columns: list
        values in the specified columns will be rounded to the specified scale
    index: str
        existing csv column name that acts as a unique identifier for rows
    scale: int
        decimal places will ve trimmed to this scale
    ------
    USAGE:
    ------
    trim_scale(csv_in=r'.csv', csv_out=r'.csv', columns=['x','y'],
        index='id', scale=2)
    """
    import os
    import pandas
    df = pandas.read_csv(filepath_or_buffer=csv_in, index_col=index)
    for column in columns:
        df[column] = df[column].apply(lambda x: round(x, scale))
    os.remove(csv_in)
    df.to_csv(csv_out)

###############################################################################

def validate_serial(string):
    """Enforces population of numeric characters in a serial number.
    -----------
    PARAMETERS:
    -----------
    string: str
        serial number in format 'YYYYRRRR' or 'YYYYRRRR-CCCC' where 'YYYY' is
        the four-digit year, 'RRRR' is the global ID, and 'CCCC' is a counter
        for multiple records belonging to the same project.
    ------
    USAGE:
    ------
    from pyxidust.utils import validate_serial
    validate_serial(string='20201234-0001')
    """

    from pyxidust.gui import launch_message

    def _check_numeric(value):
        """Standard character validation."""
        if any(i.isalpha() for i in value):
            error_message = (f'Serial number must not contain letters')
            launch_message('showinfo', 'ERROR:', error_message)
        elif any(i.isspace() for i in value):
            error_message = (f'Serial number cannot have spaces')
            launch_message('showinfo', 'ERROR:', error_message)
        elif any(i in SPECIAL for i in value):
            error_message = (f'Serial number cannot have special characters')
            launch_message('showinfo', 'ERROR:', error_message)
        else:
            pass

    def _format_error():
        """Error handling if user inputs serial # in wrong format."""
        error_message = (f'Serial # format is 00000000 or 00000000-0000')
        launch_message(option='showinfo', title='ERROR', message=error_message)

    # base serial
    if len(string) == 8:
        base = string
        _check_numeric(value=base)

    # base/counter serial
    elif len(string) == 13 and string.count('-') == 1 and string[8] == '-':
        base, suffix = string.split('-')
        _check_numeric(value=base)
        _check_numeric(value=suffix)

    # all other cases
    else:
        _format_error()

###############################################################################

# tested 9/27/2023
def validate_string(length, option, text):
    """Enforces length and character type standards in a string.
    Spaces and special characters are not permitted.
    -----------
    PARAMETERS:
    -----------
    length: str
        maximum number of characters to permit in string
    option: str
        'alpha' - permit letters only
        'numeric' - permit numbers only
        'alphanumeric' - permit letters and numbers
    text: str
        string value to be checked against the desired option
    """
    from string import punctuation as SPECIAL
    result = True
    if length < str(len(text)):
        result = False
    elif any(i.isspace() for i in text):
        result = False
    elif any(i in SPECIAL for i in text):
        result = False
    elif option == 'alpha':
        if any(i.isnumeric() for i in text):
            result = False
    elif option == 'numeric':
        if any(i.isalpha() for i in text):
            result = False
    return result, text

###############################################################################
