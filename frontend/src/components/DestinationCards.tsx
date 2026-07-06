import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import type { DestinationList } from "@/lib/types"

export interface DestinationCardsProps {
  destinations: DestinationList
  onSelect: (name: string) => void
  busy: boolean
}

export function DestinationCards({
  destinations,
  onSelect,
  busy,
}: DestinationCardsProps): JSX.Element {
  return (
    <div className="space-y-2">
      {destinations.suggestions.map((dest, idx) => (
        <Card key={idx} className="p-4 flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-baseline gap-1">
              <h3 className="font-medium">{dest.name}</h3>
              <span className="text-xs text-muted-foreground">· {dest.country}</span>
            </div>
            <p className="text-sm text-muted-foreground mt-1">{dest.why}</p>
            <div className="flex flex-wrap gap-2 mt-2">
              {dest.tags.map((tag, tidx) => (
                <Badge key={tidx} className="text-xs bg-blue-500/70 text-white hover:bg-blue-500">
                  {tag}
                </Badge>
              ))}
            </div>
          </div>
          <Button
            size="sm"
            variant="outline"
            onClick={() => onSelect(dest.name)}
            disabled={busy}
          >
            Auswählen
          </Button>
        </Card>
      ))}
    </div>
  )
}
