


Problem statement can be found [here](https://hackmd.io/s/HJkrqjkMG#part-1-lww-element-set-server).

*Notes*
 1. Throughout the code TODOs are mentioned inline, indicating possible improvements in design and implementation.
 2. Due to time constraints, no test cases have been written, only manual testing has been performed.

### LWW-Element-Set CRDT
Code can be found [here](https://github.com/harishasan/LWW-Element-Set)

### LWW-Element-Set Server
![App Architecture](https://www.dropbox.com/s/96p8nv7c8qfewg4/Screen%20Shot%202018-01-20%20at%2012.20.21%20AM.png?raw=1)

The server code is located in [server](https://github.com/harishasan/LWW-Element-Set-App/tree/master/server) directory. It contains all the REST APIs. Please note, for persistence, a file based storage is used instead of database due to couple of reasons.
 1. In the current scope, using database for persistence layer would be overkill. It won't serve any special purpose because the implemented architecture do not require any searching/indexing/querying etc.
 2. The file based storage is used as append only log, which can provide very fast write capability.

In order to get near real time results, Client Viewer sends offset of last record it received. Server sends back the data after provided offset. This ensures Client Viewer gets all past/present/future messages.
#### Todos and Improvements
 - Currently, the I/O operations are not optimized against Client Viewer sync request. One simple improvement could be to create files of fixed size instead of one big single file. This will help by limiting the number of files to read.
 - Similarly, limited set of recent operations can be cached in memory to further reduce the IO operations.
 - Instead of pooling, which gives near real time results, integrate websockets, for sending real time updates to Client Viewer.
 - Backup persistence file on external storage, like AWS S3, for fault tolerance and recovery.
 - Implement file compaction in a background thread. As it is likely that many keys would be repeating in add and remove sets, we only need to keep the latest key within a set for correct representation of LWW-Element-Set's state.
 - Enable zip on responses returned by server.
 - Though this version of app is pretty simple, using containerized images of various system components in a more complex system can be beneficial.
 - Implement URL and application event logging.
 - Configure server downtime alerts.
 - Write unit and integration tests.

### How to Run
Code is developed in python 2.7. [Requirements.txt](https://github.com/harishasan/LWW-Element-Set-App/blob/master/requirements.txt) contains the required dependencies. Individual running scripts are placed in the [run](https://github.com/harishasan/LWW-Element-Set-App/tree/master/run) directory, a [helper script](https://github.com/harishasan/LWW-Element-Set-App/blob/master/run_everything.sh) can be used to run all modules at once both locally and on production.

In short, follow these steps to run the code in **local environment**:
 1. Ensure python 2.7 is installed
 2. Open terminal
 3. Go to project root directory
 4. Run command `pip install requirements.txt`
 5. Run command `sh run_everything.sh`

[This video](https://www.dropbox.com/s/b034j13ccfzcbat/LWW_Element_App.mp4?raw=1) shows the output of running `run_everything` script locally.

**For production**:
 1. Set an environment variable `IS_PRODUCTION` to True
 2. Follow steps mentioned for local environment

### Deployment
Code is deployed on a single AWS [EC2 instance](http://34.226.152.221/). Please note that server is not serving any html pages so hitting the IP should return a JSON error. Production deployment is using [forever](https://github.com/foreverjs/forever) to automatically restart modules in case of any unexpected problem. All the configurations are passed through environment variables.

### Scale: 1M Concurrent Monkeys
![System Architecture](https://www.dropbox.com/s/brigfgu4hdkrf6g/Screen%20Shot%202018-01-20%20at%201.36.09%20AM.png?raw=1)
Key elements in this design:
 - Using Node servers at API layer because event loop based approach in this scenario can scale better as compared to one thread/request based servers.
 - REST API layer is elastic, nodes are stateless and can be added or removed as needed.
 - Kafka provides scalable, distributed and fault tolerant storage for messages. Writes go into a single Kafka topic.
 - Two Spark streams are listening against the messages in Kafka.
 - Cassandra stream sends data into Cassandra (cluster with replication), which provides high write scalability and availability. Data is partitioned by date and time for single partition access and ordered by timestamp for faster scans.
 - Cache stream groups data by writes per minutes and stores it in a Redis or Memcache based caching layer. Most of the read requests will be of recent data (client viewer demanding all updates since time xxx), so caching recent operations can greatly improve performance. Older data can be automatically expired from cache.
 - Read service can determine if requested data exists in cache or it can request data from Cassandra to serve the request.

As always, benchmarking is the only way to ensure that any proposed architecture can actually handle the required load.
### 100K Documents, 1-10 Monkeys
Another interesting and more realistic problem to solve would be to have 100K documents in our data store where each document is being edited by 1-10 monkeys simultaneously in a collaborative fashion. The architecture proposed below addresses this scenario.
![System architecture](https://www.dropbox.com/s/3mdl77iq5509ifr/Screen%20Shot%202018-01-20%20at%2011.34.26%20AM.png?raw=1)
Few points about this design:
 - Using a RDBMS here because the data can be naturally modeled as relational due to entities like users, documents, document_shares, document_versions and document_edits. Additionally, querying can be efficiently done by indexing key entities like user_id and document_id.
 - "Write Magic" is the module responsible for merging edits from multiple collaborators in real time. The core idea, as described in the image, is that the server maintains a complete document with every change updating the document version. Each client starts by pulling latest version from server, hence knows the version it is currently on. With every change, client sends the current version it has and the new change(s). Using this information server updates the document, which might have received changes from other collaborators as well, and it's version and sends the change(s) to all active collaborators. [This is still a high level design, merge logic needs more thorough thinking to ensure scenarios like offline to online clients, conflicting merges, etc are handled correctly].
 - Server maintains the live connections against active collaborators to send the changes in real time.
 - Sharding can be evaluated as an option to improve DB performance.
 - Similarly, Read/Write or Master/Slave configuration can also be considered to improve DB performance.
 - Additionally, an analytics layer can be added for reporting and monitoring purposes.

