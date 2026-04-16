export function zoneLabel(zone: string, style: 'short' | 'long' = 'short'): string {
  const labels: Record<string, { short: string; long: string }> = {
    field: { short: 'Field', long: 'Field & Research' },
    engineering: { short: 'Engineering', long: 'Engineering & Code' },
    essays: { short: 'Essays', long: 'Essays & Reflections' },
  };
  const entry = labels[zone] ?? labels.engineering;
  return style === 'long' ? entry.long : entry.short;
}
