export function formatSummary(text: string) {
  return text
    .replace(/---/g, "")
    .replace(/•/g, "\n•")
    .replace(/Short-Term Recommendation:/g, "\n\n### Short-Term Recommendation:")
    .replace(/Medium-Term Recommendation:/g, "\n\n### Medium-Term Recommendation:")
    .replace(/Long-Term Recommendation:/g, "\n\n### Long-Term Recommendation:")
    .replace(/Existing Holder Advice:/g, "\n\n### Existing Holder Advice:")
    .replace(/New Investor Advice:/g, "\n\n### New Investor Advice:")
    .trim()
}
