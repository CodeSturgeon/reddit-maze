Found a little time today to work on the client's requests.

Client can now request the returned move (POST) JSON to exclude the tile data to save on overhead. This is used when the client requests that the avatar moves to a location that has already been visited in this session.

Decoupled the avatar movement from the requests to GAE. This works really nicely but will remain unstable until optimistic locking can be introduced to the move protocol.