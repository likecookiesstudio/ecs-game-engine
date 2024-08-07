# ecs-game-engine

A piece of software or a framework aiming at covering the basics of gamedev

1.2.5. All classses

```mermaid
graph TD;

    subgraph Client
        receive_response
        start
        stop

        subgraph __init__
        self.__requests
        self.__responses
        self.send_thread
        self.recv_thread
        self.send_thread.start\\
        self.recv_thread.start\\
        end

        subgraph self.send_thread\\threading.Thread\__handle_requests\
        self.get_request\\
        send_request\encoded_request\
        end

        subgraph self.recv_thread\\threading.Thread\__handle_responses\
        receive_response
        self.add_response\response\
        end

        subgraph main_client_loop
            self.get_response\\
            subgraph process_response
                subgraph GameClient
                    update_ui
                    input
                    event_to_request
                end
            end
            self.add_request/request/
        end

        self.get_response\\
        self.get_request\\
        self.add_request/request/
        self.add_response\response\
    end

    subgraph SubjectServer
        start
        _run
        subgraph handle_connection
            on_connection
            handle_request
            send_response
        end
        subgraph handle_request
            subgraph GameServer
                subgraph process_request
                request_to_events
                process_event
                end
            end
        end
    end


    %% GameClient
    update_ui --> input
    input --event--> event_to_request
    %%! GameClient

    %% GameClient -> Client
    event_to_request --request--> self.add_request/request/
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
            self.__requests-->self.get_request\\
            self.get_request\\ --encoded_request-->send_request\encoded_request\
        %%! Client().send_thread\\threading.Thread\__handle_requests\

        %% Client().recv_thread\\threading.Thread\__handle_responses\
            receive_response --decoded_response--> self.add_response\response\
            self.add_response\response\-.response.->self.__responses
        %%! Client().recv_thread\\threading.Thread\__handle_responses\
        self.__responses-.response.->self.get_response\\
        self.add_request/request/-.request.->self.__requests 
    %%! Client

    %% Client -> SubjectServer
    send_request\encoded_request\--request-->on_connection;
    %%! Client -> SubjectServer
    on_connection --request--> request_to_events;
    %% SubjectServer
        %% SubjectServer -> GameServer
        handle_connection --request--> request_to_events;
        %%! SubjectServer -> GameServer
        %% GameServer
        request_to_events -.event.-> process_event;
        %%! GameServer
        %% GameServer -> SubjectServer
        process_event --response--> send_response;
        %%! GameServer -> SubjectServer
    %%! SubjectServer
    
    %% SubjectServer -> Client
    send_response --response--> receive_response;
    %%! SubjectServer -> Client

    %% Client -> GameClient
    start-..->self.get_response\\
    self.get_response\\ --response--> update_ui;
    %%! Client -> GameClient

```