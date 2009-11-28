- Moved code around, cleaning up lines between modules.
- Changed lookup strategy for tiles in client, >2x speed improvement.

The speed of DOM lookups, even just using the ID, really does suck. Got a _HUGE_ performance increases by using a dict for tile lookups rather than the DOM. Scrolling is not nearly as painful as it was.