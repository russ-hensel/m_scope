#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---- tof
"""

may expect AppGlobal.parameters and AppGlobal.logging ??

@author: russ


import string_list_utils
"""

# ---- Imports
#import pprint
import os

# import adjust_path
#import string_util

#from   app_global import AppGlobal

URL_VALID_PREFIXS     = [ "www.", "http://", "https://" ]


# ----------------------------------------
def clean_string_to_list( a_string,
                         delete_tailing_spaces  = True,
                         delete_comments        = False,
                         delete_blank_lines     = False,  ):
    """
    break a string on \n and put in list
        clean
           delete_tailing_spaces  = True,
           delete_comments        = False,   here comment need to start on col 0
           delete_blank_lines     = False,
    see also the textwrap
    """
    a_list   = a_string.split( "\n" )

    if delete_comments:
        a_list   = [ i_line for i_line in a_list if not i_line.startswith( "#") ]

    if delete_blank_lines:
        a_list   = [ i_line for i_line in a_list if i_line.strip( ) != ""]

    if delete_tailing_spaces:
        # for i_line in a_list:
        #     i_line = i_line.r_strip()
        a_list   = [ i_line.rstrip() for i_line in a_list ]



    return a_list

# ----------------------------------------
def extract_self( a_string ):
    """
    extract all the self.xxx = assignments
    this is used for things like construction of __init__ and __str__

    += and -= need to be delt with , perhaps change to "=" then extract
    return
        set of the xxx's
    ex:
        set_self   = clip_string_utils.extract_self( a_string )

    """
    # may be others but ones i use the most
    a_string      = a_string.replace( "+=", "")
    a_string      = a_string.replace( "-=", "")
    # clean up lines
    ( lines, ix_deleted )    = clean_string_to_list( a_string,
                                 delete_tailing_spaces  = True,
                                 delete_comments        = False,
                                 delete_blank_lines     = False,   )
    # remove leading space
    lines_new   = []
    for i_line in lines:
        lines_new.append( i_line.strip() )
    # print( lines )

    # starts with self
    lines       = lines_new
    lines_new   = []
    for i_line in lines:
        if  i_line.startswith( "self." ):
            lines_new.append( i_line )

    # remove self.
    lines       = lines_new
    lines_new   = []
    for i_line in lines:
          lines_new.append( i_line[ 5: ])

    # get assignments
    lines    = lines_new
    lines_new   = []
    for i_line in lines:
        # look for = must be something on both sides
        splits   = i_line.split( "=", maxsplit = 1 )
        if len( splits ) == 2 :
            lines_new.append( splits[0].strip() )

    # no dots no left paren
    lines       = lines_new
    lines_new   = []
    set_new     = set( )
    for i_line in lines:
        if "." not in i_line and "(" not in i_line:
            set_new.add( i_line )

    # lets sort ... and return as a list
    instance_list = sorted( list( set_new ) )
    return instance_list

# ----------------------------------------
def clean_string( a_string ):
    """
    clean up string into non empty parts, eliminate excess white space

    is this worth a function ?? this is a one liner
    :param self:
    :param a_string:
    :return: list of clean parts or clean string

    """
    # cmd> url  https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python
    # cmd> url  http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/
    # a_url  = r"http://www.instructables.com/id/Bandsaw-Stand-From-Scrap-Lumber/"

    #print "clean up whitespace "
    # sentence = ' hello \r\n   apple'
    # print sentence.split()
    b_string = " ".join(a_string.split())
    #  print b_string

    return b_string

# ------------------------------------------
def count_leading_spaces( a_string ):
    """
    what it says, read
    https://stackoverflow.com/questions/13648813/what-is-the-pythonic-way-to-count-the-leading-spaces-in-a-string
    """
    leading_spaces   = len( a_string ) - len( a_string.lstrip(' ') )

    return leading_spaces

# ---- is functions -------------------------------
def begins_with_url( a_string, ):
    """
    it_is  = string_util.begins_with_url( a_string )
    """
    parts       = a_string.split()
    if len( parts ) == 0: # pretty much null string
        return False
    test_url    = parts[0]
    #test_url   = (a_string.split() ).[0])  #.strip()     # parse off using whitespace  and strip

    for i_prefix in URL_VALID_PREFIXS:
        if test_url.find( i_prefix ) == 0:    # find str2 in str1 !! better bings with
            return  True

    return False

