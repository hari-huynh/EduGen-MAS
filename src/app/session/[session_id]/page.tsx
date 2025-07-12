'use client'
import '@/app/globals.css'
import ChatComponent from "@/app/ui/ChatComponent" ;
import { AppSidebar } from '@/app/ui/AppSidebar';
import { useSearchParams } from 'next/navigation';
import { SidebarProvider, SidebarInset, SidebarTrigger } from '@/components/ui/sidebar';
import { 
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator
} from '@/components/ui/breadcrumb';


export default function Chat() {
        // <SidebarProvider
        //     style={{
        //         "--sidebar-width": "20rem",
        //         "--sidebar-width-mobile": "20rem",
        //     }}
        // >
        //     <AppSidebar/>
                           
        // </SidebarProvider>


    const params = useSearchParams();
    const userId = params.get("userId");
    const projectId= params.get("projectId");

    
    return (
        <div className="bg-gradient-to-br from-blue-300 to-emerald-200 w-full h-full">

            <div className="flex object-top-left">
                <SidebarProvider
                    style={{
                        "--sidebar-width": "20rem",
                        "--sidebar-width-mobile": "20rem",
                    }}
                >
                    
                    <AppSidebar userId={userId} projectId={projectId}/>
                    <SidebarInset>
                {/* <header className="bg-blue-950 flex h-12 shrink-0 items-center gap-2 transition-[width, height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-8">
                    <div className="flex items-center gap-2 px-4">
                        <SidebarTrigger className="-ml-1" />
                        <Breadcrumb>
                            <BreadcrumbList>
                                <BreadcrumbItem className="hidden md:block">
                                    <BreadcrumbLink href="#">
                                        Multi-Agent
                                    </BreadcrumbLink>
                                </BreadcrumbItem>
                                <BreadcrumbSeparator className="hidden md:block" />
                                <BreadcrumbItem>
                                    <BreadcrumbPage>Chat</BreadcrumbPage>
                                </BreadcrumbItem>
                            </BreadcrumbList>
                        </Breadcrumb>
                    </div>
                </header> */}

                        <div className="flex flex-1">
                            <ChatComponent />
                        </div>
                    </SidebarInset> 
                </SidebarProvider>
            </div>
        </div>
    );
  }