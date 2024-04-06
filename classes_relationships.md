# ecs-game-engine

A piece of software or a framework aiming at covering the basics of gamedev

1.2.5. All classses

```mermaid
graph TD;

    subgraph Server
        receive_request
        send_response
    end

    subgraph Client
        send_request
        receive_response
    end

    subgraph GameClient
        update_ui
        input
        event_to_request
    end

    subgraph GameServer
        subgraph process_request
        request_to_event
        process_event
        end
    end
    %% GameClient
    update_ui --> input
    input --event--> event_to_request
    %%! GameClient

    %% GameClient -> Client
    event_to_request --request--> send_request
    %%! GameClient -> Client

    %% Client
    %%! Client

    %% Client -> Server
    send_request--request-->receive_request;
    %%! Client -> Server

    %% Server
    %%! Server
    
    %% Server -> GameServer
    receive_request --request--> request_to_event;
    %%! Server -> GameServer

    %% GameServer
    request_to_event -.event.-> process_event;
    %%! GameServer

    %% GameServer -> Server
    process_event --response--> send_response;
    %%! GameServer -> Server
    
    %% Server -> Client
    send_response --response--> receive_response;
    %%! Server -> Client

    %% Client -> GameClient
    receive_response --response--> update_ui;
    %%! Client -> GameClient

```