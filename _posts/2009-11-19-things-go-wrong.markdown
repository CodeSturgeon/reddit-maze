- Implemented light HTTPExceptions (a-la [paste])
- Wrapped main GAE functions in try: except blocks
- Cleaned up error generation on  caugt server errors
- Reworked HTML client's server error handling

When things do go wrong, they should be handled a little more gracefully now.

[paste]: http://pythonpaste.org/modules/httpexceptions.html "paste.httexceptions"
