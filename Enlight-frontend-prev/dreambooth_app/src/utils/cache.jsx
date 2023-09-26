import lruCache from 'lru-cache';

const cache = new lruCache({
    // the maximum number of items in the cache is set to be 1000
    max: 1000,
    // the maximum age of an item in the cache is set to be infinity
    maxAge: 1000 * 60 * 60 * 24 * 365,
});

export default cache;