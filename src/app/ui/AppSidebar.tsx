'use client'
import { Calendar, Home, Workflow, Plus, Search, Settings, KeyRound,
    GraduationCap, LibraryBig, ScrollText,
    ChevronDown,
    NotebookPen,
    Presentation,
    FileQuestion,
    MessageCircle
} from 'lucide-react'
import React, { useState, useEffect } from "react";

import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupAction,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarHeader,   
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarRail,
    SidebarTrigger
} from "@/components/ui/sidebar"
import { SignedIn, SignedOut, SignInButton, UserButton, ClerkProvider } from '@clerk/nextjs';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import Link from "next/link"
import { Input } from "@/components/ui/input"
import { useRouter } from "next/navigation"
// import UploadDrawer from "@/ui/UploadDrawer"
import Image from 'next/image'
import { getCookie } from '@/utils';
import { usePathname } from "next/navigation";
import UploadDrawer from "../ui/UploadDrawer";

// Menu items
const items = [
    {
        title: "Home",
        url: "/",
        icon: Home,
    },
    // {
    //     title: "Agent Workflow",
    //     url: "/multiagent",
    //     icon: Workflow,
    // },
    // {
    //     title: "Chat",
    //     url: "/chat",
    //     icon: MessageCircle,
    // },
    // {
    //     title: "Settings",
    //     url: "#",
    //     icon: Settings,
    // },
    // {
    //     title: "Secrets",
    //     url: "/secret",
    //     icon: KeyRound,
    // },
]

type Props = {
    userId: string ;
    projectId: string;
}

