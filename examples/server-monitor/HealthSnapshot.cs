using System;
using System.Collections.Generic;
using System.Linq;

namespace Portfolio.ServerMonitor
{
    public sealed class ServiceSnapshot
    {
        public string ServiceRef { get; set; }
        public string State { get; set; }
    }

    public sealed class HealthSnapshot
    {
        public string ServerRef { get; set; }
        public DateTime CollectedAtUtc { get; set; }
        public double CpuPercent { get; set; }
        public double MemoryPercent { get; set; }
        public IReadOnlyList<ServiceSnapshot> Services { get; set; }

        public bool IsHealthy(double resourceLimitPercent)
        {
            if (CpuPercent > resourceLimitPercent ||
                MemoryPercent > resourceLimitPercent)
            {
                return false;
            }

            return Services != null &&
                Services.All(service =>
                    string.Equals(
                        service.State,
                        "running",
                        StringComparison.OrdinalIgnoreCase));
        }
    }
}