#------------------------------
def begins_with_file_name( a_string, ):
    """
    it_is  = string_utils.begins_with_url( a_string )
    """
    parts       = a_string.split()
    if len( parts ) == 0: # pretty much null string
        return False
    test_file_name    = parts[0]
    #test_url   = (a_string.split() ).[0])  #.strip()     # parse off using whitespace  and strip

    if test_file_name.startswith( "/") or test_file_name.startswith( "~/"):
        if "." in test_file_name:
            return  True

    return False

# ---------------------------------
def is_url( a_string,  ):
    """
    !! seee if moved to clip_utils


    v2->v3
    clean up the string and see if it starts with a url, return cleaned url

    is the ( cleaned up ) string a url? !!
           url must be on the first line if multiple and at first non white space
    consider typing the string get_string_type
    return tuple ( boolean, cleaned up url ( truncate at space or cr or lf ... ) )
    """
    is_url_bool                 = False

    parts       = a_string.split()
    test_url    = parts[0]
    #test_url   = (a_string.split() ).[0])  #.strip()     # parse off using whitespace  and strip

    for i_prefix in URL_VALID_PREFIXS:
        if test_url.find( i_prefix ) == 0:    # find str2 in str1
            is_url_bool = True

    if is_url_bool:
        return ( is_url_bool, test_url )
    else:
        return( is_url_bool, "" )

# ------------------------------------------
def float_or_none( a_obj, ):

    """
    convert to float if it works else none
        is it worth the import for this?
        string_utils.float_or_none( a_obj, ) # import  string_utils
    """
    try:
        ret     = float( a_obj )

    except:
        ret     = None

    return ret

# ------------------------------------------
def is_filename( a_string,  ):
#def is_filename( self, a_string,  ):   is_file    file_exists  ?? not sure
    """

    looks to see if file exists
    clean up a_string and see if it starts with a file name
    return flag, cleaned_up_filename
    is the  string a file name -- full path
    might at least strip the name??
    unlike is url no clean up, perhaps a different name
    consider typing the string get_string_type
    return ( < boolean >, <cleaner filename perhaps > )

    """
    #print( "a_string = " + str( a_string ) )
    parts       = a_string.split()
    test_fn     = parts[0]
    #rint( "parts = " + str( parts ) )
    #rint( "----------------------------")
    #print( "a_string = " + str( a_string ) )

    is_fn        =  os.path.isfile( test_fn )   # accepts spaces on end under windows
    #print( a_string )
    #print( " in is_filename  " + str( is_fn ) )

    return is_fn, test_fn

# ------------ end is functions
# ------------------------------
def print_uni( a_string_ish ):
    """
    print even if unicode char messes it con
    maybe doing as a call is over kill
    """
    print(  a_string_ish.encode( 'ascii', 'ignore') )

#------------------------------------
def obj_to_str( an_object ):
    """
    a universal   __str__()
    based on object dict
        sort and justify into columns
        return string_utils.obj_to_str( self )

    to use
    #--------------------------
    # import  string_utils
    def __str__( self ):
        return string_utils.obj_to_str( self )


    """
    print( f"---------for {an_object.__class__.__name__} -------------" )
    lines       =   [ f"{key: <20} = {value!r: <50}"  for   key, value  in an_object.__dict__.items() ]
    lines.sort( )
    a_str       = " \n".join( lines )

    return a_str

# ------------------------------------------
def eval_transform( a_string ):
    """
    eval a string to special characters
    !! add exception processing
    may not be used .... delted
    not sure about print( joe ) an error, deliberate
    """
    print( joe )
    b_string    = eval( a_string,  locals(),  globals() )
    print( f">{a_string}<  >>>>  >{b_string}<")
    return b_string

# ----------------------------------------
def eval_f_string( a_fstring ):
    """
    conditional conversion to an fstring begins with single or double quote
    return
        tuple
        if a_fstring is fsting its eval, else unchanged
        else result of eval
       ( no_exception, ret_string )
    """
    no_exception   = True
    ret_string     = a_fstring
    if a_fstring.startswith( 'f"') or a_fstring.startswith( "f'" ):
        #int( f"clip_string_utils eval_f_string yes yes yes >>{a_fstring})
        #print( locals( ) )
        # print( globals() )
        #snippet  = snippet[ 4:]
        try:
            ret_string  = eval( a_fstring, globals(), locals(),  )
        except Exception as a_except:
            no_exception   = False
            ret_string  = "eval_f_string () unfortunately snippet caused exception"
            # change to loggiong or somethin else better
            print( type(a_except)  )   # the exception instance
            print( "a_except.args = {a_except.args}"  )   # arguments stored in .args
            print( a_except     )      # __str__ allows args to printed directlyeval_f_string

    return ( no_exception, ret_string )

