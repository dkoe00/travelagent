import { useState } from "react"
import { Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export interface ChatInputProps {
  onSend: (text: string) => void
  disabled: boolean
}

export function ChatInput({ onSend, disabled }: ChatInputProps): JSX.Element {
  const [text, setText] = useState("")

  const handleSubmit = (): void => {
    if (text.trim()) {
      onSend(text)
      setText("")
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent): void => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="flex gap-2 p-4 border-t">
      <Input
        placeholder="Antwort an den Coordinator…"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyPress={handleKeyPress}
        disabled={disabled}
      />
      <Button
        size="sm"
        onClick={handleSubmit}
        disabled={disabled || !text.trim()}
      >
        <Send className="w-4 h-4" />
      </Button>
    </div>
  )
}
