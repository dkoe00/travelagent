import { Separator } from "@/components/ui/separator"
import { ChatMessage, Constraints, PipelineStep, StepState, ToolLogEntry } from "@/lib/types"
import { ConstraintBadges } from "./ConstraintBadges"
import { PipelineSteps } from "./PipelineSteps"
import { ToolCallLog } from "./ToolCallLog"

export interface SidebarProps {
  constraints: Constraints
  pipeline: Record<PipelineStep, StepState>
  toolLog: ToolLogEntry[]
}

export function Sidebar({
  constraints,
  pipeline,
  toolLog,
}: SidebarProps): JSX.Element {
  return (
    <aside className="w-64 shrink-0 border-l overflow-y-auto p-4">
      <div className="space-y-6">
        <div>
          <h3 className="text-xs font-semibold text-muted-foreground mb-2">
            Erkannte Constraints
          </h3>
          <ConstraintBadges constraints={constraints} />
        </div>

        <Separator />

        <div>
          <h3 className="text-xs font-semibold text-muted-foreground mb-2">
            Pipeline
          </h3>
          <PipelineSteps pipeline={pipeline} />
        </div>

        <Separator />

        <div>
          <h3 className="text-xs font-semibold text-muted-foreground mb-2">
            Letzte Tool-Aufrufe
          </h3>
          <ToolCallLog toolLog={toolLog} />
        </div>
      </div>
    </aside>
  )
}
