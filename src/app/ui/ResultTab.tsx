'use client'
import { useState,useEffect } from "react";

import {
    Card, 
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle
} from '@/components/ui/card'

import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'

import React from 'react'
import ReactMarkdown from 'react-markdown'

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger
} from '@/components/ui/accordion'

import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from "@/components/ui/tabs"

import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from "@/components/ui/dialog"


import { List } from '@radix-ui/react-tabs'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'

import {
    ListTodo,    
    ScrollText,
    NotebookPen,
    Presentation,
    FileQuestion,
    MessageCircle,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

import Link from "next/link";
import path from "path";
import { FileText, ExternalLink } from "lucide-react";
import { FaFilePdf } from "react-icons/fa";
import { getCookie } from '@/utils';


// links_lecture: Array<string>;
// links_quiz: Array<string>;


type Props = {
    result: {
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
            }>
        } | null,
        
        lectureNotes: Array<{
           content: string;
        }>,

        quizzes: Array<{
            question: string;
            option: string[];
            answer: string;
            // explain: string;
            source: string;
        }>,

        presentationURL: Array<{
            name: string;
            url: string;
        }>,
        links_lecture: Array<string>;
        links_quiz: Array<string>;
    },
    websocket: WebSocket | null;
    isConnected: boolean;
    projectId?: string;
    sessionId?: string;
    quizCreated?: number;
}

// const [openPdfIndex, setOpenPdfIndex] = useState<number | null>(null);
const user_id = getCookie("userId");

