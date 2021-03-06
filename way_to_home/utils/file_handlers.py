"""This module implements helpers functions for work with files."""

import pickle
import csv
from zipfile import ZipFile, BadZipFile
import requests


def _get_fields_position(row_header, required_fields):
    """
    Return dictionary where the keys are required fields and
    values are numbers of columns with the appropriate name.
    """
    fields_position = {}
    for field in required_fields:
        fields_position[field] = row_header.index(field)

    return fields_position


def unzip_file(path_to_file, unzip_to='./'):
    """Unzip file to directory with path `unzip_to`."""
    try:
        with ZipFile(path_to_file, 'r') as zip_file:
            try:
                zip_file.extractall(unzip_to)
            except (ValueError, BadZipFile, PermissionError):
                return False
    except (FileNotFoundError, PermissionError):
        return False

    return True


def load_file(url, save_to='./'):
    """Download file from `url` to directory with path `save_to`."""
    file_name = url.split('/')[-1]

    request = requests.get(url)
    if not request.status_code == 200:
        return None

    try:
        with open(f'{save_to}/{file_name}', 'wb') as file:
            file.write(request.content)
            return file.name
    except PermissionError:
        pass


def parse_csv_file(path_to_file, required_fields):
    """Provide csv file parsing with the required fields."""
    parsed_data = []

    try:
        with open(path_to_file) as csv_file:
            try:
                csv_reader = csv.reader(csv_file, delimiter=',')
            except csv.Error:
                return None

            for row in csv_reader:
                if csv_reader.line_num == 1:
                    fields_position = _get_fields_position(row, required_fields)
                    continue

                item = {}
                for field, position in fields_position.items():
                    item[field] = row[position]

                parsed_data.append(item)

    except (FileNotFoundError, PermissionError):
        return None

    return parsed_data


def pickle_data(data, path_to_file):
    """Write a pickled representation of data to file."""
    with open(path_to_file, 'wb') as file:
        try:
            pickle.dump(data, file)
        except (pickle.PicklingError, PermissionError):
            return False

    return True


def unpickle_data(path_to_file):
    """Read a pickled representation of data from file."""
    try:
        with open(path_to_file, 'rb') as file:
            try:
                data = pickle.load(file)
            except pickle.UnpicklingError:
                return None
    except (FileNotFoundError, PermissionError):
        return None

    return data
