export function formatNumber(value) {
  return Number(value).toLocaleString();
}

export function formatPercent(value) {
  return `${(value * 100).toFixed(2)}%`;
}