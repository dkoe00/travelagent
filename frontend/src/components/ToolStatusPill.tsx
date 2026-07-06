import { Loader2 } from "lucide-react"

export interface ToolStatusPillProps {
  tool: string
}

export function ToolStatusPill({ tool }: ToolStatusPillProps): JSX.Element {
  return (
    <div className="flex items-center gap-2 px-3 py-2 bg-accent/10 border border-accent/30 rounded-full text-sm">
      <Loader2 className="w-4 h-4 animate-spin text-accent" />
      <span>Tool-Aufruf: <code className="text-xs font-mono">{tool}</code> läuft…</span>
    </div>
  )
}
