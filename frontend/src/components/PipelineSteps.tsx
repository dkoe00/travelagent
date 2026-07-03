import { CheckCircle2, Loader2, Circle } from "lucide-react"
import type { PipelineStep, StepState } from "@/lib/types"

const STEP_LABELS: Record<PipelineStep, string> = {
  constraints: "Constraints",
  destination: "Destination",
  places: "Places",
  itinerary: "Itinerary",
  packing: "Packing list",
}

export interface PipelineStepsProps {
  pipeline: Record<PipelineStep, StepState>
}

export function PipelineSteps({ pipeline }: PipelineStepsProps): JSX.Element {
  const steps: PipelineStep[] = ["constraints", "destination", "places", "itinerary", "packing"]

  return (
    <div className="space-y-2">
      {steps.map((step) => {
        const state = pipeline[step]
        return (
          <div key={step} className="flex items-center gap-2 text-sm">
            {state === "done" && (
              <CheckCircle2 className="w-4 h-4 text-green-600" />
            )}
            {state === "running" && (
              <Loader2 className="w-4 h-4 text-accent animate-spin" />
            )}
            {state === "pending" && (
              <Circle className="w-4 h-4 text-muted-foreground" />
            )}
            <span className={state === "running" ? "font-medium" : ""}>
              {STEP_LABELS[step]}
            </span>
          </div>
        )
      })}
    </div>
  )
}
