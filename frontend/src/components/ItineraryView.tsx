import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import type { Itinerary } from "@/lib/types"

const TIME_LABELS: Record<string, string> = {
  morning: "Vormittag",
  lunch: "Mittag",
  afternoon: "Nachmittag",
  evening: "Abend",
}

export interface ItineraryViewProps {
  itinerary: Itinerary
}

export function ItineraryView({ itinerary }: ItineraryViewProps): JSX.Element {
  return (
    <div className="space-y-3">
      {itinerary.days.map((day) => (
        <Card key={day.day} className="p-4">
          <div className="font-semibold mb-3">
            Tag {day.day} · {day.theme}
          </div>
          <div className="space-y-2">
            {day.stops.map((stop, idx) => (
              <div key={idx} className="flex gap-3 text-sm">
                <Badge className="shrink-0 whitespace-nowrap bg-amber-600 text-white hover:bg-amber-700">
                  {TIME_LABELS[stop.time_of_day] || stop.time_of_day}
                </Badge>
                <div>
                  <div className="font-medium">{stop.place_name}</div>
                  <div className="text-xs text-muted-foreground">{stop.note}</div>
                </div>
              </div>
            ))}
          </div>
        </Card>
      ))}
    </div>
  )
}
