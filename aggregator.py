# -----------------------------------------------------------------------------
# Name:        aggregator.py
# Purpose:     Implement a simple general purpose aggregator
#
# Author:   Zaw Mai (20005349)
# Date:     Nov 29, 2017
# -----------------------------------------------------------------------------
"""
Implement a simple general purpose aggregator

Usage: aggregator.py filename topic
filename: input file that contains a list of the online sources (urls).
topic:  topic to be researched and reported on

In order to find the matched keyword in the website page, a regex pattern is
used to identify inner html values within the closing '>' and '<' tags. In
other words, this aggregator default regex disregards any attributes of the
html tag. To change the default pattern, specify a new regex pattern pattern
in the 'find_matches' function.

After all matches for each url is aggregated, they are formatted to print out
to a file. Each url entry is separated by a line break decor. To change
the default format and line break, specify the parameters in the 'format_list'
function.

Note to self for future improvements. Instead formatting a huge string to
be written to file. An implementation of formatting found matches per url and
then writing to file line by line could be more memory efficient. A performance
study would be insightful.

Reference to default constants:
default_format_string = "Source url: {}\n\n{}\n{}\n\n"
default_regex_pattern = r">([^<>]*\b{}\b[^<>]*)<"
default_line_break_decor = '-------------------------------------------------'
"""

import urllib.request
import urllib.error
import re
import sys

DEFAULT_FORMAT_STRING = "Source url: {}\n\n{}\n{}\n\n"
DEFAULT_REGEX_PATTERN = r">([^<>]*\b{}\b[^<>]*)<"
DEFAULT_LINE_BREAK_COLOR = '-------------------------------------------------'


def read_web_page(url):
    """
    Read and decode a web page from the given url address.

    Arguments:
    url(string): web address

    Returns:
    html web page(string): utf-8 decoded string form of a requested web page
    """
    page = None
    try:
        with urllib.request.urlopen(url) as url_file:
            page = url_file.read().decode('utf-8')
    except urllib.error.URLError as url_error:
        print("Error opening url: ", url, url_error)
    except UnicodeDecodeError as decode_error:
        print("Error decoding url: ", url, decode_error)
    finally:
        return page


def write_to_file(data, filename):
    """
    Write content 'data' to the specified file path.

    Arguments:
    data(string):
    filename(string): destination file path to write out to
    """
    with open(filename, 'w', encoding='utf-8') as out_file:
        out_file.write(data)


def find_matches(text, keyword, pattern=DEFAULT_REGEX_PATTERN):
    """
    Find all matches that contains the keyword and meets the regex pattern
    criteria.

    Arguments:
    text(string): text to search
    keyword(string): target word to match
    pattern(raw string): regex pattern

    Returns:
    List of string containing matches. Otherwise, None.
    """
    search_pattern = pattern.format(keyword)
    return re.findall(search_pattern, text, re.IGNORECASE | re.DOTALL)


def reader(filename):
    """
    Returns a generator object to reader over line by line of a text file.
    Each iteration returns a string that is stripped of trailing whitspace.

    Arguments:
    filename(string): file path

    Returns:
    Generator Object (iterator)
    """
    with open(filename, 'r', encoding='utf-8') as source_file:
        for url_line in source_file:
            yield url_line.rstrip()
        yield None


def format_list(list_data,
                format_string=DEFAULT_FORMAT_STRING,
                line_break=DEFAULT_LINE_BREAK_COLOR):
    """
    Returns a string of formatted list elements. Each list element are
    formatted sequentially with 'format_string'. Then, line break comes after.
    Each list element is a list contains the following:
        1) A string to specify url
        2) List of strings

    Arguments:
    list_data(list of string lists): List of elements to format
    format_string(string): Format expression for each element
    line_break(string): Decoration to separate each element in the string

    Returns:
    Formatted string containing all list elements
    """
    text = ''
    for entry in list_data:
        body = ''
        source = entry[0]
        for match in entry[1]:
            body = body + match + "\n"
        body = body.rstrip()
        text = text + format_string.format(source,body,line_break)
    return text


def aggregate(filename, keyword, func=find_matches):
    """
    Returns an aggregated set of string matches for each url in the
    the source file specified by the path 'filename.'

    Arguments:
    filename(string): source file path
    keyword(string): target search string
    func(function): function to find matches

    Returns:
    Formatted string with all founds matches for each url in source file
    """
    aggregated_data = list()
    url_reader = reader(filename)
    url_string = next(url_reader)
    while url_string:
        text = read_web_page(url_string)
        if text:
            match_string_list = func(text, keyword)
            if match_string_list:
                entry = [url_string, match_string_list]
                aggregated_data.append(entry)
        url_string = next(url_reader)

    return aggregated_data


def main():
    if len(sys.argv) != 3:
        print("Error: invalid number of arguments")
        print('usage: aggregator.py filename topic')
    else:
        source_file_path = sys.argv[1]
        keyword = sys.argv[2]
        data = aggregate(source_file_path, keyword)
        data = format_list(data)
        destination_path = "{}summary.txt".format(keyword)
        write_to_file(data, destination_path)


if __name__ == '__main__':
    main()
