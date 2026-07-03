import { Badge } from "@/components/ui/badge"
import { Constraints } from "@/lib/types"

const CONSTRAINT_LABELS: Record<string, string> = {
  region: "Region",
  activity: "Aktivität",
  duration_days: "Dauer",
  month: "Monat",
  budget: "Budget",
}

export interface ConstraintBadgesProps {
  constraints: Constraints
}

export function ConstraintBadges({ constraints }: ConstraintBadgesProps): JSX.Element {
  return (
    <div className="flex flex-wrap gap-2">
      {Object.entries(CONSTRAINT_LABELS).map(([key, label]) => {
        const value = constraints[key as keyof Constraints]
        if (value != null) {
          const displayValue =
            key === "duration_days" ? `${value} Tage` : String(value)
          return (
            <Badge key={key} variant="secondary">
              {label}: {displayValue}
            </Badge>
          )
        }
        return (
          <Badge
            key={key}
            variant="outline"
            className="border-dashed text-muted-foreground"
          >
            {label}?
          </Badge>
        )
      })}
    </div>
  )
}