# ------------------------------------------
def string_to_py_list( a_string ):
    """
    Purpose:
        take a multiline string and turn it into a python
        list of strings
        usual clean up of lines
        make multiline if long
        left trim lines for leading spaces

    Notes:
        what if stuff already includes quotes.... tough
        returns a string of python code

    """
    string_list, __     = clean_string_to_list( a_string )

    a_list              = []  # return as list or back to string

    len_max             = 0
    tot_len             = 0

    for i_string in string_list:
        print( i_string )
        i_string  = i_string.lstrip()
        i_len      = len( i_string )
        tot_len   += i_len                    # ?? place for wallrus
        if i_len > len_max:
            len_max  = i_len

        a_list.append( f'"{i_string}"' )

        # ret.append( "======>" + i_string )
    if tot_len > 100:
        a_string   = ", \n".join( a_list )
    else:
        a_string   = ", ".join( a_list )

    a_string   = f"[ {a_string} ]"

    # if False: # debug
    #     print( f"i_string =           {i_string}")
    #     print( f"    leading_spaces       {i_leading_spaces}")
    #     print( f"    first_eq             {ix_first_eq}")
    #     print( f"    ix_first_pound_sign, {ix_first_pound_sign}")


    return a_string

# ---------------------
def to_columns( current_str, item_list, format_list = ( "{: <30}", "{:<30}" ), indent = "    "  ):
    """
    for __str__  probably always default format_list
    see ColunmFormatter which is supposed to be more elaborate version
    see its __str__
    ex:
        import string_util
        a_str     = string_util.to_columns( a_str, ["column_data",    f"{self.column_data}"  ] )
        a_str     = string_util.to_columns( a_str,
                                            ["column_data",    f"{self.column_data}"  ],
                                            format_list = ( "{: <30}", "{:<30}" )
    """
    #rint ( f"item_list {item_list}.............................................................. " )
    line_out  = ""
    for i_item, i_format in zip( item_list, format_list ):
        a_col  = i_format.format( i_item )
        line_out   = f"{indent}{line_out}{a_col}"
    if current_str == "":
        ret_str  = f"{line_out}"
    else:
        ret_str  = f"{current_str}\n{line_out}"
    return ret_str


