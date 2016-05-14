import ring_pattern
import abstract_ringer

ringer = abstract_ringer.Ringer()
r = ring_pattern.ring_pattern(ringer)
r.standard_ring(first=True)
