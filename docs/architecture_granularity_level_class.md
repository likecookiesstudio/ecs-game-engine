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
    event_to_response
    end

    Client--request-->Server;
    Server--request-->request_to_events;
    request_to_events--event/s-->Game;

    Game--event/s-->event_to_response;
    event_to_response--response-->Server;
    Server--response-->Client;
```

1.2.4. Game class: method granularity level

```mermaid
graph TD;
    subgraph Game
    process_event
    generate_event
    end

    Client--request-->Server;
    Server--request-->EventHandler;
    EventHandler--event/s-->process_event;

    generate_event--event/s-->EventHandler;
    EventHandler--response-->Server;
    Server--response-->Client;
```

1.2.5. All classses [add link here]