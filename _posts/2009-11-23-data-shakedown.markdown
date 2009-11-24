- Major R&D playtime with GAE APIs
- Re-made all models
- Switched to key_name based lookup for everything
- Implemented Maze parents for Tile objects
- Re-patterned memcache usage

API is noticeably faster in the new regime :)

Fun fact, getting an entity by equality testing on two properties is 2.6x slower than getting by key. Getting an entity using a single property is also 2.6x slower. Using three properties... again 2.6x slower. Maybe the differences are more distinct at larger volumes... but for my uses the results seem pretty clear. 