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
        subgraph __init__
        self.__requests
        self.__responses
        self.send_thread
        self.recv_thread
        self.send_thread.start\\
        self.recv_thread.start\\
        end

        subgraph self.send_thread\\threading.Thread\__handle_requests\
        _load_next_request
        _encode_request\request\
        _send_request\encoded_request\
        end

        subgraph self.recv_thread\\threading.Thread\__handle_responses\
        _receive_response
        _decode_response\response\
        queue_response\response\
        end

        self.load_next_response
        self.queue_next_request
    end

    subgraph EventHandler
        request_to_events
        events_to_response
    end

    subgraph Game
        process_events
        generate_events
    end

    subgraph GameClient
    end

    %% GameClient #TODO
    %%! GameClient

    %% GameClient -> Client #TODO
    GameClient-->self.queue_next_request
    self.queue_next_request-->self.__requests
    %%! GameClient -> Client

    %% Client
        %% Client().__init__
            %% definition order
                self.__responses-.define #1.->self.__requests
                self.__requests-.define #2.->self.recv_thread
                self.recv_thread-.define #3.->self.send_thread
                self.send_thread-.define #4.->self.recv_thread.start\\
                self.recv_thread.start\\-.define #5.->self.send_thread.start\\
            %%! definition order
            self.send_thread.start\\-.play.->self.send_thread\\threading.Thread\__handle_requests\
            self.recv_thread.start\\-.play.->self.recv_thread\\threading.Thread\__handle_responses\
        %%! Client().__init__
        
        %% Client().send_thread\\threading.Thread\__handle_requests\
            self.__requests-->_load_next_request
            _load_next_request --request--> _encode_request\request\
            _encode_request\request\--encoded_request-->_send_request\encoded_request\
        %%! Client().send_thread\\threading.Thread\__handle_requests\

        %% Client().recv_thread\\threading.Thread\__handle_responses\
            _receive_response--response-->_decode_response\response\
            _decode_response\response\--decoded_response-->queue_response\response\
            queue_response\response\-->self.__responses
        %%! Client().recv_thread\\threading.Thread\__handle_responses\
    %%! Client

    %% Client -> Server
    _send_request\encoded_request\--request-->receive_request;
    %%! Client -> Server

    %% Server
    %%! Server
    
    %% Server -> EventHandler
    receive_request--request-->request_to_events;
    %%! Server -> EventHandler
    
    %% EventHandler
    %%! EventHandler

    %% EventHandler -> Game
    request_to_events--event/s-->process_events;
    %%! EventHandler -> Game

    %% Game
    process_events-.->generate_events
    %%! Game

    %% Game -> EventHandler
    generate_events--event/s-->events_to_response;
    %%! Game -> EventHandler
    
    %% EventHandler -> Server
    events_to_response--response-->send_response;
    %%! EventHandler -> Server
    
    %% Server -> Client
    send_response--response-->_receive_response;
    %%! Server -> Client

    %% Client -> GameClient
    self.__responses-->self.load_next_response
    self.load_next_response-->GameClient
    %%! Client -> GameClient

```