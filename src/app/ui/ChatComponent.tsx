'use client'
import React, { useState, useEffect, useRef } from 'react'
import { Input } from '@/components/ui/input'
import { Send } from 'lucide-react'
import { Button } from '@/components/ui/button'
import MessageList  from './MessageList'
import ResultTab from './ResultTab'

import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
  } from "@/components/ui/resizable"
import { ScrollArea } from "@/components/ui/scroll-area"
import Image from 'next/image'
import { todo } from 'node:test'
import { v4 } from 'uuid'
import { getCookie } from '@/utils';


interface Message {
  messageId: string;
  role: 'agent' | 'user';
  timestamp: string;
  content: string;
  session_id: string;
  project_id: string;
  user_id: string; 
}

type Conversation = Message[];



// function addMessage(conversation: Conversation, role: 'agent' | 'user', text: string): Conversation {
//   const newMessage: Message = {
//       role: role,
//       timestamp: new Date(),
//       content: text,
//   };

//   return [...conversation, newMessage];
// }

let result: {
  todoList: Array<{
      task_id: string;
      description: string;
      status: string;
  }>,
  curriculum: {
      title: string;
      overview: string;
      modules: Array<{
          title: string;
          content: string;
          task_id: string;
      }>;
  } | null,
  lectureNotes: Array<{
    // filename: string;
    content: string;
    // url: string;
  }>,
  quizzes: Array<{
    question: string;
    option: string[];
    answer: string;
    explain: string;
    source: string;
  }>,
  presentationURL: Array<{
    name: string;
    url: string;
  }>
} = {
  todoList: [],
  curriculum: {
    title: '',
    overview: '',
    modules: []
  },
  lectureNotes: [],
  quizzes: [{
    question: '',
    option: [''],
    answer: '',
    explain: '',
    source: ''
  }],
  presentationURL: [{
    name: '',
    url: ''
  }]
};

type Props = {
    sessionId: string;
    project_id: string;}

