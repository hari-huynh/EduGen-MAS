'use client'
import React from 'react';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

import Image from 'next/image';
import { Plus } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

type Props = {
    creator_id: string | null
}

const NewProject = ({ creator_id }: Props) => {
    const router = useRouter();
    const [projectName, setProjectName] = useState("");

    const handleSubmit = () => { 
        fetch("http://localhost:8000/add_new_project", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: projectName,
                creator_id: creator_id
            }),
        })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            router.push(`/p/${data.projectId}/${data.sessionId}`);
        })
        .catch(error => {
            console.error("Lỗi gửi thông tin user:", error);
        });
    }

  return (
    // bg-gradient-to-r from-indigo-300 from-10% via-sky-300 via-30% to-emerald-300 to-90%
    <Dialog>
        <form>
            <DialogTrigger asChild>
                <Card className="flex w-80 h-48 bg-black items-center justify-center">
                    <CardContent>
                        <div>
                            <Plus className='w-20 h-20 font-bold text-white'/>
                        </div>
                    </CardContent>
                </Card>
            </DialogTrigger>

            <DialogContent className="sm:max-w-[425px]">

            <DialogHeader>
                <DialogTitle>New Project</DialogTitle>
                <DialogDescription>
                Tạo ra project mới chứa các tài liệu học tập
                </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4">
                <div className="grid gap-3">
                    <Label htmlFor="name-1">Project Name</Label>
                    <Input id="name-1" 
                           name="name" 
                           placeholder='Project Name' 
                           value={projectName}
                           onChange={(e) => setProjectName(e.target.value)}
                    />
                </div>

                {/* <div className="grid gap-3">
                <Label htmlFor="username-1">Username</Label>
                <Input id="username-1" name="username" defaultValue="@peduarte" />
                </div> */}
            </div>
            <DialogFooter>
                <DialogClose asChild>
                    <Button variant="outline">Cancel</Button>
                </DialogClose>
                
                <DialogClose>
                    <Button type="submit" onClick={handleSubmit}>Save changes</Button>
                </DialogClose>
            </DialogFooter>
            </DialogContent>
        </form>
    </Dialog>
  )
}

export default NewProject;
