# How To Get Up And Running

This repo uses python 3.10

All packages installed are included in requirements.txt

There is a sqlite3.db file, in case you would like some dummy data.

The front end client is in [this repo](https://github.com/DewofyourYouth/forum-client)

## Endpoints (not yet used in frontend):

* http://localhost:8000/threads/delete-thread/<int:thread_id>
* http://localhost:8000/threads/update-thread/<int:thread_id>
* http://localhost:8000/threads/delete-comment/<int:comment_id>
* http://localhost:8000/threads/update-comment/<int:comment_id>

## TODO

* Update and delete on the front end comment
* Update for threads
* Refresh UI for adding comments