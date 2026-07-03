import { useChatSession } from "@/hooks/useChatSession"
import { Header } from "@/components/Header"
import { ChatPanel } from "@/components/ChatPanel"
import { Sidebar } from "@/components/Sidebar"

export default function App(): JSX.Element {
  const session = useChatSession()

  return (
    <div className="h-screen flex flex-col bg-background">
      <Header onNewChat={session.newChat} />
      <div className="flex-1 flex overflow-hidden max-w-5xl mx-auto w-full">
        <ChatPanel
          messages={session.messages}
          runningTool={session.runningTool}
          busy={session.busy}
          error={session.error}
          onSend={session.sendMessage}
          onSelectDestination={(name) => session.sendMessage(`Ich nehme ${name}`)}
        />
        <Sidebar
          constraints={session.constraints}
          pipeline={session.pipeline}
          toolLog={session.toolLog}
        />
      </div>
    </div>
  )
}
