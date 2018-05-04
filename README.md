# RegularExpressionSample
Implement a simple general purpose aggregator <br/>

Usage: aggregator.py filename topic <br/>
filename: input file that contains a list of the online sources (urls). <br/>
topic:  topic to be researched and reported on <br/>

In order to find the matched keyword in the website page, a regex pattern is <br/>
used to identify inner html values within the closing '>' and '<' tags. In <br/>
other words, this aggregator default regex disregards any attributes of the <br/>
html tag. To change the default pattern, specify a new regex pattern pattern <br/>
in the 'find_matches' function. <br/>

After all matches for each url is aggregated, they are formatted to print out <br/>
to a file. Each url entry is separated by a line break decor. To change <br/>
the default format and line break, specify the parameters in the 'format_list' <br/>
function. <br/>
