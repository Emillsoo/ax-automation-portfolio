package portfolio.demo;

import java.util.Collections;
import java.util.List;
import java.util.Objects;

/**
 * Public reconstruction of a legacy-service facade.
 *
 * This class contains no production framework names, routes, schemas,
 * credentials, or patient identifiers.
 */
public final class MedicationHistoryFacade {

    private final ScreeningService screeningService;
    private final HistoryRepository historyRepository;
    private final AuditSink auditSink;

    public MedicationHistoryFacade(
            ScreeningService screeningService,
            HistoryRepository historyRepository,
            AuditSink auditSink) {
        this.screeningService = Objects.requireNonNull(screeningService);
        this.historyRepository = Objects.requireNonNull(historyRepository);
        this.auditSink = Objects.requireNonNull(auditSink);
    }

    public Response execute(Request request) {
        validate(request);

        ScreeningResult screening = screeningService.screen(
                request.subjectReference(),
                request.requestedAt());

        List<HistoryItem> history = historyRepository.findRecent(
                request.subjectReference(),
                request.lookbackDays());

        List<HistoryItem> safeHistory =
                history == null ? Collections.emptyList() : List.copyOf(history);

        auditSink.record(
                request.requestId(),
                screening.status(),
                safeHistory.size());

        return new Response(screening, safeHistory);
    }

    private static void validate(Request request) {
        Objects.requireNonNull(request, "request");
        if (isBlank(request.requestId())) {
            throw new IllegalArgumentException("requestId is required");
        }
        if (isBlank(request.subjectReference())) {
            throw new IllegalArgumentException("subjectReference is required");
        }
        if (request.lookbackDays() < 1 || request.lookbackDays() > 365) {
            throw new IllegalArgumentException("lookbackDays is out of range");
        }
    }

    private static boolean isBlank(String value) {
        return value == null || value.trim().isEmpty();
    }

    public record Request(
            String requestId,
            String subjectReference,
            java.time.Instant requestedAt,
            int lookbackDays) {}

    public record Response(
            ScreeningResult screening,
            List<HistoryItem> history) {}

    public record ScreeningResult(String status) {}

    public record HistoryItem(String category, String displayValue) {}

    public interface ScreeningService {
        ScreeningResult screen(String subjectReference, java.time.Instant requestedAt);
    }

    public interface HistoryRepository {
        List<HistoryItem> findRecent(String subjectReference, int lookbackDays);
    }

    public interface AuditSink {
        void record(String requestId, String screeningStatus, int resultCount);
    }
}

