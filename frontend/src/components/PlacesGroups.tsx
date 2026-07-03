import { Badge } from "@/components/ui/badge"
import { PlacesPool } from "@/lib/types"

const KIND_LABELS: Record<string, string> = {
  activity: "Aktivitäten",
  restaurant: "Restaurants",
  cafe: "Cafés",
  accommodation: "Unterkünfte",
}

export interface PlacesGroupsProps {
  pool: PlacesPool
}

export function PlacesGroups({ pool }: PlacesGroupsProps): JSX.Element {
  const grouped = pool.places.reduce(
    (acc, place) => {
      if (!acc[place.kind]) acc[place.kind] = []
      acc[place.kind].push(place)
      return acc
    },
    {} as Record<string, typeof pool.places>
  )

  return (
    <div className="space-y-4">
      {Object.entries(grouped).map(([kind, places]) => (
        <div key={kind}>
          <h3 className="text-sm font-semibold text-muted-foreground mb-2">
            {KIND_LABELS[kind] || kind}
          </h3>
          <div className="space-y-2">
            {places.map((place, idx) => (
              <div key={idx} className="p-3 border rounded-lg">
                <div className="font-medium">{place.name}</div>
                <div className="text-xs text-muted-foreground line-clamp-1">
                  {place.area} — {place.description}
                </div>
                <div className="flex flex-wrap gap-1 mt-1">
                  {place.tags.map((tag, tidx) => (
                    <Badge key={tidx} variant="secondary" className="text-xs">
                      {tag}
                    </Badge>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
