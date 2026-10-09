# Decision-Based AI Models

Comparison of different routing approaches for directing requests to five enterprise agents:

- Von
- Laya
- JEV
- SetFit

See [results.md](results.md) for the benchmark results.

## Benchmark language

The primary benchmark prompts were written in Turkish to evaluate multilingual and Turkish-language routing performance. Von also includes a separate English evaluation because its tested configuration is optimized for English; therefore, its English results should not be treated as directly equivalent to the Turkish results from the other routers.

## Security

API keys and local configuration files must not be committed to the repository. To run the JEV test:

```powershell
Copy-Item jev-test\.env.example jev-test\.env
```

Then set `JEV_API_KEY` in `jev-test\.env` to your local API key. `.env` files are excluded by `.gitignore`.

> If an API key has previously been shared or accidentally committed, revoke it in the provider dashboard and generate a new one. Removing it from Git history does not invalidate a leaked key.

## Project structure

| Directory | Contents |
|---|---|
| `jev-test` | JEV API-based agent and LLM router tests |
| `laya-test` | Laya multilingual router test |
| `setfit-test` | SetFit fine-tuning and unseen Turkish prompt tests |
| `von-test` | Von and SentenceTransformer-based router tests |

Local `.venv` directories, model outputs, and training checkpoints are not included in GitHub. These are reproducible local artifacts.
