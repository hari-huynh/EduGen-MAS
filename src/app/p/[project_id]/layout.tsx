'use client'

import '@/app/globals.css'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { AppSidebar } from '../../ui/AppSidebar'
import { GraduationCap } from 'lucide-react';
import { useSearchParams } from "next/navigation";
import { getCookie } from '@/utils';

interface LayoutProps {
  children: React.ReactNode;
  params: {
    project_id: string;
  };
}

export default function Layout({ children, params }: LayoutProps) {
    const user_id = getCookie("userId");
    const { project_id } = params 
    // const params = useSearchParams();
    // const userId = params.get("userId");
    // const projectId= params.get("projectId");

    
    // return (
    //     <div className="bg-gradient-to-br from-blue-300 to-emerald-200 w-full h-full">
    //         <div className="flex object-top-left">
    //             <SidebarProvider
    //                 style={{
    //                     "--sidebar-width": "20rem",
    //                     "--sidebar-width-mobile": "20rem",
    //                 }}
    //             >
                    
    //                 <AppSidebar userId={user_id} projectId={project_id}/>
    //                 <main>
    //                     {children}
    //                 </main>
    //             </SidebarProvider>
    //         </div>
    //     </div>
    // );

    // return (
    //     <div className="bg-gradient-to-br from-blue-300 to-emerald-100 min-h-screen w-full">
    //         <div className="flex min-h-screen">
    //             <SidebarProvider
    //                 style={{
    //                     "--sidebar-width": "20rem",
    //                     "--sidebar-width-mobile": "16rem",
    //                 }}
    //             >
    //                 <aside className="hidden md:flex bg-white/80 shadow-xl border-r border-gray-200 min-h-screen w-80 px-3 py-6">
    //                     <AppSidebar userId={user_id} projectId={project_id}/>
    //                 </aside>
    //                 <main className="flex-1 flex flex-col items-center px-0 py-4 md:p-10">
    //                     <div className="w-full max-w-3xl bg-white/90 rounded-2xl shadow-lg p-0 md:p-6 min-h-[600px]">
    //                         {children}
    //                     </div>
    //                 </main>
    //             </SidebarProvider>
    //         </div>
    //     </div>
    // );

    // return (
    //     <div className="bg-gradient-to-br from-blue-300 to-emerald-100 min-h-screen w-full">
    //         <div className="flex min-h-screen">
    //         <SidebarProvider
    //             style={{
    //             "--sidebar-width": "20rem",
    //             "--sidebar-width-mobile": "16rem",
    //             }}
    //         >
    //             {/* Sidebar cố định, nền trắng, shadow, border */}
    //             <aside className="hidden md:flex bg-white/90 shadow-xl border-r border-gray-200 min-h-screen w-80 px-4 py-8">
    //             <AppSidebar userId={user_id} projectId={project_id}/>
    //             </aside>

    //             {/* Main content chiếm tối đa không gian, căn giữa khung chat */}
    //             <main className="flex-1 flex justify-center items-center h-screen px-2">
    //             <div className="w-full max-w-4xl min-h-[80vh] bg-white/95 rounded-3xl shadow-2xl flex flex-col justify-between p-8">
    //                 {children}
    //             </div>
    //             </main>
    //         </SidebarProvider>
    //         </div>
    //     </div>
    //     )

     return (
        // <div className="bg-gradient-to-br from-blue-300 to-emerald-100 min-h-screen w-full">
        <div className="bg-gradient-to-br from-blue-300 to-emerald-100 min-h-screen w-full">

            <div className="flex min-h-screen">
                <SidebarProvider
                    style={{
                        "--sidebar-width": "20rem",
                        "--sidebar-width-mobile": "16rem",
                    }}
                >
                    <AppSidebar userId={user_id} projectId={project_id} />
                    <main className="flex-1 flex justify-center items-center">
                        {/* <div className="w-full h-full bg-white/95 flex flex-col justify-between"> */}
                        {/* <div className="flex flex-col h-full w-full bg-gradient-to-br from-blue-900 to-emerald-600"> */}
                        {/* <div className="bg-gradient-to-br from-blue-950 to-green-700 min-h-screen w-full"> */}
                        {/* <div className="bg-gradient-to-br from-blue-900 to-emerald-600 min-h-screen w-full"> */}
                        <div className="bg-gradient-to-br from-blue-900 via-black to-emerald-600 min-h-screen w-full">
                            {children}
                        </div>
                    </main>
                </SidebarProvider>
            </div>
        </div>
    )

}
  