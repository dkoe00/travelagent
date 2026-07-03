import { useEffect, useRef } from "react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { ChatMessage } from "@/lib/types"
import { MessageBubble } from "./MessageBubble"
import { ToolStatusPill } from "./ToolStatusPill"
import { ChatInput } from "./ChatInput"

export interface ChatPanelProps {
  messages: ChatMessage[]
  runningTool: string | null
  busy: boolean
  error: string | null
  onSend: (text: string) => void
  onSelectDestination: (name: string) => void
}

export function ChatPanel({
  messages,
  runningTool,
  busy,
  error,
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
      {error && (
        <Card className="m-4 p-4 border-red-200 bg-red-50">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="font-medium text-red-900">Etwas ist schiefgelaufen</p>
              <p className="text-sm text-red-700 mt-1">{error}</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                const lastUserMsg = [...messages].reverse().find((m) => m.role === "user")
                if (lastUserMsg) onSend(lastUserMsg.text)
              }}
              disabled={busy}
            >
              Erneut versuchen
            </Button>
          </div>
        </Card>
      )}
      <ChatInput onSend={onSend} disabled={busy} />
    </div>
  )
}
