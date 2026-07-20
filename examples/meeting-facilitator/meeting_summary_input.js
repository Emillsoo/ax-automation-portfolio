/**
 * Build a minimal, structured meeting-summary input.
 * Real member names and transcripts are intentionally absent.
 */

function buildSummaryInput({ meetingType, speakers, logs }) {
  if (!meetingType || !Array.isArray(speakers) || !Array.isArray(logs)) {
    throw new Error("invalid meeting payload");
  }

  const allowedSpeakers = new Set(speakers.map((item) => item.speakerRef));
  const sanitizedLogs = logs
    .filter((item) => allowedSpeakers.has(item.speakerRef))
    .map((item) => ({
      speakerRef: item.speakerRef,
      text: String(item.text ?? "").trim(),
    }))
    .filter((item) => item.text);

  return {
    meetingType,
    requestedSections: ["decisions", "actions", "owners", "dueDates"],
    logs: sanitizedLogs,
  };
}

module.exports = { buildSummaryInput };
