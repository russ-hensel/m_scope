# -*- coding: utf-8 -*-
"""
Purpose:
    part of my ( rsh ) library of reusable code
    a library module for multiple applications
    sometimes included with applications but not used
        as this make my source code management easier.

this needs work including call to super

try

except ( app_exceptions.ApplicationError ) as an_exception:
    print( an_exception.why )
    msg    = f"and here is why {an_exception.why}" )

import app_exceptions

msg   = f"some exception from russ"
raise app_exceptions.ApplicationError( why = msg )


msg   = f"some exception from russ"
raise app_exceptions.ReturnToGui( why = msg )


msg   = f"some exception from russ"
raise app_exceptions.DBOjectException( why = msg )


"""

import sys
import traceback


# ---- custom exceptions
class ApplicationError( Exception ):
    """
    this is for errors either in programming**
    or in configuration **
    or in user input ??
    """
    def __init__(self, why, errors = "not given"):

        # Call the base class constructor with the parameters it needs
        super( ).__init__( why  )
        #self.why    = why
        # Now for your custom code...
        self.errors = errors


class ReturnToGui( ApplicationError ):   # custom exception
    """
    see __init__
    """
    def __init__(self, why, errors = "not given" ):

        """
        raise app_exceptions.RetrunToGui( "some error", errors = "this is errors ")
        when we want to return from any nested code and give control back to the gui
        consider placing a user message in message if we do not want
        it down where the exception is raised

        use:
            for user input errors  maybe
            for user cancel        yes
            bad data in file       maybe

        example

        try:
            self.load_file( file_name )
        except app_exceptions.ReturnToGui  as an_except:
            msg  = f"File Load failed, {an_except.why}"
            AppGlobal.gui.display_info_string( msg )


        """

        # Call the base class constructor with the parameters it needs
        super( ).__init__(  why  )  # message

        # Now for your custom code...
        self.errors = errors

# ================= Class =======================
# Define a class is how we crash out
class DBOjectException( ApplicationError ):
    """
    raise if a condition ( perhaps a bad parameter makes it hard to continue )
    this is for early return to terminate a function usually because of bad
    file name, file contents.... msg should elucidate
    throw back to button press, then catch and put info on
    gui
    use why and error
    """
    # ----------------------------------------
    def __init__(self, why, errors = "not given"):
        # Call the base class constructor with the parameters it needs
        super( ).__init__(  why  )  # message

        # Now for your custom code...
        self.errors = errors

# ------------------
#def print_except_traceback():
# ------------------
def get_execpt_traceback( print_flag = True ):
    """
    Purpose:
        get the traceback info for an exception
        and perhaps print
    app_exceptions.print_except_traceback( print_flag = True )

    """
    (atype, avalue, atraceback)   = sys.exc_info()
    a_join  = "".join( traceback.format_list ( traceback.extract_tb( atraceback ) ) )
    ret_string   = f"-------- get_except_traceback()  -------------\n\n{a_join}"

    if print_flag:
        print( ret_string )

    return ret_string


# ---- test move me ------------------------



# import traceback





try:

    msg         = f"ApplicationError msg { 1 = }"
    raise ApplicationError( 'spam', 'eggs')

except ApplicationError as an_except:   #  or( E1, E2 )

    msg     = f">>{str( an_except ) = }<<"
    print( msg )

    # msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
    # print( msg )

    # msg     = f"an_except.args   >>{an_except.args}<<"
    # print( msg )

    # s_trace = traceback.format_exc()
    # msg     = f"format-exc       >>{s_trace}<<"
    # print( msg )


    #raise  # to reraise same
# finally:
#     msg     = f"in finally  {1}"
#     print( msg )



# try:

#     msg         = f"xxxxx { 1 = }"
#     raise ReturnToGui( 'spam', 'eggs')

# except Exception as an_except:   #  or( E1, E2 )

#     msg     = f">>{str( an_except) =}<<"
#     print( msg )


#     msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
#     print( msg )

#     msg     = f"an_except.args   >>{an_except.args}<<"
#     print( msg )

#     s_trace = traceback.format_exc()
#     msg     = f"format-exc       >>{s_trace}<<"
#     print( msg )
#     # AppGlobal.logger.error( msg )   #    AppGlobal.logger.debug( msg )

#     #raise  # to reraise same
# finally:
#     msg     = f"in finally  {1}"
#     print( msg )





# ---- eof