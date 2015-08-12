class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):

	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return repr(self.msg)


class TransitionError(Error):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        prev -- state at beginning of transition
        next -- attempted new state
        msg  -- explanation of why the specific transition is not allowed
    """

    def __init__(self, prev, next, msg):
        self.prev = prev
        self.next = next
        self.msg = msg