const ChatComponent = ({ sessionId, project_id }: Props) => {
    const [ws, setWs] = useState<WebSocket | null>(null);
    const [messages, setMessages] = useState<Conversation>([]);
    const [messageText, setMessageText] = useState('');
    const messagesRef = useRef(messages);

    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [isConnected, setIsConnected] = useState(false);
    const user_id = getCookie("userId");

    const [quizCreated, setQuizCreated] = useState(0);



    useEffect(() => {
      fetch(`http://localhost:8000/messages?sessionId=${sessionId}`)
        .then(res => res.json())
        .then(data => setMessages(data))
        .catch(err => console.error(err))
    }, [sessionId]);

    // Get current messages state
    useEffect(() => {
      messagesRef.current = messages;
    }, [messages]);

  
    // WebSocket connection setup on component mount
    // useEffect(() => {
    //   // Use a relative URL that works in development and production
    //   const WS_URL = typeof window !== 'undefined'
    //     ? `ws://${window.location.hostname}:8001/ws`
    //     : `ws://localhost:8001/ws`;
      
    //   const websocket = new WebSocket(WS_URL);
    //   setWs(websocket);

    //   console.log(websocket)
  
    //   websocket.onopen = () => {
    //     console.log('[CLIENT] Connected to WebSocket server');
    //     setIsConnected(true);
    //   };
  
    //   websocket.onmessage = (event) => {
    //     try {
    //       const parsedMessage = JSON.parse(event.data);
    //       console.log(parsedMessage);
          
    //       if (parsedMessage.hasOwnProperty("role")) {
    //         setMessages((prev) => [...prev, parsedMessage]);
    //       } else {
    //         // result = parsedMessage;
    //       }
    //     } catch (error) {
    //       console.error('Error parsing message from server', error);
    //     }
    //   };
  
    //   websocket.onclose = () => {
    //     console.log('[CLIENT] Disconnected from WebSocket server');
    //     setIsConnected(false);
    //   };
  
    //   websocket.onerror = (error) => {
    //     console.error('[CLIENT] WebSocket error:', error);
    //     setIsConnected(false);
    //   };
  
    //   // Clean up the WebSocket connection when the component unmounts
    //   return () => {
    //     if (websocket.readyState === WebSocket.OPEN || websocket.readyState === WebSocket.CONNECTING) {
    //       websocket.close();
    //     }
    //   };
    // }, []); // Empty dependency array ensures this runs only once on mount
  
    useEffect(() => {
        const WS_URL = typeof window !== 'undefined'
          ? `ws://${window.location.hostname}:8001/ws`
          : `ws://localhost:8001/ws`;
        
        const websocket = new WebSocket(WS_URL);
        setWs(websocket);

        websocket.onopen = () => setIsConnected(true);

        websocket.onmessage = (event) => {
          try {
            const parsedMessage = JSON.parse(event.data);

            const { messageId, content, role, timestamp, session_id } = messagesRef.current[messagesRef.current.length - 1];
            
            if (parsedMessage.event === 'quiz_created') {
                setQuizCreated(prev => prev + 1); // <-- thêm dòng này!
              }


            if (parsedMessage.hasOwnProperty("role")) {
              if (parsedMessage.messageId !== messageId) {
                    setMessages((prev) => [...prev, parsedMessage]);
              } else {
                  setMessages((prevMessages) => {
                    if (prevMessages.length === 0) return prevMessages;

                    const updatedMessages = [...prevMessages];
                    const lastIndex = updatedMessages.length - 1; 

                    updatedMessages[lastIndex] = {
                      ...updatedMessages[lastIndex],
                      content: updatedMessages[lastIndex].content + parsedMessage.content,
                    };
                  
                    return updatedMessages;
                  });
              }
            } else {
              result = parsedMessage;
            }

            
          } catch (error) {
            console.error('Error parsing message from server', error);
          }
        };

        websocket.onclose = () => setIsConnected(false);
        websocket.onerror = () => setIsConnected(false);

        return () => {
          websocket.close();
        };
      }, [sessionId]);


    // Scroll to bottom when new messages arrive
    useEffect(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);
  
    const handleSendMessage = (e: React.FormEvent) => {
      e.preventDefault();
  
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        alert('Not connected to WebSocket server!');
        return;
      }

      const messageId = v4();
  
      if (messageText.trim()) {
        const message: Message = {
          messageId: messageId, 
          content: messageText,
          role: 'user', 
          timestamp: new Date().toISOString(),
          session_id: sessionId,
          project_id: project_id,
          user_id: user_id
        };

        setMessages((prev) => [...prev, message]);
        ws.send(JSON.stringify(message));
        setMessageText('');
      }
    };

    

    // const handleSendMessage = (e: React.FormEvent) => {
    //   e.preventDefault(); // Prevent the default form submission behavior (page reload)
  
    //   if (messageText.trim()) {
    //     const message: Message = {
    //       content: messageText,
    //       role: 'user', 
    //       timestamp: new Date().toISOString(),
    //     };

    //     fetch(`http://localhost:8000/save_message`, {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json"
    //       },
    //       body: JSON.stringify({
    //         session_id: sessionId,
    //         content: messageText, 
    //         role: "user",
    //         timestamp: new Date().toISOString(),
    //       }),
    //     })
    //     .catch(error => {
    //       console.error("Lỗi khi thêm message:", error);
    //     });

    //     const response: Message = {
    //       content: "Hello, How can I help you?",
    //       role: 'agent',
    //       timestamp: new Date().toISOString(),
    //     }

    //     fetch(`http://localhost:8000/save_message`, {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json"
    //       },
    //       body: JSON.stringify({
    //         session_id: sessionId,
    //         content: messageText, 
    //         role: "agent",
    //         timestamp: new Date().toISOString(),
    //       }),
    //     })
    //     .catch(error => {
    //       console.error("Lỗi khi thêm message:", error);
    //     });

    //     setMessages((prev) => [...prev, message, response]);
    //     setMessageText(''); // Clear the input after sending
        
    //     console.log(messages);
    //   }
    // };
       
    return (
          <ResizablePanelGroup
            direction="horizontal"
            className="w-full h-screen max-h-screen rounded-lg"
          >
            <ResizablePanel defaultSize={60} minSize={40}>
              <div className="w-full h-full grid grid-rows-10 gap-4 p-4">
                <div className="">
                    <h3 className="text-lg text-slate-700 font-semibold">Introduction to Artificial Intelligence</h3>
                </div>

                {/* message list */}
                <ScrollArea className="border rounded-xl row-span-8">
                    <MessageList websocket={ws} isConnected={isConnected} messages={messages} />
                     <div ref={messagesEndRef} />
                </ScrollArea>
                
                {/* text area */}
                <div className="row-span-2">
                  <form onSubmit={(e) => handleSendMessage(e)} className="w-full flex flex-row items-center">
                     <Input value={messageText} onChange={(e) => setMessageText(e.target.value)} 
                            placeholder='Type your message ...' 
                            className="grow focus:border-2 focus:border-sky-500 ring-0 focus:ring-0 flex-row"
                     />
                     <Button className="w-10 flex-none bg-blue-500 ml-2">
                         <Send className='w-4 h-4' />
                     </Button>
                 </form>
                </div>
              </div>
            </ResizablePanel>

            <ResizableHandle withHandle/>

            <ResizablePanel className="" defaultSize={40} minSize={40}>
                  <ResultTab result={result} websocket={ws} isConnected={isConnected} sessionId={sessionId} projectId={project_id} 
                              quizCreated={quizCreated} />
                  <div className="flex rounded-xl h-full items-center justify-center p-10">

                  </div>
            </ResizablePanel>
          </ResizablePanelGroup>
        )
}

export default ChatComponent
