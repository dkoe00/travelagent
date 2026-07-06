import { Plane } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

export interface HeaderProps {
  onNewChat: () => void
}

export function Header({ onNewChat }: HeaderProps): JSX.Element {
  return (
    <header className="flex items-center justify-between px-4 py-3 border-b bg-neutral-900">
      <div className="flex items-center gap-3">
        <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-blue-500/15 text-blue-400">
          <Plane className="w-5 h-5" />
        </div>
        <div>
          <h1 className="text-lg font-semibold">Travel Agent</h1>
          <p className="text-xs text-muted-foreground">Multi-Agent-Reiseplanung</p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <Badge className="bg-green-600/80 text-white hover:bg-green-600">Coordinator aktiv</Badge>
        <Button variant="outline" size="sm" onClick={onNewChat}>
          Neuer Chat
        </Button>
      </div>
    </header>
  )
}
