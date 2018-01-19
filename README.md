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
 - Enable zip on responses returned by server.
 - Though this version of app is pretty simple, using containerized images of various system components in a more complex system can be beneficial.
 - Implement URL and application event logging.
 - Configure server downtime alerts.
 - Write unit and integration tests.

### How to Run
Code is developed in python 2.7. [Requirements.txt](https://github.com/harishasan/LWW-Element-Set-App/blob/master/requirements.txt) contains the required dependencies. Individual running scripts are placed in the [run](https://github.com/harishasan/LWW-Element-Set-App/tree/master/run) directory, a [helper script](https://github.com/harishasan/LWW-Element-Set-App/blob/master/run_everything.sh) can be used to run all modules at once both locally and on production.
### Deployment
Code is deployed on a single AWS [EC2 instance](http://34.226.152.221/). Please note that server is not serving any html pages so hitting the IP should return a JSON error. Production deployment is using [forever](https://github.com/foreverjs/forever) to automatically restart modules in case of any unexpected problem. All the configurations are passed through environment variables.

### Scale: 10M Concurrent Monkeys
![System Architecture](https://www.dropbox.com/s/brigfgu4hdkrf6g/Screen%20Shot%202018-01-20%20at%201.36.09%20AM.png?raw=1)
Key elements in this design:
 - Using Node servers at API layer because event loop based approach in this scenario can scale better as compared to one thread/request based servers.
 - REST API layer is elastic, nodes are stateless and can be added or removed as needed.
 - Kafka provides scalable, distributed and fault tolerant storage for messages. Writes go into a single Kafka topic.
 - Two Spark streams are listening against the messages in Kafka.
 - Cassandra stream sends data into Cassandra, which provides high write scalability and availability. Data is partitioned by date and time for single partition access and ordered by timestamp for faster scans.
 - Cache stream groups data by writes per minutes and stores it in a Redis or Memcache based caching layer. Most of the read requests will be of recent data (client viewer demanding all updates since time xxx), so caching recent operations can greatly improve performance. Older data can be automatically expired from cache.
 - Read service can determine if requested data exists in cache or it can request data from Cassandra to serve the request.

As always, benchmarking is the only way to ensure that any proposed architecture can actually handle the required load.