export function AppSidebar({ userId, projectId  } : Props) {
    const router = useRouter()
    const pathname = usePathname();

    // const [sessions, setSessions] = useState([])
    
    useEffect(() => {
      fetch(`http://localhost:8000/sessions?userId=${userId}&projectId=${projectId}`)
    //   fetch(`http://localhost:8000/p/projectId=${projectId}`)
      .then(res => res.json())
      .then(data => setSessions(data)            )
      .catch(err => console.error(err))
    }, [userId, projectId, pathname]);

    // console.log(sessions)

    const [uploadedFiles, setUploadedFiles] = useState<{ file_key: string; file_name: string }[]>([]);

    // const handleUploadSuccess = (fileInfo: { file_key: string; file_name: string }) => {
    //     setUploadedFiles((prev) => [...prev, fileInfo]);
    // };


    // const handleUploadSuccess = () => {
    //     fetch(`http://localhost:8000/get_book?userId=${userId}&projectId=${projectId}`)
    //         .then(res => res.json())
    //         .then(data => setBooks(data));
    //     };
    const handleUploadSuccess = () => {
            fetch(`http://localhost:8000/get_book?userId=${userId}&projectId=${projectId}`)
                .then(res => res.json())
                .then(data => setBooks(data));
            };
    //++++++++++++++++++++++++++++++++++++++++++++++++++++
    // async function handleAddNewSession() {
    //     if (!userId || !projectId) {
    //         alert("Cần có userId và projectId để tạo session mới!");
    //         return;
    //     }
    //     try {
    //         const response = await fetch("http://localhost:8000/add_new_session", {
    //             method: "POST",
    //             headers: {
    //                 "Content-Type": "application/json"
    //             },
    //             body: JSON.stringify({
    //                 id: "", // backend tự sinh session_id
    //                 user_id: userId,
    //                 project_id: projectId
    //             })
    //         });
    //         const data = await response.json();
    //         if (data.message === "Session created successfully") {
    //             // Gọi lại API lấy danh sách session để cập nhật giao diện
    //             const sessionsResponse = await fetch(`http://localhost:8000/sessions?userId=${userId}&projectId=${projectId}`);
    //             const sessionsData = await sessionsResponse.json();
    //             setSessions(sessionsData);
    //         } else {
    //             alert("Tạo session không thành công!");
    //         }
    //     } catch (error) {
    //         console.error("Error:", error);
    //         alert("Có lỗi xảy ra khi tạo session mới.");
    //     }
    // }

    //___________________________________
    async function handleAddNewSession() {
        if (!projectId) {
            alert("Cần có projectId để tạo session mới!");
            return;
        }
        try {
            const userId = getCookie("userId")

            const response = await fetch("http://localhost:8000/add_new_session", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id: "",
                    user_id: userId,
                    project_id: projectId
                })
            });
            const data = await response.json();
            if (data.message === "Session created successfully") {
              
                if (data.session_id) {
                    router.push(`/p/${projectId}/${data.session_id}`);
                    //  setTimeout(() => {
                    //             window.location.reload();
                    //             }, 10); 
                } else {
                    const sessionsResponse = await fetch(`http://localhost:8000/p/${projectId}/${data.session_id}`);
                    const sessionsData = await sessionsResponse.json();
                    setSessions(sessionsData);
                }
            } else {
                alert("Tạo session không thành công!");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Có lỗi xảy ra khi tạo session mới.");
        }
    }

    interface SessionItem {
        session_id: string;
        name?: string;
        id?: string;
        }

        const [sessions, setSessions] = useState<SessionItem[]>([]);


    // const pathname = usePathname();
    let currentSessionId = null;
    const pathParts = pathname.split('/');
    if (pathParts.length >= 4 && pathParts[1] === 'p') {
        currentSessionId = pathParts[3];
    }
    const [selectedSessionId, setSelectedSessionId] = useState<string | null>(currentSessionId || null);


    console.log("User ID:", userId);
    console.log("Project ID:", projectId);


    const [books, setBooks] = useState<{book_id: string; name_book: string; link_book: string;}[]>([]);
    useEffect(() => {
        if (!userId || !projectId) return;
            fetch(`http://localhost:8000/get_book?userId=${userId}&projectId=${projectId}`)
                .then(res => res.json())
                .then(data => {
                setBooks(data);
                })
                .catch(err => console.error(err));
            }, [userId, projectId]);
    return (
        <Sidebar 
        className="dark" 
        collapsible="icon">
        
            <SidebarHeader>
                <div className="flex justify-end items-center">
                    <SidebarTrigger />
                </div>
            </SidebarHeader>

            <SidebarContent className="dark" >
                <SidebarGroup className="dark">
                    <SidebarGroupLabel className="text-md dark">
                        <LibraryBig className="dark:text-white" />
                        <span className="p-2">Sources</span>
                    </SidebarGroupLabel>
                    <SidebarGroupAction title="Add new source">
                        <UploadDrawer  userId={userId || ""}
                                    projectId={projectId || ""} 
                                    onUploadSuccess={handleUploadSuccess}
                                     >
                            <Plus /> 
                        </UploadDrawer>
                        <span className="sr-only">Add new chat</span>
                    </SidebarGroupAction>

                    {/* {uploadedFiles.length > 0 && (
                        <div className="pl-8 pt-2 space-y-1">
                            {uploadedFiles.map((file) => (
                                <div key={file.file_key} className="text-white text-xs truncate flex items-center gap-2">
                                    <Image 
                                        src="pdf.svg"
                                        alt="PDF Icon"
                                        width={20}
                                        height={20}
                                    />
                                    <p className="truncate">{file.file_name}</p>
                                </div>
                            ))}
                        </div>
                    )} */}

                    {/* {books.length > 0 && (
                            <div className="pl-8 pt-2 space-y-1">
                            {books.map((book) => (
                                <div key={book.book_id} className="text-white text-xs truncate flex items-center gap-2">
                                <Image 
                                    src="/pdf.svg"
                                    alt="PDF Icon"
                                    width={20}
                                    height={20}
                                />
                                <a
                                    className="truncate underline"
                                    href={book.link_book}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    title={book.name_book}
                                >
                                    {book.name_book}
                                </a>
                                </div>
                            ))}
                            </div>
                    )} */}

                    {books.length > 0 && (
                        <div className="pl-8 pt-2 space-y-1 overflow-y-auto max-h-64">
                            {books.map((book) => (
                            <div key={book.book_id} className="text-white text-xs truncate flex items-center gap-2">
                                <Image
                                src="/pdf.svg"
                                alt="PDF Icon"
                                width={20}
                                height={20}
                                />
                                <a
                                className="truncate underline"
                                href={book.link_book}
                                target="_blank"
                                rel="noopener noreferrer"
                                title={book.name_book}
                                >
                                {book.name_book}
                                </a>
                            </div>
                            ))}
                        </div>
                        )}
                </SidebarGroup>
                    
                <SidebarGroup className="dark">
                    <SidebarGroupLabel className="text-md dark">
                        <MessageCircle className="dark:text-white"/>
                        <span className="p-2">Chat Sessions</span>
                    </SidebarGroupLabel>

                    <SidebarGroupAction title="New chat session" onClick={handleAddNewSession}>
                        <Plus className="w-10 h-10"/> 
                        <span className="sr-only">New chat session</span>
                    </SidebarGroupAction>

                    {/* <SidebarGroupContent className="dark">
                      
                    
                        <SidebarMenu className="dark">
                                {sessions.map((session) => {
                                    const sid = session.session_id || session.id;
                                    // Kiểm tra nếu là session hiện tại thì thêm class nổi bật
                                    const isCurrent = sid === currentSessionId;
                                    const menuItemClass = `dark py-1 ${isCurrent ? "bg-blue-600 text-white" : ""}`;
                                    return (
                                        <SidebarMenuItem className={menuItemClass} key={sid}>
                                            <SidebarMenuButton asChild size="sm">
                                                <Link href={`/p/${projectId}/${sid}`}>
                                                    <span className="text-md ml-2 dark:text-white">{session.name || 'Untitled Session'}</span>
                                                </Link>
                                            </SidebarMenuButton>
                                        </SidebarMenuItem>
                                    );
                                })}
                                </SidebarMenu>

                    </SidebarGroupContent> */}
                                

                    <SidebarGroupContent className="dark overflow-y-auto max-h-64">
                            <SidebarMenu className="dark">
                                {sessions.map((session) => {
                                const sid = session.session_id || session.id;
                                const isCurrent = sid === currentSessionId;
                                const menuItemClass = `dark py-1 ${isCurrent ? "bg-blue-600 text-white" : ""}`;
                                return (
                                    <SidebarMenuItem className={menuItemClass} key={sid}>
                                    <SidebarMenuButton asChild size="sm">
                                        <Link href={`/p/${projectId}/${sid}`}>
                                        <span className="text-md ml-2 dark:text-white">
                                            {session.name || 'Untitled Session'}
                                        </span>
                                        </Link>
                                    </SidebarMenuButton>
                                    </SidebarMenuItem>
                                );
                                })}
                            </SidebarMenu>
                            </SidebarGroupContent>
                </SidebarGroup>
                    
                <Collapsible defaultOpen className='group/collapsible'>
                    <SidebarGroup className="dark">
                        <SidebarGroupLabel asChild className="text-md dark">
                            <CollapsibleTrigger>
                                Results
                                <ChevronDown className="ml-auto transition-transform group-data-[state=open]/collapsible:rotate-180" />
                            </CollapsibleTrigger>
                        </SidebarGroupLabel>  

                        <CollapsibleContent>
                            <SidebarGroupContent className="dark">
                                <SidebarMenu className="dark">
                                    {items.map((item) => (
                                        <SidebarMenuItem className="dark py-1" key={item.title}>
                                            <SidebarMenuButton asChild size="sm">
                                                <Link href={item.url}>
                                                    <item.icon className='w-24 h-24 dark:text-white' />
                                                    <span className="text-md ml-2 dark:text-white">{item.title}</span>
                                                </Link>
                                            </SidebarMenuButton>
                                        </SidebarMenuItem>
                                    ))}
                                </SidebarMenu>
                            </SidebarGroupContent>
                        </CollapsibleContent>

                    </SidebarGroup>
                </Collapsible>


                <SidebarFooter>
                    <div className="flex items-center space-x-4">
                        <div className="shrink-0">
                            <SignedIn>
                                <UserButton />
                            </SignedIn>
                        </div>

                        <div className="flex flex-col">
                            <p className="font-semibold dark:text-white">Hải Huỳnh</p>
                            <p className="text-sm text-gray-500">whitehatsuzerain3578@gmail.com</p>
                        </div>
                    </div>
                </SidebarFooter>
            </SidebarContent>

            {/* <SidebarFooter>
                <div className="flex items-center space-x-4">
                    <div className="shrink-0">
                        <SignedIn>
                            <UserButton />
                        </SignedIn>
                    </div>

                    <div className="flex flex-col">
                        <p className="font-semibold dark:text-white">Hải Huỳnh</p>
                        <p className="text-sm text-gray-500">whitehatsuzerain3578@gmail.com</p>
                    </div>
                </div>
            </SidebarFooter> */}
        </Sidebar>
    )
}
