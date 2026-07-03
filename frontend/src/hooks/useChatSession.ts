import { useState, useCallback } from "react"
import { postSse } from "@/lib/sse"
import type {
  ChatMessage,
  Constraints,
  PipelineStep,
  StepState,
  ToolLogEntry,
  ToolPayload,
  SpecialistTool,
} from "@/lib/types"

interface UseChatSessionState {
  messages: ChatMessage[]
  constraints: Constraints
  toolLog: ToolLogEntry[]
  runningTool: string | null
  busy: boolean
  error: string | null
  sessionId: string | null
  pipeline: Record<PipelineStep, StepState>
}

export function useChatSession(): UseChatSessionState & {
  sendMessage: (text: string) => Promise<void>
  newChat: () => void
} {
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [constraints, setConstraints] = useState<Constraints>({})
  const [toolLog, setToolLog] = useState<ToolLogEntry[]>([])
  const [runningTool, setRunningTool] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Derived pipeline state
  const pipeline: Record<PipelineStep, StepState> = {
    constraints: Object.values(constraints).some((v) => v != null) ? "done" : "pending",
    destination: runningTool === "discover_destinations"
      ? "running"
      : messages.some((m) =>
          m.toolResults.some((tr) => tr.tool === "discover_destinations")
        )
      ? "done"
      : "pending",
    places: runningTool === "find_places"
      ? "running"
      : messages.some((m) =>
          m.toolResults.some((tr) => tr.tool === "find_places")
        )
      ? "done"
      : "pending",
    itinerary: runningTool === "plan_itinerary"
      ? "running"
      : messages.some((m) =>
          m.toolResults.some((tr) => tr.tool === "plan_itinerary")
        )
      ? "done"
      : "pending",
    packing: "pending",
  }

  const ensureSession = useCallback(async (): Promise<string> => {
    if (sessionId) return sessionId
    try {
      const res = await fetch("/api/sessions", { method: "POST" })
      const data = await res.json()
      setSessionId(data.session_id)
      return data.session_id
    } catch {
      throw new Error("Verbindung fehlgeschlagen. Läuft der API-Server?")
    }
  }, [sessionId])

  const sendMessage = useCallback(
    async (text: string) => {
      const id = await ensureSession()
      try {
        setError(null)
        setBusy(true)
        setMessages((prev) => [
          ...prev,
          { id: Date.now().toString(), role: "user", text, toolResults: [], streaming: false },
          { id: (Date.now() + 1).toString(), role: "assistant", text: "", toolResults: [], streaming: true },
        ])

        const lastMessageIndex = messages.length + 1

        await postSse(`/api/sessions/${id}/messages`, { content: text }, (evt) => {
          if (evt.event === "text_delta") {
            const data = evt.data as { delta: string }
            setMessages((prev) => {
              const updated = [...prev]
              if (updated[lastMessageIndex]) {
                updated[lastMessageIndex] = {
                  ...updated[lastMessageIndex],
                  text: updated[lastMessageIndex].text + data.delta,
                }
              }
              return updated
            })
          } else if (evt.event === "tool_started") {
            const data = evt.data as { tool: string; arguments: string }
            setRunningTool(data.tool)
            setToolLog((prev) => [...prev, { tool: data.tool, status: "running" }])
          } else if (evt.event === "tool_finished") {
            const data = evt.data as { tool: string; payload: unknown }
            setRunningTool(null)
            setToolLog((prev) =>
              prev.map((e) =>
                e.tool === data.tool ? { ...e, status: "done" } : e
              )
            )
            const toolPayload: ToolPayload = {
              tool: data.tool as SpecialistTool,
              payload: data.payload as never,
            }
            setMessages((prev) => {
              const updated = [...prev]
              if (updated[lastMessageIndex]) {
                updated[lastMessageIndex] = {
                  ...updated[lastMessageIndex],
                  text: "",
                  toolResults: [...updated[lastMessageIndex].toolResults, toolPayload],
                }
              }
              return updated
            })
          } else if (evt.event === "constraints") {
            const data = evt.data as Constraints
            setConstraints((prev) => ({ ...prev, ...data }))
          } else if (evt.event === "final") {
            const data = evt.data as { text: string }
            setMessages((prev) => {
              const updated = [...prev]
              if (updated[lastMessageIndex]) {
                updated[lastMessageIndex] = {
                  ...updated[lastMessageIndex],
                  text: data.text,
                  streaming: false,
                }
              }
              return updated
            })
          } else if (evt.event === "error") {
            const data = evt.data as { message: string }
            setError(data.message)
            setMessages((prev) => {
              const updated = [...prev]
              if (updated[lastMessageIndex]) {
                updated[lastMessageIndex] = {
                  ...updated[lastMessageIndex],
                  streaming: false,
                }
              }
              return updated
            })
          } else if (evt.event === "done") {
            setBusy(false)
          }
        })
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Fehler beim Senden"
        setError(msg)
        setBusy(false)
        setMessages((prev) => {
          const updated = [...prev]
          if (updated[lastMessageIndex]) {
            updated[lastMessageIndex] = {
              ...updated[lastMessageIndex],
              streaming: false,
            }
          }
          return updated
        })
      }
    },
    [messages.length, sessionId, ensureSession]
  )

  const newChat = useCallback(async () => {
    if (sessionId) {
      try {
        await fetch(`/api/sessions/${sessionId}`, { method: "DELETE" })
      } catch {
        /* ignore */
      }
    }
    setSessionId(null)
    setMessages([])
    setConstraints({})
    setToolLog([])
    setRunningTool(null)
    setError(null)
    setBusy(false)
  }, [sessionId])

  return {
    messages,
    constraints,
    toolLog,
    runningTool,
    busy,
    error,
    sessionId,
    pipeline,
    sendMessage,
    newChat,
  }
}
