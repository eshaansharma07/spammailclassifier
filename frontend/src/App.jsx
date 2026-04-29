import { useMemo, useState } from "react";
import { Loader2, MailCheck, SendHorizonal, ShieldCheck } from "lucide-react";
import { classifyMessage } from "./api/client";
import ResultCard from "./components/ResultCard";

const EXAMPLES = [
  "Congratulations! You have won a free gift card. Claim now before midnight.",
  "Hi, can you review the project notes before tomorrow's meeting?",
];

export default function App() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const canAnalyze = useMemo(() => message.trim().length > 0 && !loading, [message, loading]);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!message.trim()) {
      setError("Enter an email message before analyzing.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const prediction = await classifyMessage(message.trim());
      setResult(prediction);
    } catch (apiError) {
      const detail = apiError.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Unable to analyze the message. Is the API running?");
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen overflow-hidden bg-slate-950 text-white">
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute left-[8%] top-[10%] h-56 w-56 rounded-full bg-teal-500/20 blur-3xl" />
        <div className="absolute right-[8%] top-[18%] h-64 w-64 rounded-full bg-rose-500/20 blur-3xl" />
        <div className="absolute bottom-[8%] left-[36%] h-72 w-72 rounded-full bg-indigo-500/15 blur-3xl" />
      </div>

      <section className="relative mx-auto flex min-h-screen w-full max-w-6xl flex-col px-5 py-8 sm:px-8 lg:px-10">
        <header className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="grid h-11 w-11 place-items-center rounded-2xl bg-white/10 shadow-glow ring-1 ring-white/15">
              <ShieldCheck className="h-6 w-6 text-teal-200" />
            </div>
            <div>
              <p className="text-sm text-slate-400">AI Email Security</p>
              <h1 className="text-xl font-semibold tracking-normal">Spam Mail Classifier</h1>
            </div>
          </div>
          <div className="hidden rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-slate-300 sm:block">
            TF-IDF + Naive Bayes
          </div>
        </header>

        <div className="grid flex-1 items-center gap-8 py-10 lg:grid-cols-[1.05fr_0.95fr]">
          <section>
            <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-teal-300/20 bg-teal-300/10 px-4 py-2 text-sm text-teal-100">
              <MailCheck className="h-4 w-4" />
              Real-time message risk analysis
            </div>
            <h2 className="max-w-3xl text-4xl font-bold leading-tight text-white sm:text-5xl lg:text-6xl">
              Catch suspicious email before it catches you.
            </h2>
            <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-300">
              Paste any email message and get a clear spam verdict, confidence score, and the words that influenced the model.
            </p>

            <div className="mt-7 flex flex-wrap gap-3">
              {EXAMPLES.map((example) => (
                <button
                  key={example}
                  type="button"
                  onClick={() => {
                    setMessage(example);
                    setError("");
                  }}
                  className="rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-slate-300 transition hover:border-teal-300/40 hover:bg-teal-300/10 hover:text-teal-100"
                >
                  Try example
                </button>
              ))}
            </div>
          </section>

          <section className="rounded-[28px] border border-white/10 bg-slate-900/70 p-5 shadow-2xl shadow-black/30 backdrop-blur-xl sm:p-6">
            <form onSubmit={handleSubmit} className="space-y-5">
              <label htmlFor="message" className="block text-sm font-medium text-slate-300">
                Email message
              </label>
              <textarea
                id="message"
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                placeholder="Paste the email body here..."
                className="min-h-52 w-full resize-y rounded-3xl border border-white/10 bg-slate-950/70 px-5 py-4 text-base leading-7 text-white outline-none transition placeholder:text-slate-500 focus:border-teal-300/60 focus:ring-4 focus:ring-teal-300/10"
              />

              {error && (
                <div className="rounded-2xl border border-red-300/20 bg-red-500/10 px-4 py-3 text-sm text-red-100">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={!canAnalyze}
                className="group flex w-full items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-teal-400 via-cyan-400 to-indigo-400 px-5 py-4 font-semibold text-slate-950 shadow-glow transition duration-300 hover:scale-[1.01] hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:scale-100"
              >
                {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <SendHorizonal className="h-5 w-5 transition group-hover:translate-x-1" />}
                {loading ? "Analyzing..." : "Analyze"}
              </button>
            </form>

            <div className="mt-5">
              {loading ? (
                <div className="result-shell border-white/10 bg-white/[0.04]">
                  <div className="flex items-center gap-4">
                    <div className="h-12 w-12 rounded-2xl bg-teal-300/20 animate-pulseGlow" />
                    <div className="flex-1 space-y-3">
                      <div className="h-3 w-1/2 rounded-full bg-white/15" />
                      <div className="h-3 w-3/4 rounded-full bg-white/10" />
                    </div>
                  </div>
                </div>
              ) : (
                <ResultCard result={result} />
              )}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}
