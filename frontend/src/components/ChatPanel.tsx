import { useEffect, useRef } from "react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { ChatMessage } from "@/lib/types"
import { MessageBubble } from "./MessageBubble"
import { ToolStatusPill } from "./ToolStatusPill"
import { ChatInput } from "./ChatInput"

export interface ChatPanelProps {
  messages: ChatMessage[]
  runningTool: string | null
  busy: boolean
  onSend: (text: string) => void
  onSelectDestination: (name: string) => void
}

export function ChatPanel({
  messages,
  runningTool,
  busy,
  onSend,
  onSelectDestination,
}: ChatPanelProps): JSX.Element {
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" })
    }
  }, [messages, runningTool])

  const isEmpty = messages.length === 0

  return (
    <div className="flex flex-1 flex-col min-w-0">
      <ScrollArea className="flex-1">
        <div className="p-4 space-y-4">
          {isEmpty && (
            <div className="flex items-center justify-center h-full text-muted-foreground">
              Beschreibe deine Reiseidee — vage oder konkret.
            </div>
          )}
          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              onSelectDestination={onSelectDestination}
              busy={busy}
            />
          ))}
          {runningTool && <ToolStatusPill tool={runningTool} />}
          <div ref={scrollRef} />
        </div>
      </ScrollArea>
      <ChatInput onSend={onSend} disabled={busy} />
    </div>
  )
}
