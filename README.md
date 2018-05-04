# RegularExpressionSample
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