# -----------------------------------------
class ColumnFormater( ):

    """
    this thing is probably a bad idea --- make something simpler
    using  .format( 'test' ) )
    a_file_deleter    = FileDeleter( )
    a_file_deleter.do_delete_empty( a_path )

    what_deleted     = a_file_deleter.delete_list

    ?? consider adding an output print function to display the progress

    """
    def __init__(self,   ):
        """
        what it says, read

        """
        ...
        self.reset(   )

    # ----------------------------------------
    def reset( self, ):
        """
        reset for reuse


        """
        self.column_data   = []  # fill with tuples of the column data
        self.column_specs  = []  # list of dicts as below in column order

        # a_spcec       =  { "width": 5,
        #                    "allign": "r",   # "l"
        #                     }

    # ----------------------------------------
    def reset_data( self,  ):
        """
        reset for reuse
        you can get the str from time to time and then reset

        """
        self.column_data   = []  # fill with tuples of the column data


    # ----------------------------------------
    def get_default_spec(  self ):
        a_default_spec  =  { "width": 25,
                             "allign": "r",   # "l"
                             }
        return a_default_spec

    # ----------------------------------------
    def return_line( self, column_tuple  ):
        """
        what it says, read
        data formatted and returned
        """
        for i_col_data,  i_column_spec  in zip( column_tuple, self.column_specs ):
            str_line  = ( f"{i_col_data}   format with  {i_column_spec}" )

        return str_line

    # ----------------------------------------
    def add_line( self, column_tuple  ):
        """
        what it says, read
        data accumulated in object
        """
        pass
        self.column_data.append( column_tuple )
        # Could check length against column specs

    # ----------------------------------------
    def add_column( self, column_spec ):
        """
        what it says, read

        """
        self.column_specs.append( column_spec )

    # ----------------------------------------
    def get_result( self,  ):
        """
        format it up
        """
        a_str   = ""

        for i_line in self.column_data:
            str_line   = ""
            for i_col_data,  i_column_spec  in zip( i_line, self.column_specs ):
                str_line  = ( f"{str_line}{i_col_data}   format with  {i_column_spec}" )

        a_str   = f"\n{a_str} {str_line}"

            #for i_column_spec in self.column_specs
        return a_str



    # ----------------------------------------
    def get_str( self,  ):
        """
        not sure what it does
        """
        a_str   = ""

        for i_line in self.column_data:
            a_str   = f"{a_str}\n"
            for ix_col, i_col_data in enumerate( i_line ):
                a_line  = ( i_col_data + "          " )[ 0: self.column_specs[ ix_col ]["width"] ]

        a_str   = f"{a_str} {a_line}"

            #for i_column_spec in self.column_specs
        return a_str

    #------------------
    def __str__( self, ):
        """
        Purpose:
           see title, what it says, read, for debug
        Return:
           a string of info about object
        Raises:
           none planned

        """
        newline  = "\n" + " " * 4
        a_str    = ""
        a_str    = f"{a_str}>>>>>>>>>>* ColumnFormatter (some values) *<<<<<<<<<<<<"
        #a_str    = ( f"{a_str}\n{self.__class__.__name__}: name = {self.name}" )
        # a_str    = f"super().__str__()"

        a_str    = f"{a_str}{newline}column_specs                {self.column_specs}"
        a_str    = f"{a_str}{newline}column_data                 {self.column_data}"

        # convert to
        a_str   = to_columns( a_str, ["column_specs",        f"{self.column_specs}" ] )
        a_str   = to_columns( a_str, ["column_data",         f"{self.column_data}"  ] )

        # a_str    = f"{a_str}{newline}computer_id         {self.running_on.computer_id}"
        # a_str    = f"{a_str}{newline}logger_id           {self.logger_id}"

        return a_str

# ------------------------------------------
def string_to_py_list( a_string ):
    """
    FROM CLIP_STRING_UTIL
    Purpose:
        take a multiline string and turn it into a python
        list of strings
        usual clean up of lines
        make multiline if long
        left trim lines for leading spaces

    Notes:
        what if stuff already includes quotes.... tough
        returns a string of python code

    """
    string_list, __     = clean_string_to_list( a_string )

    a_list              = []  # return as list or back to string

    len_max             = 0
    tot_len             = 0

    for i_string in string_list:
        print( i_string )
        i_string  = i_string.lstrip()
        i_len      = len( i_string )
        tot_len   += i_len                    # ?? place for wallrus
        if i_len > len_max:
            len_max  = i_len

        a_list.append( f'"{i_string}"' )

        # ret.append( "======>" + i_string )
    if tot_len > 100:
        a_string   = ", \n".join( a_list )
    else:
        a_string   = ", ".join( a_list )

    a_string   = f"[ {a_string} ]"

    # if False: # debug
    #     print( f"i_string =           {i_string}")
    #     print( f"    leading_spaces       {i_leading_spaces}")
    #     print( f"    first_eq             {ix_first_eq}")
    #     print( f"    ix_first_pound_sign, {ix_first_pound_sign}")


    return a_string