const ResultTab = ({ 
    result = { 
                    todoList: [], 
                    curriculum: {title: '', overview: '', modules: []}, 
                    lectureNotes: [],
                    quizzes: [],
                    presentationURL: [],
                    links_lecture:[], 
                    links_quiz: []},
            websocket,
            isConnected,
            projectId,
            sessionId,
            quizCreated = 0
             }:  Props) => {  //: Props

    // const [result, setResult] = useState({
    //                             todoList: [],
    //                             curriculum: { title: '', overview: '', modules: [] },
    //                             lectureNotes: [],
    //                             quizzes: [],
    //                             presentationURL: [],
    //                             links_lecture: [],
    //                             links_quiz: []
    //                         });
    // useEffect(() => {
    //     async function fetchData() {
    //         if (!sessionId) return;
    //         const res = await fetch(`/get_session_info?sessionId=${sessionId}`);
    //         const data = await res.json();
    //         // Nếu backend trả về object rỗng thì giữ nguyên default
    //         setResult({
    //             todoList: data.todoList || [],
    //             curriculum: data.curriculum || { title: '', overview: '', modules: [] },
    //             lectureNotes: data.lectureNotes || [],
    //             quizzes: data.quizzes || [],
    //             presentationURL: data.presentationURL || [],
    //             links_lecture: data.links_lecture || [],
    //             links_quiz: data.links_quiz || []
    //         });
    //     }
    //     fetchData();
    // }, [sessionId]);                            
    
    // const [linksQuiz, setLinksQuiz] = useState<string[]>([]);
    // useEffect(() => {
    //     if (!sessionId) return;
    //     fetch(`http://127.0.0.1:8000/get_session_info?sessionId=${sessionId}`)
    //     .then(res => res.json())
    //     .then((data: any[]) => {
    //         const allLinks = data.flatMap((item: any) => item.links_quiz || []);
    //         const uniqueLinks = Array.from(new Set(allLinks));
    //         setLinksQuiz(uniqueLinks);
    //     });
    //     }, [sessionId]);
    
    // const [linksLecture, setLinksLecture] = useState<string[]>([]);
    // useEffect(() => {
    //     if (!sessionId) return;
    //     fetch(`http://127.0.0.1:8000/get_session_info?sessionId=${sessionId}`)
    //     .then(res => res.json())
    //     .then((data: any[]) => {
    //         const allLinks = data.flatMap((item: any) => item.links_lecture || []);
    //         const uniqueLinks = Array.from(new Set(allLinks));
    //         setLinksLecture(uniqueLinks);
    //     });
    //     }, [sessionId]);

    const [linksQuiz, setLinksQuiz] = useState<string[]>([]);
    const [linksLecture, setLinksLecture] = useState<string[]>([]);

    // useEffect(() => {
    // if (!sessionId) return;

    // fetch(`http://127.0.0.1:8000/get_session_info?sessionId=${sessionId}`)
    //     .then(res => res.json())
    //     .then((data: any[]) => {
    //     const getUniqueLinks = (key: 'links_quiz' | 'links_lecture') =>
    //         Array.from(new Set(data.flatMap((item: any) => item[key] || [])));

    //     setLinksQuiz(getUniqueLinks('links_quiz'));
    //     setLinksLecture(getUniqueLinks('links_lecture'));
    //     });
    // }, [sessionId]);


    const fetchLinks = () => {
        fetch(`http://127.0.0.1:8000/get_session_info?sessionId=${sessionId}`)
            .then(res => res.json())
            .then((data: any[]) => {
            const getUniqueLinks = (key: 'links_quiz' | 'links_lecture') =>
                Array.from(new Set(data.flatMap((item: any) => item[key] || [])));
            setLinksQuiz(getUniqueLinks('links_quiz'));
            setLinksLecture(getUniqueLinks('links_lecture'));
            });
        };
    
    // useEffect(() => {  
    //     if (!sessionId) return;
    //     fetchLinks();
    //     }, [sessionId]);

    
        
    useEffect(() => {
        if (!sessionId) return;
        // fetch(`http://127.0.0.1:8000/get_session_info?sessionId=${sessionId}`)
        //     .then(res => res.json())
        //     .then((data: any[]) => {
        //     const allLinks = data.flatMap((item: any) => item.links_quiz || []);
        //     const uniqueLinks = Array.from(new Set(allLinks));
        //     setLinksQuiz(uniqueLinks);
        //     });
        fetch(`http://127.0.0.1:8000/get_session_info?sessionId=${sessionId}`)
            .then(res => res.json())
            .then((data: any[]) => {
            const getUniqueLinks = (key: 'links_quiz' | 'links_lecture') =>
                Array.from(new Set(data.flatMap((item: any) => item[key] || [])));
            setLinksQuiz(getUniqueLinks('links_quiz'));
            setLinksLecture(getUniqueLinks('links_lecture'));
            });
        }, [sessionId, quizCreated]);
    return (
        <Tabs defaultValue='todolist' className="w-full">

            <TabsList className="grid w-full grid-cols-5">
                <TabsTrigger value="todolist">
                    <ListTodo className="w-8 h-8"/>
                </TabsTrigger>

                <TabsTrigger value="curriculum">
                    <ScrollText className='w-8 h-8'/>
                </TabsTrigger>

                <TabsTrigger value="lecture-note">
                    <NotebookPen className='w-8 h-8'/>
                </TabsTrigger>

                <TabsTrigger value="presentation">
                    <Presentation className='w-8 h-8' />
                </TabsTrigger>

                <TabsTrigger value="quiz">
                    <FileQuestion className='w-8 h-8' />
                </TabsTrigger>
            </TabsList>

            <TabsContent value='todolist'>
                <ScrollArea>
                    <div className="">
                        {result.todoList?.map((task) => (
                        <div className="flex space-x-2 space-y-2 ml-5 mt-2">
                            <Checkbox id={task.task_id} 
                                    checked={task.status == "done"} 
                                    className="data-[state=checked]:rounded-full border-green-500 data-[state=checked]:bg-green-500 data-[state=checked]:text-white data-[state=checked]:border-none"/>
                            <Label className="" htmlFor={task.task_id}>{task.description}</Label>
                        </div>
                        ))}
                    </div>
                </ScrollArea>
            </TabsContent>

            <TabsContent value="curriculum">
                <ScrollArea className="h-screen">
                    <div>
                        <div className="items-center p-6">
                            <h1 className="font-bold text-2xl text-center p-2">{result.curriculum?.title}</h1>
                            <p className="text-justify">
                                <ReactMarkdown>{result.curriculum?.overview}</ReactMarkdown>
                            </p>
                        </div>
                        <Accordion type="single" collapsible className='w-full border border-2 m-2 rounded-2xl p-2'>
                            {result.curriculum?.modules?.map((module, index) => (
                                <AccordionItem key={`module-${index}`} value={`item-${index + 1}`}>
                                    <AccordionTrigger>{module.title}</AccordionTrigger>
                                    <AccordionContent>
                                        <p>
                                            <ReactMarkdown>{module.content}</ReactMarkdown>
                                        </p>

                                        <Dialog>
                                            <DialogTrigger asChild>
                                                <Badge>
                                                    <NotebookPen className="w-4 h-4"/>
                                                </Badge>
                                            </DialogTrigger>
                                            

                                            <DialogContent className="w-[95vw] max-w-[95vw] h-[95vh] p-2"
                                                           style={{ maxWidth: '95vw', maxHeight: '95vh', width: '95vw', height: '95vh' }}>
                                                <DialogHeader>
                                                    <DialogTitle className="text-slate-950">Lecture Note</DialogTitle>
                                                        <DialogDescription></DialogDescription>
                                                    </DialogHeader>

                                                    <ScrollArea className="h-[400px]">
                                                        <div className="w-2/3">
                                                            <ReactMarkdown>
                                                                {result.lectureNotes[index]?.content || ""}
                                                            </ReactMarkdown>
                                                        </div>
                                                        <ScrollBar />
                                                    </ScrollArea>
            
                                            </DialogContent>
                                        </Dialog>
                                    </AccordionContent>
                                </AccordionItem>  
                            ))}
                        </Accordion>
                    </div>
                    <ScrollBar />
                </ScrollArea>
            </TabsContent>

            <TabsContent value="presentation">
            </TabsContent>

            {/* <TabsContent value="quiz">

            </TabsContent> */}

            {/* <TabsContent value="quiz">
                <ScrollArea className="h-screen">
                    <div className="p-4 space-y-4">
                        <h2 className="text-xl font-bold mb-2">Quiz Files</h2>
                        {result.links_quiz.length === 0 ? (
                            <p className="text-muted-foreground">No quiz files available.</p>
                        ) : (
                            result.links_quiz.map((fileUrl, idx) => {
                                const moduleTitle = result.curriculum?.modules[idx]?.title;
                                const fallbackFileName = fileUrl.split('/').pop() || `File ${idx + 1}`;
                                const displayName = moduleTitle ? `${moduleTitle}.pdf` : fallbackFileName;

                                return (
                                    <div 
                                        key={`lecture-file-${idx}`} 
                                        className="flex items-center p-3 border rounded-lg hover:shadow transition"
                                    >
                                        <FaFilePdf className="w-6 h-6 text-red-600 mr-3" />
                                        
                                        <Dialog>
                                            <DialogTrigger asChild>
                                                <button className="flex-1 truncate text-left text-blue-600 hover:underline">
                                                    {displayName}
                                                </button>
                                            </DialogTrigger>


                                            <DialogContent 
                                            className="w-[95vw] max-w-[95vw] h-[95vh] p-2"
                                            style={{ maxWidth: '95vw', maxHeight: '95vh', width: '95vw', height: '95vh' }}>
                                                <div className="flex flex-col w-full h-full">
                                                    <div className="text-lg font-semibold p-2 leading-tight">
                                                        {displayName}
                                                    </div>
                                                    <iframe 
                                                        src={fileUrl}
                                                        title={displayName}
                                                        className="w-full flex-1 border-none rounded"
                                                    />
                                                </div>
                                            </DialogContent>

                                        </Dialog>

                                        <a href={fileUrl} target="_blank" rel="noopener noreferrer">
                                            <ExternalLink className="w-5 h-5 text-blue-500 hover:text-blue-700 ml-2" />
                                        </a>
                                    </div>
                                );
                            })
                        )}
                    </div>
                </ScrollArea>
            </TabsContent>
            */}





            <TabsContent value="quiz">
                <ScrollArea className="h-screen">
                    <div className="p-4 space-y-4">

                        {/* <button
                        className="text-blue-600 hover:underline"
                        onClick={fetchLinks}
                        >
                            Làm mới
                        </button> */}

                        <h2 className="text-xl font-bold mb-2">Quiz Files</h2>
                        {(linksQuiz?.length ?? 0) === 0 ? ( //result.links_quiz
                            <p className="text-muted-foreground">No quiz files available.</p>
                        ) : (
                            (linksQuiz ?? []).map((fileUrl, idx) => {
                                // const moduleTitle = result.curriculum?.modules[idx]?.title;
                                // const fallbackFileName = fileUrl.split('/').pop() || `File ${idx + 1}`;
                                // const displayName = moduleTitle ? `${moduleTitle}.pdf` : fallbackFileName;
                                const displayName = fileUrl.split('/').pop() || `File ${idx + 1}`;
                                return (
                                    <div 
                                        key={`lecture-file-${idx}`} 
                                        className="flex items-center p-3 border rounded-lg hover:shadow transition"
                                    >
                                        <FaFilePdf className="w-6 h-6 text-red-600 mr-3" />
                                        
                                        <Dialog>
                                            <DialogTrigger asChild>
                                                <button className="flex-1 truncate text-left text-blue-600 hover:underline">
                                                    {displayName}
                                                </button>
                                            </DialogTrigger>

                                            <DialogContent 
                                            className="w-[95vw] max-w-[95vw] h-[95vh] p-2"
                                            style={{ maxWidth: '95vw', maxHeight: '95vh', width: '95vw', height: '95vh' }}>
                                                <div className="flex flex-col w-full h-full">
                                                    <div className="text-lg font-semibold p-2 leading-tight">
                                                        {displayName}
                                                    </div>
                                                    <iframe 
                                                        src={fileUrl}
                                                        title={displayName}
                                                        className="w-full flex-1 border-none rounded"
                                                    />
                                                </div>
                                            </DialogContent>

                                        </Dialog>

                                        <a href={fileUrl} target="_blank" rel="noopener noreferrer">
                                            <ExternalLink className="w-5 h-5 text-blue-500 hover:text-blue-700 ml-2" />
                                        </a>
                                    </div>
                                );
                            })
                        )}
                    </div>
                </ScrollArea>
            </TabsContent>
            
            {/* <TabsContent value="lecture-note">
                <ScrollArea className="h-screen">
                    <div className="p-4 space-y-4">
                        <h2 className="text-xl font-bold mb-2">Lecture Files</h2>
                        {result.links_lecture.length === 0 ? (
                            <p className="text-muted-foreground">No lecture files available.</p>
                        ) : (
                            result.links_lecture.map((fileUrl, idx) => {
                                const fileName = fileUrl.split('/').pop() || `File ${idx + 1}`;
                                return (
                                    <div 
                                        key={`lecture-file-${idx}`} 
                                        className="flex items-center p-3 border rounded-lg hover:shadow transition"
                                    >
                                        <FileText className="w-6 h-6 text-red-500 mr-3" />
                                        <span className="flex-1 truncate">{fileName}</span>
                                        <a href={fileUrl} target="_blank" rel="noopener noreferrer">
                                            <ExternalLink className="w-5 h-5 text-blue-500 hover:text-blue-700" />
                                        </a>
                                    </div>
                                );
                            })
                        )}
                    </div>
                </ScrollArea>
            </TabsContent> */}

            {/* <TabsContent value="lecture-note">
                    <ScrollArea className="h-screen">
                        <div className="p-4 space-y-4">
                            <h2 className="text-xl font-bold mb-2">Lecture Files</h2>
                            {result.links_lecture.length === 0 ? (
                                <p className="text-muted-foreground">No lecture files available.</p>
                            ) : (
                                result.links_lecture.map((fileUrl, idx) => {
                                    const moduleTitle = result.curriculum?.modules[idx]?.title;
                                    const fallbackFileName = fileUrl.split('/').pop() || `File ${idx + 1}`;
                                    const displayName = moduleTitle ? `${moduleTitle}.pdf` : fallbackFileName;

                                    return (
                                        <div 
                                            key={`lecture-file-${idx}`} 
                                            className="flex items-center p-3 border rounded-lg hover:shadow transition"
                                        >
                                            <FaFilePdf className="w-6 h-6 text-red-600 mr-3" />
                                            <span className="flex-1 truncate">{displayName}</span>
                                            <a href={fileUrl} target="_blank" rel="noopener noreferrer">
                                                <ExternalLink className="w-5 h-5 text-blue-500 hover:text-blue-700" />
                                            </a>
                                        </div>
                                    );
                                })
                            )}
                        </div>
                    </ScrollArea>
            </TabsContent> */}

           
            <TabsContent value="lecture-note">
                <ScrollArea className="h-screen">
                    <div className="p-4 space-y-4">
                        <h2 className="text-xl font-bold mb-2">Lecture Files</h2>
                        {(linksLecture?.length?? 0 ) === 0 ? (
                            <p className="text-muted-foreground">No lecture files available.</p>
                        ) : (
                            ( linksLecture ?? []).map((fileUrl, idx) => { //result.links_lecture
                                // const moduleTitle = result.curriculum?.modules[idx]?.title;
                                // const fallbackFileName = fileUrl.split('/').pop() || `File ${idx + 1}`;
                                // const displayName = moduleTitle ? `${moduleTitle}.pdf` : fallbackFileName;
                                const displayName = fileUrl.split('/').pop() || `File ${idx + 1}`;

                                return (
                                    <div 
                                        key={`lecture-file-${idx}`} 
                                        className="flex items-center p-3 border rounded-lg hover:shadow transition"
                                    >
                                        <FaFilePdf className="w-6 h-6 text-red-600 mr-3" />
                                        
                                        <Dialog>
                                            <DialogTrigger asChild>
                                                <button className="flex-1 truncate text-left text-blue-600 hover:underline">
                                                    {displayName}
                                                </button>
                                            </DialogTrigger>

                                            {/* <DialogContent className="w-[95vw] h-[95vh]">
                                                <DialogHeader>
                                                    <DialogTitle>{displayName}</DialogTitle>
                                                </DialogHeader>
                                                <div className="w-full h-full">
                                                    <iframe 
                                                        src={fileUrl}
                                                        title={displayName}
                                                        className="w-full h-full border-none rounded"
                                                    />
                                                </div>
                                            </DialogContent> */}

                                            {/* <DialogContent 
                                            className="w-[95vw] max-w-[95vw] h-[95vh] p-2"
                                            style={{ maxWidth: '95vw', maxHeight: '95vh', width: '95vw', height: '95vh' }}
                                                >
                                            <DialogHeader className="p-0 m-0">
                                                <DialogTitle className="text-lg font-semibold p-2 m-0">{displayName}</DialogTitle>
                                            </DialogHeader>
                                            <div className="w-full h-full">
                                                <iframe 
                                                    src={fileUrl}
                                                    title={displayName}
                                                    className="w-full h-full border-none rounded"
                                                />
                                            </div>
                                            </DialogContent> */}
                                            <DialogContent 
                                            className="w-[95vw] max-w-[95vw] h-[95vh] p-2"
                                            style={{ maxWidth: '95vw', maxHeight: '95vh', width: '95vw', height: '95vh' }}>
                                                <div className="flex flex-col w-full h-full">
                                                    <div className="text-lg font-semibold p-2 leading-tight">
                                                        {displayName}
                                                    </div>
                                                    <iframe 
                                                        src={fileUrl}
                                                        title={displayName}
                                                        className="w-full flex-1 border-none rounded"
                                                    />
                                                </div>
                                            </DialogContent>

                                        </Dialog>

                                        <a href={fileUrl} target="_blank" rel="noopener noreferrer">
                                            <ExternalLink className="w-5 h-5 text-blue-500 hover:text-blue-700 ml-2" />
                                        </a>
                                    </div>
                                );
                            })
                        )}
                    </div>
                </ScrollArea>
            </TabsContent>


            
        </Tabs>
    )
}

export default ResultTab;


 