```
- ST0263, Project 1
Students:
- Sebastian Pulido Gomez, spulido1@eafit.edu.co
- Danilo De Jesus Toro Echeverri, djtoroe@eafit.edu.co
- David Jose Cardona Nieves, djcardonan@eafit.edu.co

Professor:
- Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
```

# MoM Project

## 1) Description

## 1.1) Accomplished requirements

Our MoM implementation has the following accomplishments:

- A MoM system that allows a client to list, create, and delete queues.
- A MoM system that allows a client to list, create and delete channels (with optional topics) on a specific queue.
- A MoM system that allows a client to push messages (with optional topic) to a specific queue.
- A MoM system that allows a client to subscribe to a specific channel and receive messages.
- A system that distributes queues over multiple MoM servers in order to balance the load.
- A system that is capable of detecting which MoM servers are unavailable so that the queues they served are reallocated
  among the available servers.
- A system that stores messages in a database in order to have a backup whenever queues have to be replicated and restored
  in some other available MoM server.
- A system where administrative operations such as listing, creation, and deletion of queues and channels are done via
  API REST, but the heavy weight operations such as message pushing and reception are done via gRPC.
- An example client application that uses our MoM system via a client module.

Our MoM implementation lacks the following features:

- There is no support for users, authentication and authorization.
- There is no encryption support for messages.

## 2) Architecture

The following diagram shows a general view of our system:

![general-arch](assets/general-arch.png)


This diagram depicts the 3 main layers of our system, namely:

- *Routing/Management layer*: The manager (in red) is in charge of offering the administrative REST API to the clients (in yellow),
  that is, clients can list/create/delete queues and channels via the manager which is in charge of allocating/deallocating the resources
  across the available MoM servers (in blue). The manager is also in charge of keeping track of which MoMs are down in order to
  request some of the other available MoMs to restore the missing queues. Finally, the manager is also in charge of providing
  the clients with the connection information necessary for the clients to push messages to and consume messages from the
  queues that have been created.

- *MoM layer*: The MoM servers (in blue) are in charge of hosting the queues and the channels over those queues. Thus,
  whenever clients want to push messages, they have to connect directly to the MoM hosting the queue they are targeting. Likewise,
  whenever clients want to consume messages from a specific channel in a queue, they have to connect directly to the MoM
  that hosts the channel attached to that queue. These operations, pushing and subscribing, are done via gRPC and there is no
  involvement of the manager here. A consequence of using gRPC for these operations is that clients will have a dedicated
  permanent connection to send/retrieve data from the MoM servers. In particular, this makes message notification a lot more
  efficient as the clients can create a subscriber that listens to a stream of messages that arrive asynchronously via the
  gRPC connection.

- *Storage layer*: On the one hand, a database (in gray) is used for administrative purposes, that is, the manager stores
  information about the available MoM servers and the queues and channels that have been created. On the other hand, the
  MoM servers use the database to store a backup of the messages that are pushed to queues. The messages stored in database
  are used for restoring queues whenever a MoM server goes down.


The next diagram has a more detailed view of how queues and channels are organized in MoM servers:


![mom-service](assets/mom-service.png)

A MoM server hosts one or more queues upon which multiple receiver ends or channels can be created. These channels can be
created with an optional topic, which means that only messages pushed with that specific topic will be seen by a potential
subscriber. In the image above, our MoM server has two channels, C1 and C2, with topics A and B, respectively. Consumer clients
1 and 2 have subscribed to these channels in order to receive a stream of messages via gRPC. Queues have a single write end ("writer")
which is used by pusher clients to send messages with an optional topic to the queue. Notice that pusher clients 1 and 2
use the same writer end to send notifications via gRPC. Now, messages with topic A will only be seen by Consumer 1 and
messages with topic B will only be seen by Consumer 2.


MoM servers are subject to be unavailable for indefinite periods of time. That is why the manager periodically sends
life probes to the registered MoMs in order to know their availability:

![queue-restoring](assets/queue-restoring.png)