# ------------------------------------------
def allign_eq_signs( a_string ):
    """
    FROM CLIP, NOT YET FIXED BUT SHULD BE EASY
    Purpose:
        alligns = signs, using first line as a template
        preserves comments
        ignores blank lines and all comment lines
        trims trailing blanks

    Notes:

        must have an exposed = sign on first line
        allign stops if change in indent
                     no = sign found on a line -- unless blank or comment



    ?? probably want to skip blank lines ... may not allow as first
    inconsistent use of i and ix

    !! need to add += ......


    returns a list, not a sting, join with list_to_string_lines( a_list ) if you want a string

            abc         = def   # comment

    change to indicate success ?
    i_format  = "{: <30}"
    a_col  = i_format.format( i_item )

    find_eq

    """

    ( lines, ix_deleted )  = clean_string_to_list( a_string,
                          delete_tailing_spaces  = True,
                          delete_comments        = False,
                          delete_blank_lines     = False,   )
    space_count  = None
    new_lines    = []
    for i_line in lines:
        if space_count is None:
            space_count   = string_utils.count_leading_spaces( i_line )
            find_eq       = i_line.find( "=",   )
            if find_eq == 0:
                return a_string
            #format_var    =  '{:<'  + str( find_eq - space_count ) + '}'
            format_var    =  '{:<'  + str( find_eq     ) + '}'
        splits        = i_line.split( "=" )
        if len( splits)  < 2:
            # no =
            i_new_line   = i_line
            new_lines.append( i_new_line )
            continue

        var          = ( space_count * " " ) + splits[0].strip()
        #format_var    =  '"{: <' 30}"

        assign_to    = "= " + splits[1].strip()
        i_new_line   = string_utils.to_columns( "",
                                            [var,    assign_to  ],
                                            format_list = [  format_var, "{:<50}" ],
                                            indent = "" )

        #i_new_line  = var + assign_to
        new_lines.append( i_new_line )

    return "\n".join( new_lines )


# ------------------------------------------
def num_to_string( an_int, dp_places = "not implemented yet" ):
    """
    string_utils.num_to_string( an_int )

        if dealing with ints in some ranges may not want the dp ??

    """
    test_val   =  1_000_000_000
    if an_int > test_val:
        an_int = an_int/test_val
        text   = f"{an_int:.3f} Giga"
        return text

    test_val   =  1_000_000
    if an_int > test_val:
        an_int = an_int/test_val
        text   = f"{an_int:.3f} Mega"
        return text

    test_val   =  1_000
    if an_int > test_val:
        an_int = an_int/test_val
        text   = f"{an_int:.3f} Kilo"
        return text

    test_val   =  1
    if an_int > test_val:
        an_int = an_int/test_val
        text   = f"{an_int:.3f} "
        return text

    test_val   =  .001
    if an_int > test_val:
        an_int = an_int / test_val
        text   = f"{an_int:.3f} mili"
        return text

    test_val   =  .000001
    if an_int > test_val:
        an_int = an_int/test_val
        text   = f"{an_int:.3f} micro"
        return text

    text   = str( an_int )
    return text

#-------------------------------
def delta_time_to_string( a_float ):
    """
    delta_time in seconds
    use a unit that makes sense
        string_utils.delta_time_to_string( a_float )

    """
    minutes    = 60
    hour       = 60 * minutes
    day        = 24 * hour

    test_val   = day
    if a_float > test_val:
        value  = a_float/test_val
        text   = f"{value:.3f} Days"
        return text

    test_val   =  hour
    if a_float > test_val:
        a_float = a_float/test_val
        text   = f"{a_float:.3f} Hours"
        return text

    test_val   =  minutes
    if a_float > test_val:
        a_float = a_float/test_val
        text   = f"{a_float:.3f} Minutes"
        return text

    test_val   =  1
    if a_float > test_val:
        an_int = a_float/test_val
        text   = f"{a_float:.3f} Seconds"
        return text

    test_val   =  .001
    if a_float > test_val:
        a_float = a_float / test_val
        text   = f"{a_float:.3f} mili Seconds"
        return text

    test_val   =  .000001
    if a_float > test_val:
        a_float = a_float/test_val
        text   = f"{a_float:.3f} micro Seconds"
        return text

    text   = str( an_int )
    return text


#---------------------------
def test_delta_time_to_string():
    """

    delta_time_to_string( a_float )
    """
    a_float    = 24 * 60 * 60 * 22
    print( f"{a_float} -> {delta_time_to_string(a_float)}")

    a_float  = a_float/10
    print( f"{a_float} -> {delta_time_to_string(a_float)}")

    a_float  = a_float/10
    print( f"{a_float} -> {delta_time_to_string(a_float)}")

    a_float  = a_float/10
    print( f"{a_float} -> {delta_time_to_string(a_float)}")

    a_float  = a_float/10
    print( f"{a_float} -> {delta_time_to_string(a_float)}")

    a_float  = a_float/10
    print( f"{a_float} -> {delta_time_to_string(a_float)}")

    a_float  = a_float/10
    print( f"{a_float} -> {delta_time_to_string(a_float)}")

    a_float  = a_float/10
    print( f"{a_float} -> {delta_time_to_string(a_float)}")

    a_float  = a_float/10
    print( f"{a_float} -> {delta_time_to_string(a_float)}")

    a_float  = a_float/10
    print( f"{a_float} -> {delta_time_to_string(a_float)}")

    a_float  = a_float/10
    print( f"{a_float} -> {delta_time_to_string(a_float)}")




