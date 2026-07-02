from app.retrieval.volume import count_mentions

def detect_volume_spike(brand: str) -> dict:
    recent = count_mentions(brand, hours=6)
    baseline_total = count_mentions(brand, hours=24 * 7)
    baseline_per_6h = baseline_total / 28 if baseline_total else 0

    spike_ratio = recent / baseline_per_6h if baseline_per_6h > 0 else (recent / 1)

    return {
        "recent_6h": recent,
        "baseline_per_6h": round(baseline_per_6h, 2),
        "spike_ratio": round(spike_ratio, 2),
        "is_anomaly": spike_ratio >= 2.5
    }
