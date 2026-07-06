export interface DestinationSuggestion { name: string; country: string; why: string; tags: string[] }
export interface DestinationList { suggestions: DestinationSuggestion[] }
export interface Place { kind: string; name: string; area: string; description: string; tags: string[] }
export interface PlacesPool { destination: string; places: Place[] }
export interface ItineraryStop { time_of_day: string; place_name: string; note: string }
export interface ItineraryDay { day: number; theme: string; stops: ItineraryStop[] }
export interface Itinerary { destination: string; days: ItineraryDay[] }

export type SpecialistTool = "discover_destinations" | "find_places" | "plan_itinerary"

export interface Constraints {
  region?: string | null; activity?: string | null; duration_days?: number | null
  month?: string | null; budget?: string | null
}

export type ToolPayload =
  | { tool: "discover_destinations"; payload: DestinationList }
  | { tool: "find_places"; payload: PlacesPool }
  | { tool: "plan_itinerary"; payload: Itinerary }

export interface ChatMessage {
  id: string
  role: "user" | "assistant"
  text: string
  toolResults: ToolPayload[]   // structured cards rendered above/with the text
  streaming: boolean
}

export interface ToolLogEntry { tool: string; status: "running" | "done" }

export type PipelineStep = "constraints" | "destination" | "places" | "itinerary" | "packing"
export type StepState = "done" | "running" | "pending"
