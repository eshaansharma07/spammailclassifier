import { AlertTriangle, CheckCircle2, Sparkles } from "lucide-react";

export default function ResultCard({ result }) {
  if (!result) {
    return (
      <section className="result-shell border-white/10 bg-white/[0.04] text-slate-300">
        <div className="flex items-center gap-3">
          <Sparkles className="h-5 w-5 text-teal-300" />
          <p className="text-sm">Paste an email and run analysis to see the verdict.</p>
        </div>
      </section>
    );
  }

  const isSpam = result.prediction === "spam";
  const confidence = Math.round(result.confidence * 100);

  return (
    <section
      className={`result-shell ${
        isSpam
          ? "border-red-400/30 bg-red-500/[0.08] shadow-red-950/30"
          : "border-emerald-400/30 bg-emerald-500/[0.08] shadow-emerald-950/30"
      }`}
    >
      <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex items-start gap-4">
          <div
            className={`rounded-2xl p-3 ${
              isSpam ? "bg-red-500/15 text-red-300" : "bg-emerald-500/15 text-emerald-300"
            }`}
          >
            {isSpam ? <AlertTriangle className="h-7 w-7" /> : <CheckCircle2 className="h-7 w-7" />}
          </div>
          <div>
            <p className="text-sm uppercase tracking-[0.22em] text-slate-400">Prediction</p>
            <h2 className={`mt-1 text-3xl font-bold ${isSpam ? "text-red-200" : "text-emerald-200"}`}>
              {isSpam ? "Spam" : "Not Spam"}
            </h2>
          </div>
        </div>

        <div className="min-w-32 rounded-2xl border border-white/10 bg-slate-950/45 px-5 py-4 text-left sm:text-right">
          <p className="text-sm text-slate-400">Confidence</p>
          <p className="text-3xl font-semibold text-white">{confidence}%</p>
        </div>
      </div>

      <div className="mt-6">
        <p className="mb-3 text-sm font-medium text-slate-300">Top signals</p>
        {result.important_words?.length ? (
          <div className="flex flex-wrap gap-2">
            {result.important_words.map((word) => (
              <span
                key={word}
                className={`rounded-full border px-3 py-1 text-sm ${
                  isSpam
                    ? "border-red-300/20 bg-red-300/10 text-red-100"
                    : "border-emerald-300/20 bg-emerald-300/10 text-emerald-100"
                }`}
              >
                {word}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-sm text-slate-400">No strong word-level signals were found.</p>
        )}
      </div>
    </section>
  );
}
