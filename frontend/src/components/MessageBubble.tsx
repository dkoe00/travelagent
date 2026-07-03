import { Route } from "lucide-react"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Card } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import type { ChatMessage } from "@/lib/types"
import { DestinationCards } from "./DestinationCards"
import { PlacesGroups } from "./PlacesGroups"
import { ItineraryView } from "./ItineraryView"

export interface MessageBubbleProps {
  message: ChatMessage
  onSelectDestination: (name: string) => void
  busy: boolean
}

export function MessageBubble({
  message,
  onSelectDestination,
  busy,
}: MessageBubbleProps): JSX.Element {
  if (message.role === "user") {
    return (
      <div className="flex justify-end gap-2">
        <Card className="max-w-xs p-3 bg-muted">
          <p className="text-sm">{message.text}</p>
        </Card>
      </div>
    )
  }

  return (
    <div className="flex gap-2">
      <Avatar className="w-6 h-6 shrink-0">
        <AvatarFallback>
          <Route className="w-4 h-4" />
        </AvatarFallback>
      </Avatar>
      <div className="flex-1 space-y-2">
        {message.toolResults.map((result, idx) => (
          <div key={idx}>
            {result.tool === "discover_destinations" && (
              <DestinationCards
                destinations={result.payload}
                onSelect={(name) => onSelectDestination(name)}
                busy={busy}
              />
            )}
            {result.tool === "find_places" && (
              <PlacesGroups pool={result.payload} />
            )}
            {result.tool === "plan_itinerary" && (
              <ItineraryView itinerary={result.payload} />
            )}
          </div>
        ))}
        {message.streaming && !message.text && (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <Skeleton className="h-4 w-4/6" />
          </div>
        )}
        {message.text && (
          <div className="prose prose-sm max-w-none">
            {message.text.split("\n\n").map((para, idx) => (
              <p key={idx} className="text-sm leading-relaxed">
                {para}
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
