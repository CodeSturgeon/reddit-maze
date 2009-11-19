- Changed POST format to JSON
- Re-implemented move submission to list for multiple moves per POST
- Eliminated know-seen tiles

Makes the client tile loading a lot slicker. On the down side, it's a lot more prone to datastore timeouts and hiccups. Better datastore error handling is needed before release.