Whenever the manager finds a MoM server that is down, it will retrieve from database the list of queues that MoM was hosting,
and will send requests to available MoMs in order for them to restore those queues. The manager will dispatch queue requests
to those MoM servers with the least amount of queues. In turn, MoM servers will retrieve queue messages from database whose
TTL is still valid. This means that there is the chance that some messages that are broadcast through a channel are duplicates
because of this recovery feature. However, each message has a unique id which allows the client to discriminate duplicates.

Finally, it is worth noticing that it is possible for the manager itself to go down. This is one of the single points of
failure in our system. However, there are two facts that mitigate this issue, namely:

- Once clients have established connection with a MoM server, they will no longer need the manager for pushing or consuming
  messages. That is why, if the manager goes down for a while, some clients might not even be affected by it.

- If some MoM servers go down while the manager is down as well, MoM servers are implemented in such a way that if they
  come back to activity before the manager is up, they will rebuild, at boot time, any queues they were previously hosting.
  This works because all queues in database have a record that points to the MoM server that hosts them. Thus if the manager
  has not updated that record, it means that it did not have the chance to reallocate it into a different MoM server.


## 3) Development environment

### 3.1) Operating system

This lab project was developed and tested in Ubuntu 22.04.

### 3.2) Programming languages

*Manager*

