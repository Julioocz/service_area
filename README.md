# Service Area app.
This app consist in a rest API built with geodjango, django rest
framework to allow service providers to set an area (a polygon) where
they provide their services. The API has an endpoint that allows users
to search for providers that contains a location (lat, lon).

## Caching.
Right now the major problem with this API is the caching. At this moment
it caches the search results (for a given location) with using a key
with an expire time of 5 minutes. If any provider adds a service area
that also contains the location that it's cached it wont be shown.

The solution for this is to invalidate the cache for a location when a
provider adds a service area that contains it. An option to do this will
be to run a background task that checks if any cached location is
contained by a new service area.
