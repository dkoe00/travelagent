import { ToolLogEntry } from "@/lib/types"

export interface ToolCallLogProps {
  toolLog: ToolLogEntry[]
}

export function ToolCallLog({ toolLog }: ToolCallLogProps): JSX.Element {
  const last6 = toolLog.slice(-6)

  return (
    <div className="space-y-1 font-mono text-xs text-muted-foreground">
      {last6.map((entry, idx) => (
        <div key={idx}>
          {entry.tool} {entry.status === "done" ? "✓" : "…"}
        </div>
      ))}
    </div>
  )
}
