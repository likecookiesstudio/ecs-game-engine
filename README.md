# ecs-game-engine

A piece of software or a framework aiming at covering the basics of gamedev


# 1. Architecture granularity level from top to bottom

1.1. Class granularity level

```mermaid
graph TD;
    Client--request-->Server;
    Server--request-->EventHandler;
    EventHandler--event/s-->Game;

    Game--event/s-->EventHandler;
    EventHandler--response-->Server;
    Server--response-->Client;
```

1.2. Method granularity level
1.2.1. Client class: method granularity level

```mermaid
graph TD;
    subgraph Client
    _send_request
    _receive_response
    end

    _send_request--request-->Server;
    Server--request-->EventHandler;
    EventHandler--event/s-->Game;

    Game--event/s-->EventHandler;
    EventHandler--response-->Server;
    Server--response-->_receive_response;
```

1.2.2. Server class: method granularity level

```mermaid
graph TD;
    subgraph Server
    receive_request
    send_response
    end

    Client--request-->receive_request;
    receive_request--request-->EventHandler;
    EventHandler--event/s-->Game;

    Game--event/s-->EventHandler;
    EventHandler--response-->send_response;
    send_response--response-->Client;
```

1.2.3. EventHandler class: method granularity level

```mermaid
graph TD;
    subgraph EventHandler
    request_to_events
    events_to_response
    end

    Client--request-->Server;
    Server--request-->request_to_events;
    request_to_events--event/s-->Game;

    Game--event/s-->events_to_response;
    events_to_response--response-->Server;
    Server--response-->Client;
```

1.2.4. Game class: method granularity level

```mermaid
graph TD;
    subgraph Game
    process_events
    generate_events
    end

    Client--request-->Server;
    Server--request-->EventHandler;
    EventHandler--event/s-->process_events;

    generate_events--event/s-->EventHandler;
    EventHandler--response-->Server;
    Server--response-->Client;
```

1.2.5. All classses

```mermaid
graph TD;

    subgraph Server
        receive_request
        send_response
    end

    subgraph Client
        subgraph __init__
            TODO
        end
        _send_request
        subgraph threading.Thread  __handle_responses
            subgraph queue_response\response\
                self.__responses.append\response\
            end
            _receive_response --response--> _decode_response\response\--decoded_response-->queue_response\response\
        end
        subgraph threading.Thread  __handle_requests
            subgraph queue_request\response\
                self.__requests.append\response\
            end
            _send_request --request--> _decode_request\request\--decoded_request-->queue_request\request\
        end
    end

    subgraph EventHandler
        request_to_events
        events_to_response
    end

    subgraph Game
        process_events
        generate_events
    end

    _receive_response-.->_send_request

    queue_request\request\--request-->receive_request;
    receive_request--request-->request_to_events;
    request_to_events--event/s-->process_events;

    process_events-.->generate_events

    generate_events--event/s-->events_to_response;
    events_to_response--response-->send_response;
    send_response--response-->_receive_response;

```