'use client'
import React from 'react';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
} from "@/components/ui/card"

import Image from 'next/image';
import { Label } from '@/components/ui/label';
import { useRouter } from 'next/navigation';

type Props = {
    userId: string | null;
    projectId: string;
    title: string;
    createAt: string
}

const ProjectCard = ({userId, projectId, title, createAt}: Props) => {
    const router = useRouter();
    return (
        // bg-gradient-to-r from-indigo-300 from-10% via-sky-300 via-30% to-emerald-300 to-90%

        <Card className="w-80 h-48 bg-slate-950/40"
            onClick={() => {
                // document.cookie = `projectId=${projectId}`
                router.push(`/p/${projectId}`);
            }}

            ///${projectId}
        >
            <CardContent>
                <div className="grid grid-cols-2">
                    <div className="justify-start">
                        <Image src="/images/images.jpg" alt="Artificial Intelligence" width={100} height={100} />
                    </div>

                    <div className="flex p-5 justify-center items-center">
                        <Label className="text-2xl font-semibold text-slate-600">{title}</Label>
                        <Label>{createAt}</Label>
                    </div>
                </div>
            </CardContent>
        </Card>
  )
}

export default ProjectCard;
