# This file is used to generate the GldParser class
#
# Description of syntax of this file
#
# Parser directive
#	%CLASS GlmFile
#   %START entry_call(target)
#   %END finalization_call()
#
# Target definition
# target-name
#		: target-1 target-2 ... target-N
#			:: terminal-1
#			:: terminal-2
#			...
#			:: terminal-N
#
#   % 			specifies a parser directive (e.g., BASE, START, END)
#   #			specifies a command
#   ALLCAPS		specifies a new pattern name
#   "text"		specifies literal text
#   [pattern]	specifies list of characters
#   ?			specifies the last pattern occurs zero or one time only
#   *			specifies the last pattern occurs zero or more times
#   +			specifies the last pattern occurs one or more times
#   (pattern)   specifies an inline pattern substitution
#   call(list)	specifies a function call on the patterns matched
#   NEWLINE		ends the current specification
#	:			specify an terminal sequence
#	::			specify a terminal handler
#
# convert this file to C++ using the command
# 	% python glmparser.py glmparser.y
#

%CLASS glmparser
%BASE GlmFile
%START GLMFILE

NEWLINE 
	: [\n\r] NEWLINE

SPACE
	: [ \t\r\n\f]

WHITE
	: SPACE*

SPACES
	: SPACE+

ENDLINE
	: WHITE NEWLINE

FILEPATH
	: DQUOTE PATHNAME DQUOTE
	: QUOTE PATHNAME QUOTE
	: "[" URLNAME "]"
	: "<" PATHNAME ">"
	: "{" INLINETEXT "}"

PATHNAME
	: "/" PATHNAME
	: PATHNAME
	: FILENAME

FILENAME
	: [-A-Za-z0-9_.]+

URLNAME
	: URLPROTOCOL ":" URLSPEC
		:: load_url(URLPROTOCOL,URLSPEC)

URLPROTOCOL
	: [a-z]+

URLSPEC
	: [-/:_.A-Za-z0-9%+&?]+
	: URLSPEC ( "${" GLOBALNAME "}" ) URLSPEC

GLMFILE
	: WHITE "#" MACROEXPRESSION ENDLINE 
		:: process_macro(MACROEXPRESSION)
	: WHITE "module" FILENAME ";"
		:: load_module(FILENAME)
	: WHITE "clock" WHITE "{" PROPERTYLIST "}"
		:: load_clock(PROPERTYLIST)
	: WHITE "class" SPACES CLASSNAME  "{" <declaration-list> "}"
		:: create_class(CLASSNAME,<declaration-list>)
	: WHITE "object" SPACES CLASSNAME "{" PROPERTYLIST "}"
		:: create_object(CLASSNAME,PROPERTYLIST)
	# TODO: modify, filter, schedule

MACROEXPRESSION
	: "set" SPACES GLOBALNAME WHITE EXPRESSION ENDLINE
		:: set_global(GLOBALNAME,EXPRESSION)
	: "setenv" SPACES ENVIRONMENTNAME WHITE EXPRESSION ENDLINE
		:: set_environment(ENVIRONMENTNAME,EXPRESSION)
	: "define" SPACES GLOBALNAME WHITE EXPRESSION ENDLINE
		:: define_global(GLOBALNAME,EXPRESSION)
	: "undefine" SPACES GLOBALNAMEPATTERN ENDLINE
		:: undefine_global(GLOBALNAMEPATTERN)
	: "if" GLOBALTESTEXPRESSION ENDLINE
		:: if_open(GLOBALTESTEXPRESSION)
	: "elif" GLOBALTESTEXPRESSION ENDLINE
		:: else_if(GLOBALTESTEXPRESSION)
	: "else" ENDLINE
		:: if_else()
	: "endif" ENDLINE
		:: if_close()
	# TODO: wget, print, warning, error, etc.

INLINETEXT
	: BLOCKTEXT
	: "{" INLINETEXT "}"

BLOCKTEXT
	: [^{]*

%END resolve_unknowns()