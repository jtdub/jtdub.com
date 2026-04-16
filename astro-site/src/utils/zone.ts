export function zoneLabel(zone: string, style: 'short' | 'long' = 'short'): string {
  if (style === 'long') {
    return zone === 'field' ? 'Field & Research' : 'Engineering & Code';
  }
  return zone === 'field' ? 'Field' : 'Engineering';
}