#---------------------------
def test_num_to_string():
    """


    """
    an_int  = 36.53
    print( f"{an_int} -> {num_to_string(an_int)}")

    an_int  = an_int/10
    print( f"{an_int} -> {num_to_string(an_int)}")

    an_int  = an_int/10
    print( f"{an_int} -> {num_to_string(an_int)}")

    an_int  = an_int/10
    print( f"{an_int} -> {num_to_string(an_int)}")

    an_int  = an_int/10
    print( f"{an_int} -> {num_to_string(an_int)}")

    an_int  = an_int/10
    print( f"{an_int} -> {num_to_string(an_int)}")

    # print( "---------------------")
    # an_int  = 3.53 *   1_000_000_000
    # print( f"{num_to_string(an_int)}")

    # an_int  = 36.53 *   1_000_000_000
    # print( f"{num_to_string(an_int)}")

    # an_int  = 36.53
    # print( f"{num_to_string(an_int)}")

    # an_int  = 36.53  *   1_000
    # print( f"{num_to_string(an_int)}")

    # an_int  = .3653
    # print( f"{num_to_string(an_int)}")

    # an_int  = 3.653/1_000
    # print( f"{an_int} -> {num_to_string(an_int)}")

#---------------------------
def get_test_string():
    """


    """
    string_list     = ( "no lead or trail\n"
                        "no lead but trail      \n"
                        "                  \n"
                        "      lead and trail      \n"
                        "        \n"
                        "#      comment      "  # \n here produces anothe line

                     )



    return string_list
#---------------------------
def test_clean_string_to_list():
    """

    """
    a_string          = get_test_string()
    a_list            = clean_string_to_list( a_string,
                             delete_tailing_spaces  = True,
                             delete_comments        = False,
                             delete_blank_lines     = False,  )

    #print( f"{a_list}")

    print( "delete trailing")
    for i_line in a_list:
        print( f">{i_line}<" )

    a_list            = clean_string_to_list( a_string,
                             delete_tailing_spaces  = True,
                             delete_comments        = True,
                             delete_blank_lines     = False,  )

    print( "\ndelete trailing and comments")
    for i_line in a_list:
        print( f">{i_line}<" )



    a_list            = clean_string_to_list( a_string,
                             delete_tailing_spaces  = True,
                             delete_comments        = True,
                             delete_blank_lines     = True,  )

    print( "\ndelete trailing and comments and blank")
    for i_line in a_list:
        print( f">{i_line}<" )

#---------------------------
def test_column_formatterxxx():
    """


    """
    a_column_formatter   = ColumnFormater()

    column_spec          = a_column_formatter.get_default_spec()
    a_column_formatter.add_column( column_spec )
    a_column_formatter.add_column( column_spec )

    a_line               = "name",   "john"
    a_column_formatter.add_line( a_line )
    a_line               = "name",   "sueellenjone"
    a_column_formatter.add_line( a_line )
    a_line               = "nm",   "johnthan"
    a_column_formatter.add_line( a_line )

    print( a_column_formatter )
    print( a_column_formatter.get_str() )


    print( a_column_formatter.get_result() )

class TestClass():
    def __init__( self ):
        self.aaaa = "all a's"
        self.bbb  = "some Be gooe"
    def __str__( self ):
        return obj_to_str( self )

# --------------------
def test_obj_to_str():
    """


    """
    a_test_class   = TestClass( )
    # lines       =   [ f"{key: <30} = {value!r: <30}"  for   key, value  in a_test_class.__dict__.items() ]

    # lines.sort(    )
    # a_str       = " \n".join( lines )
    # print(a_str)
    print( f"{str( a_test_class ) }"   )

# ---- test_column_formatter() and...
# --------------------
if __name__ == "x__main__":
   #move tests to sub dir and delete here
   1/0
   test_num_to_string()
   test_obj_to_str()
   test_clean_string_to_list()
   test_delta_time_to_string()
# --------------------



# ---- eof


