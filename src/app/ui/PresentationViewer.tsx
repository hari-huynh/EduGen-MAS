import React from 'react'

type Props = {
    presentation_url: string
}

const PresentationViewer = ({presentation_url}: Props) => {
    return (
        <iframe 
            src={`https://docs.google.com/presentation/d/${presentation_url}/embed?start=true&loop=true&delayms=5000`}
            frameborder="0" className="w-full h-full"
        >
        </iframe>
    )
}

export default PresentationViewer;