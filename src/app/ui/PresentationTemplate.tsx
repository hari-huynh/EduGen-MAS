import Image from 'next/image';
import React from 'react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface Template {
    id: string;
    thumbnailUrl: string;
    description: string;
}

interface Props {
    onSelectTemplate: (template: string) => void;
}

const PresentationTemplate: React.FC<Props> = ({ onSelectTemplate }) => {
  const templates = [
    {
      id: 'template_1',
      name: 'Modern Template',
      description: 'Clean and modern design with gradient backgrounds',
      preview: '/templates/template_1.png'
    },
    {
      id: 'template_2',
      name: 'Professional Template', 
      description: 'Corporate style with subtle colors and professional fonts',
      preview: '/templates/template_2.png'
    },
    {
      id: 'template_3',
      name: 'Creative Template',
      description: 'Bold colors and dynamic layouts for creative presentations',
      preview: '/templates/template_3.png'
    },
    {
        id: 'template_4',
        name: 'Creative Template',
        description: 'Bold colors and dynamic layouts for creative presentations',
        preview: '/templates/template_4.png'
      }
  ];

  return (
        <ScrollArea className="h-[300px]">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
            {templates.map((template) => (
                <Card 
                key={template.id}
                className="cursor-pointer hover:shadow-lg transition-shadow"
                onClick={() => onSelectTemplate(template.id)}
                >
                <CardHeader>
                    <CardTitle>{template.name}</CardTitle>
                    <CardDescription>{template.description}</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="aspect-video bg-gray-100 rounded-lg mb-4">
                        <Image src={template.preview}
                            alt={template.description}
                            width={1600}
                            height={900}
                        />
                    </div>
                    <Button 
                    className="w-full"
                    onClick={(e) => {
                        e.stopPropagation();
                        onSelectTemplate(template.id);
                    }}
                    >
                    Select Template
                    </Button>
                </CardContent>
                </Card>
            ))}
            </div>
        </ScrollArea>
  );
};

export default PresentationTemplate;