The manager was implemented with the [Rust](https://www.rust-lang.org) programming language with compiler version `rustc 1.70.0-nightly`.
All of the dependencies together with their versions are specified in the [Cargo.toml](https://github.com/sebashack/rusty-mom/blob/main/rmom-manager/Cargo.toml)
file in the `rmom-manager` subproject.

*MoM server*

The mom server was implemented with the [Rust](https://www.rust-lang.org) programming language with compiler version `rustc 1.70.0-nightly`.
All of the dependencies together with their versions are specified in the [Cargo.toml](https://github.com/sebashack/rusty-mom/blob/main/rmom/Cargo.toml)
file in the `rmom` subproject.

*Example clients*

The example clients were implemented in Python 3.10.6. The list of dependencies together with their versions are specified
in the [requirements.txt](https://github.com/sebashack/rusty-mom/blob/main/momclient/requirements.txt) file in the `momclient` subproject.


### 3.3) Dir tree

```
rusty-mom
├── first-time-install.sh
├── migrations
│   ├── add.sh
│   ├── run.sh
│   └── sql
│       ├── 20230402194739_add_mom_table.sql
│       ├── 20230402195255_add_queue_table.sql
│       ├── 20230403212924_add_channel_table.sql
│       └── 20230404143935_add_message_table.sql.sql
├── momclient
│   ├── lib
│   │   ├── messages_pb2_grpc.py
│   │   ├── messages_pb2.py
│   │   ├── messages_pb2.pyi
│   │   └── momlib.py
│   ├── Makefile
│   ├── news-consumer
│   │   ├── __main__.py
│   │   └── templates
│   │       └── news.html
│   ├── news-pusher
│   │   └── __main__.py
│   │   └── templates
│   │       └── comments.html
│   └── requirements.txt
├── protos
│   └── messages.proto
├── README.md
├── rmom
│   ├── build.rs
│   ├── build-sqlx.sh
│   ├── Cargo.lock
│   ├── Cargo.toml
│   ├── dev-confs
│   │   ├── mom1.yaml
│   │   ├── mom2.yaml
│   │   ├── mom3.yaml
│   │   └── mom4.yaml
│   ├── environment
│   ├── sqlx-data.json
│   └── src
│       ├── broadcast
│       │   ├── mod.rs
│       │   ├── queue.rs
│       │   └── stream_server.rs
│       ├── database
│       │   ├── connection.rs
│       │   ├── crud.rs
│       │   └── mod.rs
│       ├── lib.rs
│       ├── main.rs
│       └── opts.rs
└── rmom-manager
    ├── build.rs
    ├── build-sqlx.sh
    ├── Cargo.lock
    ├── Cargo.toml
    ├── environment
    ├── Rocket.toml
    ├── sqlx-data.json
    └── src
        ├── api
        │   ├── endpoints.rs
        │   ├── mod.rs
        │   └── server.rs
        ├── client
        │   ├── endpoints.rs
        │   └── mod.rs
        ├── database
        │   ├── connection.rs
        │   ├── crud.rs
        │   └── mod.rs
        ├── lib.rs
        ├── main.rs
        └── manager
            ├── mod.rs
            └── mom.rs
```

### 3.4) Build process

#### 3.4.1) System dependencies

To install the dependencies necessary to build and work on this project execute the [first-time-install.sh](https://github.com/sebashack/rusty-mom/blob/main/first-time-install.sh) script at the root of this repository:

```
./first-time-install.sh
```


#### 3.4.2) PostgreSQL and migrations

This project requires PostgreSQL 12. To launch a docker container execute the [service.sh](https://github.com/sebashack/rusty-mom/blob/main/docker/service.sh)
script at the `docker` subdirectory:

```
cd docker
./service up
```

To run the database migrations, execute the [run.sh](https://github.com/sebashack/rusty-mom/blob/main/migrations/run.sh) at the
`migrations` subdirectory:

```
cd migrations
./run.sh
```

#### 3.4.3) rmom

All of the dependencies for the `rmom` subproject are managed with the [cargo](https://doc.rust-lang.org/cargo/) tool already
installed with `first-time-install.sh`. To build and run a debugable binary:

```
cd rmom

RUST_LOG=INFO cargo run dev-confs/mom1.yaml
```

`dev-confs/mom1.yaml` is an example configuration file for development which you can modify as needed:

```
host: "127.0.0.1"
port: 50051
external_host: "127.0.0.1"
external_port: 50051
queue_buffer_size: 10000
message_ttl: 600

database:
  host: "127.0.0.1"
  port: 5432
  user: postgres
  password: secret
  dbname: rmom_manager
  min_connections: 2
  max_connections: 20
```

Here is a breakdown of the different sections and their corresponding settings:

*[server section]*

- `host`: This option specifies the IP address or hostname of the machine that the server is running on. In this case, it is set to 127.0.0.1.
- `port`: This option specifies the port number that the server will listen on for incoming connections. In this case, it is set to 50051.
- `external_host`: This option specifies the IP address or hostname that clients should use to connect to the server. In this case, it is also set to 127.0.0.1.
                   This host is the one that should be registered on the manager's configuration.
- `external_port`: This option specifies the port number that clients should use to connect to the server. In this case, it is set to 50051.
                   This port is the one that should be registered on the manager's configuration.
- `queue_buffer_size`: This option specifies the maximum number of messages that a queue buffer can hold in memory. In this case, it is set to 10000.
- `message_ttl`: This option specifies the maximum amount of time that a message is valid in database before being discarded. In this case, it is set to 600 seconds, or 10 minutes.

*[database section]*

This section specifies the configuration options for the database that the mom uses to store and retrieve messages.

- `host`: This option specifies the IP address or hostname of the database server. In this case, it is set to 127.0.0.1.
- `port`: This option specifies the port number that the database server is listening on. In this case, it is set to 5432, which is the default port for PostgreSQL.
- `user`: This option specifies the username that the server uses to authenticate with the database. In this case, it is set to postgres.
- `password`: This option specifies the password that the server uses to authenticate with the database. In this case, it is set to secret.
- `dbname`: This option specifies the name of the database that the server will use to store its data. In this case, it is set to rmom_manager.
- `min_connections`: This option specifies the minimum number of database connections that the server will maintain. In this case, it is set to 2.
- `max_connections`: This option specifies the maximum number of database connections that the server will allow. In this case, it is set to 20.

There are other 3 instances--mom2.yaml, mom3.yaml, mom4.yaml--which can be used to launch additional instances of the
service as required.

#### 3.4.4) rmom-manager

All of the dependencies for the `rmom-manager` subproject are managed with the [cargo](https://doc.rust-lang.org/cargo/) tool already
installed with `first-time-install.sh`. To build and run a debugable binary:


```
cd rmom-manager

RUST_LOG=INFO cargo run
```

A development configuration file for this service is located at [rmom-manager/Rocket.toml](https://github.com/sebashack/rusty-mom/blob/main/rmom-manager/Rocket.toml):

```
[default]
address = "127.0.0.1"
port = 8082
workers = 5
max_blocking = 512
keep_alive = 5
manager_cycle_secs = 5
life_probe_retry_delay_millis = 33
life_probe_max_retries = 3
moms = [{ host = "127.0.0.1", port = 50051 },
        { host = "127.0.0.2", port = 50051 },
        { host = "127.0.0.3", port = 50051 },
        { host = "127.0.0.4", port = 50051 }]

[release]
port = 8080
workers = 20
moms = [{ host = "127.0.0.1", port = 50051 },
        { host = "127.0.0.2", port = 50051 },
        { host = "127.0.0.3", port = 50051 },
        { host = "127.0.0.4", port = 50051 }]

[default.databases.rmom_manager]
url = "postgresql://postgres:secret@127.0.0.1:5432/rmom_manager"
min_connections = 3
max_connections = 5
idle_timeout = 120
connect_timeout = 7
```

Here is a breakdown of the different sections and their corresponding settings:

*[default] Section*

This section sets the default configuration for the manager server.

- `address` specifies the IP address that the server should bind to, which in this case is 127.0.0.1.
- `port` specifies the port number that the server should listen on, which in this case is 8082.
- `workers` specifies the number of worker threads that the server should spawn to handle incoming requests. This is set to 5.
- `max_blocking` specifies the maximum number of blocking tasks that can be queued by each worker thread. This is set to 512.
- `keep_alive` specifies the number of seconds that a connection should be kept alive before being closed. This is set to 5.
- `manager_cycle_secs` specifies the number of seconds between each cycle of the life probing manager loop. This is set to 5.
- `life_probe_retry_delay_millis` specifies the number of milliseconds to wait between retries when checking the health of a MoM server. This is set to 33.
- `life_probe_max_retries` specifies the maximum number of retries that should be attempted when checking the health of a MoM server. This is set to 3.
- `moms` specifies a list of MoM servers that the manager server can communicate with. Each MoM server is specified as a dictionary with host and port keys.

*[release] Section*

This section sets the configuration for the "release" version of the manager server.

- `port` specifies the port number that the release version of the server should listen on, which in this case is 8080.
- `workers specifies the number of worker threads that the release version of the server should spawn to handle incoming requests. This is set to 20.
- `moms` specifies a list of MoM servers that the release version of the manager server can communicate with. Each MoM server is specified in the same
   way as in the [default] section.

*[default.databases.rmom_manager] Section*

This section sets the configuration for the rmom_manager database, which is used by the manager server.

- `url` specifies the connection URL for the database, which in this case is a PostgreSQL database running on 127.0.0.1:5432.
   The URL includes the username (postgres), password (secret), and database name (rmom_manager).
- `min_connections` specifies the minimum number of connections that should be kept open to the database. This is set to 3.
- `max_connections` specifies the maximum number of connections that should be kept open to the database. This is set to 5.
- `idle_timeout` specifies the number of seconds that a connection to the database can be idle before it is closed. This is set to 120.
- `connect_timeout` specifies the number of seconds to wait for a connection to the database before giving up. This is set to 7.

#### 3.4.5) momclient

To build a Python virtual environment with all of the required dependencies run:

```
cd momclient
make set-py-venv-with-deps
```

To run application that pushes news content run:

```
make run-news-pusher
```

To run application that consumes news content and pushes comments run:

```
make run-news-consumer
```

You should be able to see both applications served at `http://127.0.0.1:8081/news` and `http://127.0.0.1:8080/comments`.

You can tweak the configuration settings for each application at `momclient/news-pusher/config.json` and `momclient/news-consumer/config.json`.

## 3.5) Implementation details

### 3.5.1) Protocol buffers

At the root of this repository there is a file named [protos/messages.proto](https://github.com/sebashack/rusty-mom/blob/main/protos/messages.proto)
where the gRPC communication protocol has been defined. The remote call procedures defined there have the following semantics:

- `CreateQueue`: Given a request with a `queue_label`, create a queue on some available MoM server. The `queue_label` must
                 be unique and it is case insensitive.
- `CreateChannel`: Given a channel request with a `queue_label` and a topic, create a channel on the queue identified by
                   `queue_label`. If the channel is not intended to have a topic, the special `__none__` reserved word can
                   be used. Topics are case insensitive.
- `DeleteChannel`: Given a `channel_id`remove the channel identified by it from the queue where it is hosted.
- `DeleteQueue`: Given a `queue_label` remove the queue identified by it from the MoM where it is hosted. When a queue
                 is deleted, all of the messages attached to it are also removed both from the MoM server and database.
- `PushToQueue`: Push a message with a topic to a specific queue hosted by a MoM server. If the message is not intended to have a topic,
                 the special `__none__` reserved word can be used. This operation is intended to be used by clients of
                 this MoM system.
- `SubscribeToChannel`: Subscribe a client to a permanent message stream coming from the channel identified by `channel_id`.
                        Note that this operation will block the consumer client as it will be constanly listening to a
                        data stream.
- `GetHeartbeat`: Send a empty message to a specific MoM server in order to check its availability. This operation is
                  used by the rmom-manager to determine if a MoM server is down.
- `RebuildQueue`: This operation is used by the rmom-manager to request an available MoM server to restore a queue identified
                  by a `queue_label`. After this operation is completed successfully, the MoM server becomes the new owner
                  of that queue.


### 3.5.2) rmom-manager

`rmom-manager` is the coordination and routing layer for our MoM system, that is, it is in charge of keeping track of which
MoM servers are available and which are not; restoring queues on available servers if possible; and providing clients with
an administrative API to manage queues and channels and to get the information necessary to create connections for pushing
to queues and subscribing to channels. To accomplish this, the `rmom-manager` has three major components, namely, the gRPC
client interface to the MoM servers, the REST API exposed to clients and the management task.

The gRPC client interface is defined in [rmom-manager/src/client/endpoints.rs](https://github.com/sebashack/rusty-mom/blob/main/rmom-manager/src/client/endpoints.rs),
and it defines handlers for the operations `CreateQueue`, `DeleteQueue`, `RebuildQueue`, `CreateChannel`, `DeleteChannel`, and `GetHeartbeat`.
This client is intended to address an specific MoM server the manager has been able to establish a connection with. Now,
taking into account that multiple MoM servers are registered in order to increase fault tolerance and balance the load, the manager
keeps track of multiple connections at once via the [AvailableMoMs](https://github.com/sebashack/rusty-mom/blob/main/rmom-manager/src/manager/mom.rs#L101)
data structure:

```
pub struct RegisteredMoM {
    connection: Option<Client>,
    pub host: String,
    pub port: i32,
}

...

type Host = String;
type Port = i32;
type Key = (Host, Port);

...

pub struct AvailableMoMs {
    moms: HashMap<Key, Arc<Mutex<RegisteredMoM>>>,
}
```

`AvailableMoMs` is an immutable HashMap that stores a reference to gRPC clients that where registered in the `Rocket.toml`
config file. Notice that the references to these clients are wrapped within a Mutex in order to prevent race conditions and
synchronize their access.

The REST API is defined at [rmom-manager/src/api/endpoints.rs](https://github.com/sebashack/rusty-mom/blob/main/rmom-manager/src/api/endpoints.rs)
and it defines the following routes:

- `POST /queues/<queue_label>`: Given a unique queue `queue_label`, create a queue in some available MoM in `AvailableMoMs`. Notice
                          that the available MoM will be chosen randomly. The new queue will be also registered in database
                          and associated to the MoM server.
- `DELETE /queues/<queue_label>`: Given a `queue_label`, delete the queue identified by it from the host MoM server and from database.
- `GET /queues/<queue_label>`: Given a `queue_label`, get the MoM server information necessary to push data to the queue identified by it, namely,
                               `{ label: String, host: String, port: int }`.
- `GET /queues`: Get a list of all queues created thus far.
- `GET /queue/<queue_label>/topics`: Get a list of all the different topics created on a specific queue thus far.
- `GET /channels`: Get a list of all channels created thus far.
- `GET /channels/<channel_id>`: Given a `channel_id`, get the MoM server information necessary to subscribe to that channel, namely,
                                `{ id: String, host: String, port: int }`
- `DELETE /channels/<channel_id>`: Given a `channel_id`, delete the channel identified by it. Notice that it will be removed both
                                   from the MoM queue hosting and database.
- `PUT /queues/<queue_label>/channels/<topic>`: Given a `queue_label` and a `topic`, create a channel on the queue identified by
                                                `queue_label`. If the channel is not intended to have a topic, the special `__none__`
                                                reserved word must be used as a topic.

The management task is implemented at [rmom-manager/src/manager/mod.rs](https://github.com/sebashack/rusty-mom/blob/main/rmom-manager/src/manager/mod.rs). Its
data structure is:

```
pub struct Manager {
    moms: AvailableMoMs,
    db_pool: Pool<Postgres>,
    manager_cycle_secs: u64,
    life_probe_max_retries: u16,
    life_probe_retry_delay_millis: u64,
}
```

and implements the `run()` method which spawns a task that is constantly sending life probes to the MoMs registered in `AvailableMoMs`. If the
life probe fails for a number of attempts, the manager assumes the MoM is not available, and for each of the queues that MoM server
was hosting, the manager will pick out the available MoM with the least amount of hosted queues, and will dispatch a RebuildQueue request to it.
If the available MoM could restore the queue successfully, the ownership of the queue will be updated in database. This management
task runs periodically every `manager_cycle_secs` on a separate thread. The manager also implements the `restore_queues()`
operation that does something similar to the `run()` task, but it is only intended to restore any queues when the manager is
booted, which is useful for those cases when the manager was down and some of the MoMs also went down during that period.

### 3.5.3) rmom

`rmom` is the service intended to host queues and channels, and to broadcast messages over those queues. The main components
of `rmom` are its broadcast queue implementation and the gRPC server that implements the `messages.proto` specification.

The broadcast queue implementation can be found at [rmom/src/broadcast/queue.rs](https://github.com/sebashack/rusty-mom/blob/main/rmom/src/broadcast/queue.rs)
which is basically an adaptation of a `Multiple Producer, Multiple Consumer` queue offered by this library: https://github.com/smol-rs/async-broadcast.

In our interface, whenever we create a Queue, we are creating instances of the receiver and sender ends to that queue:

```
pub struct Queue {
    label: QueueLabel,
    w: Sender<Result<Message, Status>>,
    r: Receiver<Result<Message, Status>>,
}
```

One of the important methods for a `Queue` is `duplicate_channel` which, given an optional topic, returns a `ChannelReceiver` endpoint
from which clients can get a data stream:

```
pub struct ChannelReceiver {
    pub id: ChannelId,
    pub topic: Option<String>,
    pub receiver: Receiver<Result<Message, Status>>,
}
```

The other important method is `get_broadcast_end` which returns and endpoint where new messages can be pushed and broadcast
through that queue.

The gRPC server implementation can be found at [rmom/src/broadcast/stream_server.rs](https://github.com/sebashack/rusty-mom/blob/main/rmom/src/broadcast/stream_server.rs).
The data structure that contains the server's state is:

```
pub struct StreamServer {
    host: String,
    port: u16,
    external_host: String,
    external_port: u16,
    channel_receivers: Arc<Mutex<HashMap<ChannelId, (ChannelReceiver, QueueLabel)>>>,
    broadcast_ends: Arc<Mutex<HashMap<QueueLabel, (Queue, BroadcastEnd)>>>,
    buffer_size: usize,
    message_ttl: i64,
    db_pool: DbPool,
}
```

It keeps track of the channels and queues in `channel_receivers` and `broadcast_ends`, respectively. Notice that for each
`Queue` only one `BroadcastEnd` is stored and its access is synchronized by a Mutex. Access to `ChannelReceivers` is also
synchronized via a Mutex. The `StreamServer` also has a `DbPool` which database connections can be acquired from. The database
is used to backup messages and to retrieve messages when a `Queue` needs to be restored. Additionally, `StreamServer` implements
all of the RPC handlers specified in `messages.proto`, but we will only mention some of the outstanding methods here:

- `async fn push_to_queue(&self, push: Request<Push>) -> Result<Response<PushOkResponse>, Status>`: Whenever a `Push` request
  is received (`Push { bytes content = 1; string topic = 2; string queue_label = 3; }`), this method will access the queue
  identified by `queue_label` in `broadcast_ends`, and broadcast a `Message` (`Message { string id = 1; bytes content = 2; string topic = 3; }`)
  on that queue. `Push` notifications are also stored in database with an expiration given by a TTL in order to enable
  queue restoring in case of failures.

- `async fn subscribe_to_channel(&self, req: Request<SubscriptionRequest>,) -> Result<Response<Self::SubscribeToChannelStream>, Status>`: Whenever a
  `SubscriptionRequest` is received (`SubscriptionRequest { string channel_id = 1; }`), the `ChannelReceiver` identified with
  `channel_id` will be retrieved from `channel_receivers`. This `ChannelReceiver` is turned into a data stream and in case a topic
  was specified in the receiver, the messages that don't match it won't be delivered to the consumer. If there is no topic,
  all messages, regardless of the topic, will be delivered.

- `async fn get_heartbeat(&self, _request: Request<HeartbeatRequest>) -> Result<Response<HeartbeatOkResponse>, Status>`: This
  simple operation is used by the manager to detect whether the connection with this MoM server is available or not.


### 3.5.3) momclient example app

`momclient` is just a simple example application that uses our MoM system. It simulates a scenario where one server pushes
`news` to a `news-queue`, and another server consumes the news on that queue to be displayed on a web page. The latter, in turn,
pushes `comments` on those news to a `comments-queue` which are consumed by the former which also displays those comments
on a web page:

![example-arch](assets/example-arch.png)

The example servers are implemented via a rudimentary `momlib` client module that was implemented in order for client
applications to easily interface our system. This module can be found at [momclient/lib/momlib.py](https://github.com/sebashack/rusty-mom/blob/main/momclient/lib/momlib.py).

The two example applications can be found at:

- https://github.com/sebashack/rusty-mom/tree/main/momclient/news-consumer
- https://github.com/sebashack/rusty-mom/tree/main/momclient/news-pusher


## 4) Deployment

This project was deployed in 5 EC2 instances on the AWS academy cloud:

![ec2-machines](assets/ec2-machines.png)

The deployment was performed by cloning the repository on the machines and running a subset of the build scripts  already
mentioned above. The PostgreSQL database was released in its own container with docker-compose. Also, the configuration files
were properly setup for a production environment.

Systemd files where implemented in order to initialize the services when the instances are booted. A copy of
these files can be seen [here](systemd).

Finally, once all of the machines have been initialized, it should be possible to see the web pages of both the `news-consumer`
and the `news-pusher` on some web browser via the dynamic public IP that is allocated for the `project1-clients` machine. For example,
in the screenshot above, the public IP turned out to be `3.91.184.128`. Thus, the applications should be visible on:

- `news-pusher`: http://3.91.184.128:8081/news
- `news-consumer`: http://3.91.184.128:8080/comments

The web pages should look like this:

![ec2-machines](assets/news-pusher-web.png)
![ec2-machines](assets/news-consumer-web.png)

And on refreshing the browser, you should be able to see how new messages are added to the list.


## 5) References

- https://grpc.io/docs/languages/python/basics
- https://doc.rust-lang.org/stable/book/
- https://rocket.rs/v0.5-rc/guide/
- https://github.com/smol-rs/async-broadcast
- https://docs.rs/tonic/latest/tonic
