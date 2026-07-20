/**
 * Public reconstruction of a workflow double filter.
 *
 * Input uses synthetic records only. The server-selected rows are checked
 * again before notification, and mismatches stop the workflow.
 */

const ALLOWED_STATUS = new Set(["eligible", "review"]);
const ALLOWED_CHANNEL = new Set(["email", "task"]);

function isWorkflowTarget(row, now) {
  const checkedAt = Date.parse(row.checkedAt);
  return (
    typeof row.recordId === "string" &&
    ALLOWED_STATUS.has(row.status) &&
    ALLOWED_CHANNEL.has(row.channel) &&
    row.sourceReceived === true &&
    Number.isFinite(checkedAt) &&
    checkedAt <= now.getTime()
  );
}

function verifyServerSelection(payload, now = new Date()) {
  const source = Array.isArray(payload.rows) ? payload.rows : [];
  const verified = source.filter((row) => isWorkflowTarget(row, now));
  const serverCount = Number(payload.serverCount ?? -1);
  const mismatch = serverCount !== verified.length;

  if (mismatch) {
    return {
      status: "blocked",
      reason: "server/workflow target mismatch",
      serverCount,
      verifiedCount: verified.length,
      rows: [],
    };
  }

  if (verified.length === 0) {
    return {
      status: "no_targets",
      reason: "normal early exit",
      serverCount: 0,
      verifiedCount: 0,
      rows: [],
    };
  }

  return {
    status: "ready",
    serverCount,
    verifiedCount: verified.length,
    rows: verified.map(({ recordId, status, channel }) => ({
      recordId,
      status,
      channel,
    })),
  };
}

module.exports = { isWorkflowTarget, verifyServerSelection };

